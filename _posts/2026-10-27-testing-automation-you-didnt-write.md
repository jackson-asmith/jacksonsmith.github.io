---
title: "Testing automation you didn't write"
image: /assets/img/social/post-testing-automation.png
description: A practical approach to adding Pester tests to an existing PowerShell script, before you touch a single line of logic.
date: 2026-10-27
updated: 2026-11-23
principles: [Testing comes before trust, Automation must reduce risk, Modernize incrementally]
---

Somebody hands you a PowerShell script. It's been running in production for two years. Nobody knows exactly what it does in every case, but it works, and people depend on it. Your job is to change it.

This is the situation Pester tutorials don't cover. They show you how to test code you're writing from scratch, with clean inputs and predictable outputs. They don't show you how to build confidence in 400 lines of inherited automation that mixes business logic with API calls and writes to the filesystem in the same function.

Here's how I approach it.

## Start with characterization, not coverage

Before writing a single test, get clear on what you're actually trying to achieve. You're not aiming for 80% coverage. You're trying to make it safe to change something.

That means identifying the behavior that, if it broke, would cause a real problem: the thing that fires a notification, modifies an account, or deletes a record. Everything else is secondary.

A characterization test captures what the code *does* before you fully understand why. You run it, observe the output, and write a test that asserts exactly that output. You're not validating that the behavior is correct. You're creating a regression wire. If your change alters the behavior, the test will tell you.

```powershell
Describe 'Get-UserStatus' {
    BeforeAll {
        # Load the code under test. For a module, use Import-Module instead.
        . $PSScriptRoot/../src/Get-UserStatus.ps1

        Mock Get-ADUser {
            return [pscustomobject]@{ SamAccountName = 'jsmith'; Enabled = $false }
        }
    }

    It 'returns Disabled for an inactive account' {
        $result = Get-UserStatus -SamAccountName 'jsmith'
        $result.Status | Should -Be 'Disabled'
    }
}
```

That test might encode a bug. That's fine. The goal at this stage is a stable baseline, not a specification. You can fix correctness once you can verify behavior.

If the code lives in a module, mocking gets one extra step: a mock defined in the test doesn't replace a command the module calls internally unless you scope it with `Mock -ModuleName`, or run the test inside `InModuleScope`. When a mock "doesn't work", that's usually why.

## Find the seams

Most inherited scripts fail the same way: side effects are everywhere. An API call happens in the middle of a decision. A file write is buried inside a transformation. There's no clean boundary between "figure out what to do" and "do it."

You can't easily test code in that shape. But you don't have to rewrite it to make it testable. You need to find the seams.

A seam is a place where you can change what happens without changing the code around it. The most common form in PowerShell is a function boundary. If the script is a single long function, your first move is to extract the decision logic into its own function that takes data and returns data, with no side effects.

Before:

```powershell
function Disable-StaleAccounts {
    $users = Get-ADUser -Filter { Enabled -eq $true }
    foreach ($user in $users) {
        $lastLogon = $user.LastLogonDate
        if ($lastLogon -lt (Get-Date).AddDays(-90)) {
            Set-ADUser -Identity $user -Enabled $false
            Write-Log "Disabled $($user.SamAccountName)"
        }
    }
}
```

The staleness check is untestable here, because it's tangled with the AD query and the mutation. Extract it:

```powershell
function Test-AccountIsStale {
    param(
        [Nullable[datetime]]$LastLogonDate,
        [int]$ThresholdDays = 90,
        [datetime]$AsOf = (Get-Date)
    )
    # An account that has never logged on has no LastLogonDate at all.
    # Counting it as stale is a business rule, so it's stated here
    # instead of falling out of how $null happens to compare.
    if ($null -eq $LastLogonDate) { return $true }
    return $LastLogonDate -lt $AsOf.AddDays(-$ThresholdDays)
}
```

Now `Test-AccountIsStale` has no external dependencies. It takes data and returns a boolean. The `$AsOf` parameter is worth calling out: without it, `Get-Date` is an implicit dependency and tests near the exact threshold boundary will be flaky. Injecting the reference date keeps the function pure and the threshold edge cases reliable.

