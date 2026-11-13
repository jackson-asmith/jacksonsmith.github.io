---
title: "One retry fix, eight Kiota SDKs"
description: I fixed a duplicate-send bug in Kiota's .NET retry handler, and the maintainer asked me to port it to every other language. The fix was the same everywhere. The code around it wasn't.
date: 2026-11-13
principles: [Reliability is a feature, Testing comes before trust]
---

Last week I wrote about [how Microsoft Graph's `sendMail` can send the same email four times](/writing/2026/graph-sendmail-duplicate-sends/). The root cause is in the retry handler of Kiota, the HTTP library under Microsoft's Graph SDKs: after a `504 Gateway Timeout`, it resends a POST that the server may already have processed.

I reported it in [microsoft/kiota-dotnet#851](https://github.com/microsoft/kiota-dotnet/issues/851). This post covers what happened next: a fix in .NET, a request to port it to seven more languages, and how much the "same fix" changed from one codebase to the next.

## The fix: an opt-in setting

The change adds one setting to the retry handler. When it's on, POST and PATCH requests are retried only after a `429` or `503`, the two responses that, by common service convention, mean the server didn't process the request. A `504`, or any other response the handler would normally retry, goes back to the caller instead. GET, PUT, DELETE and other idempotent methods keep retrying as before.

It's off by default, so nobody's retries change unless they ask. My first version got there backwards: it was called `RetryNonIdempotentRequestsWhenOutcomeUnknown`, where the default of `true` kept today's retries and `false` turned the protection on. The maintainer pointed out that a default of `true` is counterintuitive. After two renames it became `RetryUnprocessedMutationsOnly`, where `true` turns the protection on and the default is `false`.

That name isn't perfectly precise: PUT and DELETE are mutations too, but they're idempotent, so the setting leaves them alone. I said so in review, offered a longer exact name, and took theirs. The docs carry the nuance, and a short name the maintainers chose is worth more than a precise one they'd have to live with.

## Eight days, then a few hours

The issue sat for eight days with no response. The pull request, [microsoft/kiota-dotnet#864](https://github.com/microsoft/kiota-dotnet/pull/864), was reviewed within hours and merged the next morning. Then the maintainer asked whether I'd port it to Python, PHP, TypeScript, Go, Dart, Ruby and Java, and opened an issue in each repository with a checklist of the tests they wanted. All seven ports were merged by the end of that same day.

If you're hoping to get a bug fixed in a busy open source project, that's the lesson I'd pass on: an issue asks maintainers for their time, while a tested pull request asks for much less of it.

## Same fix, different code

The rule was identical in every language. Applying it wasn't, because the eight SDKs handle retries differently in three ways that turned out to matter.

**Who handles redirects first.** In .NET, Go and TypeScript, the retry handler wraps the redirect handler, so it sees responses only after redirects have been followed. In Python, Java, PHP and Ruby, it's the other way around: the redirect handler wraps the retry handler, which only ever sees one hop at a time.

**What a retry resends.** This is where the first difference bites. When a POST gets a `303 See Other`, it's followed as a GET. If that GET gets a `504` and the retry handler sits outside the redirect handler, what does a retry send?

| SDK | A retry after a redirect resends |
|---|---|
| .NET | the redirected request, taken from the response |
| Go | the original POST |
| TypeScript | the request object, which the redirect handler already changed to a GET |
| Dart | the original POST |
| Python, Java, PHP, Ruby | only the current hop, since redirects happen outside |

So "check the method of the request" means a different request in each codebase. In .NET it's the redirected one. In Go and Dart it's the original. Get it wrong and the setting either blocks safe retries or misses unsafe ones. My first .NET version checked the wrong one, and an automated review caught it before it merged.

**Whether callers could already work around it.** In .NET, Go, Java, TypeScript and Ruby, the retry callback can see the request's method, so a determined caller could filter retries themselves. In Python the callback is just an on/off switch, and in PHP it never receives the request, so there was no workaround short of subclassing the handler. Dart had no retry handler of its own at all: it wraps a generic retry client with a fixed rule that retried POSTs after a `408`, `500`, `502` or `504`. There, the setting became a parameter on the client factory, and per-request configuration would have meant inventing a mechanism the SDK doesn't have.

## The bug I nearly shipped twice

Go and Dart both resend the original POST after a redirect. That created a case none of my tests covered: a POST gets a `303`, the redirected GET gets a `503`, and the setting allows the retry, because `503` means "not processed."

But the `503` describes the GET. The `303` already showed the server accepted the POST, and the retry resends that POST. The setting meant to prevent duplicate sends would have allowed one.

An automated review raised this on the Dart pull request. The same flaw was in Go, which nobody had flagged. The fix in both is to never retry a POST or PATCH that was redirected, since the redirect itself proves the server accepted it. Go detects that the method changed; Dart compares the response's final URL with the request's. Dart's version has a known gap: its HTTP library only exposes the final URL, so a redirect chain that ends back at the original URL goes undetected. That limit is documented rather than hidden.

## What review caught

Across eight pull requests, review found:

- the wrong request being checked in .NET
- the redirect case above, in Go and Dart
- missing redirect tests in Python and Java, which the maintainer's checklist had asked for and I'd skipped because I'd reasoned the case couldn't happen there
- a PHP code path, where the HTTP client throws on a `504` instead of returning it, that I'd claimed was covered but never tested
- Dart tests "for the default" that passed the default value explicitly, so they would have kept passing if the default changed

Two habits came out of that. When a maintainer gives you a test checklist, write every test on it, even the ones your reasoning says are redundant: the reasoning is the thing being tested. And to test a default, leave the argument out.

## If you use the Graph SDKs

For .NET, the setting is merged and will ship in the next kiota-dotnet release, 2.2.0 in the [open release pull request](https://github.com/microsoft/kiota-dotnet/pull/854). Once it's out, code that builds its own Graph client can turn it on through `RetryHandlerOption`:

```csharp
var retryOption = new RetryHandlerOption
{
    RetryUnprocessedMutationsOnly = true
};
```

The other seven SDKs have the same setting under their own naming conventions, merged in [Go](https://github.com/microsoft/kiota-http-go/pull/312), [Python](https://github.com/microsoft/kiota-python/pull/897), [Java](https://github.com/microsoft/kiota-java/pull/2251), [TypeScript](https://github.com/microsoft/kiota-typescript/pull/2230), [PHP](https://github.com/microsoft/kiota-php/pull/143), [Dart](https://github.com/microsoft/kiota-dart/pull/179) and [Ruby](https://github.com/microsoft/kiota-ruby/pull/225). Each arrives with that SDK's next release.

Two caveats. The generated SDKs don't turn it on for you, so you have to opt in. And the Graph PowerShell SDK can't set it yet: `Set-MgRequestContext` only exposes `MaxRetry`, `RetryDelay` and `RetriesTimeLimit`. For PowerShell scripts, [turning off SDK retries around your sends](/writing/2026/graph-sendmail-duplicate-sends/) is still the workaround, and it's what [keel](https://github.com/jackson-asmith/keel) keeps doing for now.
