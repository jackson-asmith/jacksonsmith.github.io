---
title: "Testing automation you didn't write"
description: A practical approach to adding Pester tests to an existing PowerShell script — before you touch a single line of logic.
date: 2026-10-27
principles: [Testing comes before trust, Automation must reduce risk, Modernize incrementally]
---

Somebody hands you a PowerShell script. It's been running in production for two years. Nobody knows exactly what it does in every case, but it works, and people depend on it. Your job is to change it.

This is the situation Pester tutorials don't cover. They show you how to test code you're writing from scratch, with clean inputs and predictable outputs. They don't show you how to build confidence in 400 lines of inherited automation that mixes business logic with API calls and writes to the filesystem in the same function.

Here's how I approach it.

## Start with characterization, not coverage

Before writing a single test, get clear on what you're actually trying to achieve. You're not aiming for 80% coverage. You're trying to make it safe to change something.

That means identifying the behavior that, if it broke, would cause a real problem: the thing that fires a notification, modifies an account, or deletes a record. Everything else is secondary.

A characterization test captures what the code *does* before you fully understand why. You run it, observe the output, and write a test that asserts exactly that output. You're not validating that the behavior is correct — you're creating a regression wire. If your change alters the behavior, the test will tell you.

```powershell
Describe 'Get-UserStatus' {
    BeforeAll {
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

## Find the seams

Most inherited scripts fail the same way: side effects are everywhere. An API call happens in the middle of a decision. A file write is buried inside a transformation. There's no clean boundary between "figure out what to do" and "do it."

You can't easily test code in that shape. But you don't have to rewrite it to make it testable — you need to find the seams.

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

The staleness check is untestable here — it's tangled with the AD query and the mutation. Extract it:

```powershell
function Test-AccountIsStale {
    param(
        [datetime]$LastLogonDate,
        [int]$ThresholdDays = 90,
        [datetime]$AsOf = (Get-Date)
    )
    return $LastLogonDate -lt $AsOf.AddDays(-$ThresholdDays)
}
```

Now `Test-AccountIsStale` has no external dependencies. It takes data and returns a boolean. The `$AsOf` parameter is worth calling out: without it, `Get-Date` is an implicit dependency and tests near the exact threshold boundary will be flaky. Injecting the reference date keeps the function pure and the threshold edge cases reliable. You can test every scenario — accounts inactive for 91 days, accounts active yesterday, accounts that have never logged on — without touching Active Directory or a mock.

```powershell
Describe 'Test-AccountIsStale' {
    BeforeAll {
        $now = [datetime]'2024-06-01'
    }

    It 'returns true for an account inactive for 91 days' {
        $result = Test-AccountIsStale -LastLogonDate $now.AddDays(-91) -AsOf $now
        $result | Should -Be $true
    }

    It 'returns false for an account active yesterday' {
        $result = Test-AccountIsStale -LastLogonDate $now.AddDays(-1) -AsOf $now
        $result | Should -Be $false
    }

    It 'returns true for an account that has never logged on' {
        $result = Test-AccountIsStale -LastLogonDate ([datetime]::MinValue) -AsOf $now
        $result | Should -Be $true
    }
}
```

You haven't changed the behavior of `Disable-StaleAccounts`. You've extracted a piece of it that you can now verify.

## Mock the boundary, not the logic

At some point you'll need to test something that calls an external system. The instinct is to mock heavily — mock everything, make the test run in isolation. Resist it.

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
        Mock Get-Date { return [datetime]'2024-06-01' }
    }

    It 'includes only accounts inactive beyond the threshold' {
        $report = Get-StaleAccountReport -ThresholdDays 90
        $report.Count | Should -Be 1
        $report[0].SamAccountName | Should -Be 'jsmith'
    }
}
```

`Get-ADUser` is mocked because it crosses a boundary (the domain). The filtering logic is real. If the filtering logic breaks, this test fails.

## Cover the failure paths

Production scripts fail. Networks time out, APIs return 429, files are locked. The most important tests to write aren't the happy paths — it's the failure paths, because that's where unattended automation becomes a problem.

For every external call, ask: what happens if this fails? If the answer is "the script crashes and nobody knows," that's where you need a test.

```powershell
Describe 'Invoke-GraphRequest' {
    It 'retries on a 429 response' {
        $script:callCount = 0
        Mock Invoke-RestMethod {
            $script:callCount++
            if ($script:callCount -lt 3) {
                throw [System.Net.WebException]::new('Too Many Requests')
            }
            return @{ value = @() }
        }

        { Invoke-GraphRequest -Uri 'https://example.com/api' } | Should -Not -Throw
        $script:callCount | Should -Be 3
    }
}
```

That test validates that the retry logic actually runs. If someone removes the retry loop later, this test fails. That's the point.

## Make the tests part of the pipeline

Tests that only run locally aren't reliable. They get skipped when there's pressure to ship, and they drift as the code changes.

Once you have meaningful coverage, add a CI step. In GitHub Actions, running Pester takes about fifteen lines:

```yaml
- name: Install Pester
  shell: pwsh
  run: Install-Module Pester -Force -MinimumVersion 5.0

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

The install step matters: Windows runners ship with Pester 3.x, and `New-PesterConfiguration` is Pester 5+. Without it, the old version runs silently and nothing gets tested.

Set the branch protection rule to require the check to pass. Now the tests enforce themselves.

---

You won't have complete coverage after this. You're not trying to. You're trying to reach the point where you can make a specific change with confidence, and know within a few minutes if something broke.

That's what "testing comes before trust" actually means in practice — not perfect coverage, but enough verified behavior that the next engineer (or future you) can move without fear.

Start with the thing most likely to cause a problem if it breaks. Extract it so it's testable. Write the obvious cases plus the failure path. Add CI. Then change what you came to change.