The `[Nullable[datetime]]` is there on purpose. Active Directory leaves `LastLogonDate` empty for an account that has never logged on, so the real value is `$null`. The original inline comparison treated that as stale, because `$null -lt` a date is `$true` in PowerShell. A plain `[datetime]` parameter can't accept `$null` and would throw instead, so the extraction would have quietly changed behavior for exactly the accounts most likely to be stale.

You can now test every scenario without touching Active Directory or a mock: accounts inactive for 91 days, exactly 90 days, active yesterday, or never logged on.

```powershell
Describe 'Test-AccountIsStale' {
    BeforeAll {
        $now = [datetime]'2024-06-01'
    }

    It 'returns true for an account inactive for 91 days' {
        $result = Test-AccountIsStale -LastLogonDate $now.AddDays(-91) -AsOf $now
        $result | Should -Be $true
    }

    It 'returns false for an account inactive for exactly 90 days' {
        # -lt means the threshold day itself isn't stale yet. This test pins that choice.
        $result = Test-AccountIsStale -LastLogonDate $now.AddDays(-90) -AsOf $now
        $result | Should -Be $false
    }

    It 'returns false for an account active yesterday' {
        $result = Test-AccountIsStale -LastLogonDate $now.AddDays(-1) -AsOf $now
        $result | Should -Be $false
    }

    It 'returns true for an account that has never logged on' {
        $result = Test-AccountIsStale -LastLogonDate $null -AsOf $now
        $result | Should -Be $true
    }
}
```

Once `Disable-StaleAccounts` calls `Test-AccountIsStale` instead of comparing inline, the extraction is meant to preserve behavior. That's an intention, not a guarantee: the `$null` case above is exactly the kind of change PowerShell's type conversion and parameter binding can introduce. Run the characterization tests from the first step before and after the extraction. That's how you know it didn't change anything.

## Mock the boundary, not the logic

At some point you'll need to test something that calls an external system. The instinct is to mock heavily: mock everything, and make the test run in isolation. Resist it.

Mocks are useful at the boundary: the function that calls the API, writes the file, sends the notification. They're not useful inside your business logic, because they start hiding the very behavior you're trying to verify. A mock that always returns the same value doesn't tell you anything about how your code handles unexpected input.

The rule I use: mock at the layer that crosses a system boundary, test everything inside that layer with real data.

```powershell
Describe 'Get-StaleAccountReport' {
    BeforeAll {
        Mock Get-ADUser {
            return @(
                [pscustomobject]@{ SamAccountName = 'jsmith'; LastLogonDate = [datetime]'2024-02-01' }
                [pscustomobject]@{ SamAccountName = 'alee';   LastLogonDate = [datetime]'2024-05-22' }
            )
        }
    }

    It 'includes only accounts inactive beyond the threshold' {
        $report = Get-StaleAccountReport -ThresholdDays 90 -AsOf ([datetime]'2024-06-01')
        $report.Count | Should -Be 1
        $report[0].SamAccountName | Should -Be 'jsmith'
    }
}
```

`Get-ADUser` is mocked because it crosses a boundary (the domain). The filtering logic is real. If the filtering logic breaks, this test fails. The report takes `-AsOf` the same way `Test-AccountIsStale` does. If you've inherited a function that calls `Get-Date` itself and you can't change its signature yet, `Mock Get-Date` works as a stopgap, but move to a parameter when you can.

For a function with side effects, also assert what it did and didn't do. Checking return values isn't enough when the consequence is a disabled account:

```powershell
Describe 'Disable-StaleAccounts' {
    BeforeAll {
        Mock Get-ADUser {
            return @(
                [pscustomobject]@{ SamAccountName = 'jsmith'; LastLogonDate = [datetime]'2024-02-01' }
                [pscustomobject]@{ SamAccountName = 'alee';   LastLogonDate = [datetime]'2024-05-22' }
            )
        }
        Mock Set-ADUser {}
        Mock Write-Log {}
    }

    It 'disables the stale account and leaves the active one alone' {
        Disable-StaleAccounts -AsOf ([datetime]'2024-06-01')

        Should -Invoke Set-ADUser -Times 1 -Exactly -ParameterFilter { $Identity.SamAccountName -eq 'jsmith' }
        Should -Invoke Set-ADUser -Times 0 -Exactly -ParameterFilter { $Identity.SamAccountName -eq 'alee' }
    }
}
```

