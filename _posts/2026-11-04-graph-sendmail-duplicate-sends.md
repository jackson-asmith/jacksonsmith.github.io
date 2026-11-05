---
title: "Your Send-MailMessage replacement might be sending email twice"
description: Microsoft Graph's sendMail isn't safe to repeat, and the Graph PowerShell SDK retries it after a 504 by default. Here's how one failed send became four, and how to stop it.
date: 2026-11-04
principles: [Reliability is a feature, Automation must reduce risk, Testing comes before trust]
---

If you run PowerShell automation against Exchange Online, you've probably been moving scripts off `Send-MailMessage`. The cmdlet is obsolete, and Microsoft has been retiring Basic authentication for SMTP AUTH, so scripts that log in to `smtp.office365.com` with a username and password stop working. The recommended replacement is Microsoft Graph's `sendMail` API with app-only authentication, usually through the Microsoft Graph PowerShell SDK.

That migration has a trap I didn't see coming: with default settings, one failed send can deliver the same email several times.

## sendMail isn't safe to repeat

`POST /users/{id}/sendMail` returns `202 Accepted` and nothing else. There's no message ID in the response and no idempotency key you can send. If a request fails, you can't ask Graph "did that one go through?" and resend only if it didn't.

Most failures are clear about that. A `400` or `403` means Graph rejected the request. A `429` or `503` means Graph is busy and didn't process it. Resending those is safe.

A `504 Gateway Timeout` isn't clear. A gateway gave up waiting for the service behind it, and that service may already have accepted the message. The same goes for a `500`, a `502`, or a connection that drops after the request was sent. After any of those, resending might deliver a second copy.

## The SDK retries it anyway

The Graph PowerShell SDK sends requests through a retry handler from Microsoft's Kiota HTTP library. By default it retries `429`, `503`, and `504` up to three times. It skips POST requests only when the body is streamed with an unknown length. A `sendMail` call has a small JSON body of known length, so it gets retried like anything else.

I reproduced this with a stub endpoint standing in for Graph that answers every request with `504`. One `Invoke-MgGraphRequest` call to `sendMail`, with default settings, produced this:

```text
Invoke-MgGraphRequest failed: Too many retries performed. More than 3 retries encountered while sending the request.
Requests received by the stub: 4
  POST /v1.0/users/sender@contoso.com/sendMail
  POST /v1.0/users/sender@contoso.com/sendMail
  POST /v1.0/users/sender@contoso.com/sendMail
  POST /v1.0/users/sender@contoso.com/sendMail
```

Four POSTs, and the caller sees one error. If Graph had accepted the first one, the recipients would get the message up to four times, and the script would report that it failed.

I tested this with `Invoke-MgGraphRequest` and `Microsoft.Graph.Authentication` 2.40.0. Generated cmdlets such as `Send-MgUserMail` use the same SDK HTTP pipeline, but I haven't tested them directly.

## My own wrapper had the same bug

