---
description: Jackson Smith is a software engineer who spent a decade operating production infrastructure and now builds reliable automation, testable code, and systems that don't page someone at 3am.
---

<img class="avatar-hero" src="/assets/img/avatar-240.webp" width="120" height="120" fetchpriority="high" alt="Jackson Smith">

# Hi, I'm Jackson

I'm a software engineer in Philadelphia. Before moving into software, I spent ten years running production infrastructure, and that experience shaped how I write code, because I think about failure modes first, like what happens when the API throttles, a retry sends a duplicate, or nobody is watching at 3am. I care about correctness, testability, and systems that run without me.

This site is where I write up how I work: the principles I go by, the projects behind them, and what I'd do differently next time. If you're hiring, [experience](/experience/) has my career history and skills.

I'm always happy to talk shop, or to help if you're earlier in your career. [Email me](mailto:jackson@jacksonasmith.com) or find me on [LinkedIn](https://www.linkedin.com/in/jackson-a-smith/).

## Impact

<ul class="impact">
  <li><strong>8 SDKs</strong><span>my retry-safety fix, <a href="/writing/2026/one-retry-fix-eight-sdks/">merged into Microsoft’s Kiota</a> in every language</span></li>
  <li><strong>24 scripts</strong><span>(47 call sites) now running on the internal standard library I built for my team</span></li>
  <li><strong>$400K+</strong><span>annual outsourcing cost eliminated, and 70% less vulnerability exposure, through automated patching</span></li>
  <li><strong>40–60% → 99.99%</strong><span>availability on a 1,200-server platform our ops team stabilized</span></li>
</ul>

Context for each number is on the [experience](/experience/) page.

## Principles I work by

1. [Reliability is a feature](/principles/#1-reliability-is-a-feature)
2. [Automation must reduce risk, not create it](/principles/#2-automation-must-reduce-risk-not-create-it)
3. [Modernize incrementally](/principles/#3-modernize-incrementally)
4. [Governance should enable engineers](/principles/#4-governance-should-enable-engineers)
5. [Testing comes before trust](/principles/#5-testing-comes-before-trust)
6. [Documentation is engineering work](/principles/#6-documentation-is-engineering-work)

## Current focus

I'm most interested in internal platforms, developer tooling, and reliability engineering.

* Bringing test coverage and CI quality gates to existing codebases
* Reliable, unattended API integrations with Microsoft Graph, GitHub, and identity platforms
* GitHub Enterprise governance and developer experience that doesn't slow teams down
* AI-assisted development with explicit research, planning, and review checkpoints
* Observability and reliability engineering

## Selected work

* [gh-baseline](/projects/gh-baseline/) is a read-only `gh` extension that audits GitHub repositories against a tiered security baseline. I built it in Go after auditing my own repositories by hand.
* [Keel](/projects/keel/) is a pair of PowerShell modules for unattended automation, CI-tested on Windows PowerShell 5.1 and PowerShell 7. It retries HTTP calls within limits, and its Graph-first mail won't resend after an ambiguous failure.
* The [email alignment checker](/projects/email-alignment-checker/) is a scheduled GitHub Actions workflow that monitors this domain's SPF, DKIM, and DMARC records.

[All projects and case studies →](/projects/)

Outside of work you'll find me skiing, cooking, on a yoga mat, or suffering through another Ferrari strategy call.