## Cover the failure paths

Production scripts fail. Networks time out, APIs return 429, files are locked. The most important tests to write aren't for the happy paths. They're for the failure paths, because that's where unattended automation becomes a problem.

For every external call, ask: what happens if this fails? If the answer is "the script crashes and nobody knows," that's where you need a test.

```powershell
Describe 'Invoke-GraphRequest' {
    It 'retries on a 429 response' {
        $script:callCount = 0
        Mock Invoke-RestMethod {
            $script:callCount++
            if ($script:callCount -lt 3) {
                # PowerShell 7's Invoke-RestMethod throws this, with the status code attached.
                $response = [System.Net.Http.HttpResponseMessage]::new([System.Net.HttpStatusCode]::TooManyRequests)
                throw [Microsoft.PowerShell.Commands.HttpResponseException]::new('Too Many Requests', $response)
            }
            return @{ value = @() }
        }
        Mock Start-Sleep {}   # don't actually wait between retries

        { Invoke-GraphRequest -Uri 'https://example.com/api' } | Should -Not -Throw
        $script:callCount | Should -Be 3
    }
}
```

That test validates that the retry logic actually runs. If someone removes the retry loop later, this test fails. That's the point.

Two details make it honest. The mock throws the exception type `Invoke-RestMethod` really throws, carrying a real 429 status. A generic exception whose message says "Too Many Requests" only models a 429 if your code decides by reading the message, and it shouldn't. And `Start-Sleep` is mocked so the test doesn't wait out real backoff delays.

Production retry logic needs more than this test shows: honor `Retry-After`, cap the number of attempts, back off exponentially with jitter, don't retry failures that won't go away (a 400 or 404), and surface the final error instead of swallowing it. Each of those deserves its own test. [Keel](/projects/keel/) is my worked example, including why a request that isn't safe to repeat needs a narrower rule.

## Make the tests part of the pipeline

Tests that only run locally aren't reliable. They get skipped when there's pressure to ship, and they drift as the code changes.

Once you have meaningful coverage, add a CI step. In GitHub Actions, running Pester takes about fifteen lines:

```yaml
- name: Install Pester
  shell: pwsh
  # Pin the version you've tested. -SkipPublisherCheck lets Pester 5
  # install alongside the Pester 3.4 that ships with Windows PowerShell.
  run: Install-Module Pester -RequiredVersion 5.7.1 -Scope CurrentUser -Force -SkipPublisherCheck

- name: Run Pester tests
  shell: pwsh
  run: |
    $config = New-PesterConfiguration
    $config.Run.Path = './tests'
    $config.TestResult.Enabled = $true
    $config.TestResult.OutputPath = 'test-results.xml'
    $config.Run.Exit = $true
    Invoke-Pester -Configuration $config
```

The install step matters. Windows PowerShell ships with Pester 3.4, `New-PesterConfiguration` needs Pester 5, and whatever else a hosted runner image includes can change without notice. Installing an exact version means a new Pester release can't change your results until you choose to upgrade. `-MinimumVersion` would let it. Publishing `test-results.xml` (as a build artifact, or through a test-report action) means a failure shows up with the failing test's name, not just a red X.

Set the branch protection rule to require the check to pass. Now the tests enforce themselves.

---

You won't have complete coverage after this. You're not trying to. You're trying to reach the point where you can make a specific change with confidence, and know within a few minutes if something broke.

That's what "testing comes before trust" actually means in practice. Not perfect coverage, but enough verified behavior that the next engineer (or future you) can move without fear.

Start with the thing most likely to cause a problem if it breaks. Extract it so it's testable. Write the obvious cases plus the failure path. Add CI. Then change what you came to change.