I ran into this while building [Keel](https://github.com/jackson-asmith/keel), a small PowerShell library for unattended mail. It wraps Graph sending behind one `Send-Email` command, with SMTP fallback for when Graph is unavailable. A code review of its first version flagged the problem, and the [Keel case study](/projects/keel/) covers the design side of the fix.

That first version made things worse. It retried `408`, `429`, `500`, `502`, `503`, and `504`, and then fell back to SMTP on any Graph failure. So one `504` could mean three Graph attempts, each possibly retried by the SDK underneath, followed by an SMTP send. For alerting, that isn't a cosmetic problem. Duplicate alerts teach people to ignore alerts, and a duplicated notice to a customer looks like a malfunction.

## The fix: only resend when Graph clearly refused

Keel now follows one rule: resend, through Graph or SMTP, only when the failure proves Graph didn't accept the message. When delivery is uncertain, stop and say so.

In practice:

- **Safe to resend:** any `4xx`, `503`, and connection failures that happen before the request is sent, such as DNS lookups, refused connections, and TLS errors. Keel retries `429` and `503`, honoring `Retry-After`.
- **Possibly delivered:** `500`, `502`, `504`, timeouts, and connections dropped mid-request. Keel doesn't retry and doesn't fall back to SMTP. It throws a `GraphDeliveryUnknown` error telling the operator to check message trace before resending.
- **Anything it doesn't recognize** counts as possibly delivered, so gaps fail safe.

Then it turns off the SDK's own retries for each send, so Keel is the only thing deciding what to retry:

```powershell
$saved = Get-MgRequestContext
$restore = @{
    MaxRetry         = $saved.MaxRetry
    RetryDelay       = $saved.RetryDelay
    # Get-MgRequestContext returns a TimeSpan; Set-MgRequestContext takes seconds.
    RetriesTimeLimit = [int]$saved.RetriesTimeLimit.TotalSeconds
}
$request = @{
    Method      = 'POST'
    Uri         = "/v1.0/users/$([uri]::EscapeDataString($sender))/sendMail"
    Body        = $json
    ContentType = 'application/json'
}

Set-MgRequestContext -MaxRetry 0 | Out-Null
try {
    Invoke-MgGraphRequest @request
}
finally {
    Set-MgRequestContext @restore | Out-Null
}
```

One caveat: the SDK's request context is process-wide, shared by every runspace, so while that call is in flight, other Graph calls in the same process also run without SDK retries.

**Update, November 2026:** if one process sends in parallel, for example with `ForEach-Object -Parallel`, this snippet isn't enough on its own. Two overlapping sends can undo each other: one restores retries while the other's request is going out, and the SDK resends it after a 504. Run sends one at a time, or hold one lock shared by the whole process around saving, changing, and restoring the settings. keel does the latter as of [1.1.1](https://github.com/jackson-asmith/keel/releases/tag/v1.1.1); [PR #12](https://github.com/jackson-asmith/keel/pull/12) has the details.

The trade-off is deliberate. Some messages that a retry would have delivered now fail instead. I'd rather a job fail loudly than send a quiet duplicate. The full reasoning is in [ADR 0002](https://github.com/jackson-asmith/keel/blob/main/docs/adr/0002-no-resend-after-ambiguous-graph-failure.md).

## Testing it without a tenant

Unit tests with a mocked `Invoke-MgGraphRequest` can't catch this, because the retries happen inside the SDK. So Keel's integration tests run the real `Microsoft.Graph.Authentication` module against a local stub:

- A `System.Net.HttpListener` stands in for Graph and answers with whatever status the test queues up.
- `Add-MgEnvironment` points the SDK at the stub, and `Connect-MgGraph -AccessToken` signs in with an unsigned fake token, which the stub ignores.
- One quirk: `Invoke-MgGraphRequest` resolves relative URIs against the environment's host and drops any custom port, so the stub has to listen on port 80. macOS allows that without elevation, and GitHub's Windows runners run as administrator.

The tests assert that a `504` produces exactly one request, that a `429` is retried by Keel and not the SDK, and that the caller's SDK retry settings are restored afterward. They run in CI on macOS with PowerShell 7 and on Windows PowerShell 5.1, with no tenant, no credentials, and no mail sent.

## If you're migrating

1. Treat `sendMail` as unsafe to repeat. A `504`, `500`, or timeout means "maybe delivered", not "failed".
2. Turn off the SDK's retries around sends, or make sure whatever retries for you treats those statuses as final.
3. Don't fall back to SMTP after an ambiguous Graph failure, or you've just built a duplicate-sender.
4. Tell the operator what happened. "Check message trace before resending" beats a silent second copy.

I've reported the retry behavior to the Kiota maintainers in [microsoft/kiota-dotnet#851](https://github.com/microsoft/kiota-dotnet/issues/851), with a reproduction script, and suggested not retrying `504` for POST requests by default. Until something changes, `MaxRetry 0` around your sends is the workaround.

Keel is [on GitHub](https://github.com/jackson-asmith/keel) under the MIT license.
