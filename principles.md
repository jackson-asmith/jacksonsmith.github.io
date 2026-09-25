---
title: Engineering Principles
description: The six principles behind how Jackson Smith designs, automates, and modernizes systems — and where each one shows up in real work.
permalink: /principles/
---

# How I approach engineering

I want the infrastructure I build to be invisible when it works and recoverable when it breaks. I don't chase hype. I try to build systems that last, and I mentor, document, and automate so that others can pick up where I left off.

These principles came out of a decade of running production systems. Each one links to work where I applied it.

## 1. Reliability is a feature

> Systems shouldn't need heroics to operate.

If a system only stays up because one engineer knows its quirks, it isn't reliable. I design for components failing and for recovery that any engineer on the team can carry out.

**In practice:** eliminating single points of failure, graceful failure and recovery, alerting tied to meaningful service levels, and validating disaster recovery instead of assuming it works.

**Where it shows up:** a three-node SQL availability group that removed a single point of failure (99.99% uptime, sub-15-minute RTO); disaster-recovery validation twice a year for core line-of-business applications; SLI/SLO-based alerting that cut unplanned downtime by 35%. ([Experience](/experience/))

## 2. Automation must reduce risk, not create it

> Automating a bad process just produces bad outcomes faster.

Removing manual steps doesn't count as success on its own. Good automation is more repeatable, more visible, and more secure than the process it replaced, and it's safe to run unattended. Security is part of the job, not someone else's review step.

**In practice:** validating input before acting, bounded retries with backoff, structured logs that leave out sensitive data, failure states that tell you what to do next, and keeping a human in the loop for consequential decisions.

**Where it shows up:** API orchestration across GitHub Enterprise, Entra ID, and Microsoft Graph with rate-limit handling, exponential backoff, and structured event logging; input validation and hardening on critical workflows; a patching pipeline that reduced vulnerability exposure by 70%. ([Experience](/experience/))

## 3. Modernize incrementally

> Improve what exists first. Rewrite only when the evidence supports it.

A rewrite isn't automatically the responsible choice. I weigh technical improvement against production risk, how much change the team can absorb, and the value delivered at each step.

**In practice:** assess the current state first, tackle the highest-risk dependencies early, introduce seams that make existing code testable, and deliver changes in stages that can each be verified independently.

**Where it shows up:** a phased modularization plan that extracts notification and directory-lookup logic *before* touching destructive workflows, so each extraction is unit-testable and has no production side effects; platform upgrades completed 18–24 months ahead of end-of-life deadlines. ([Experience](/experience/))

## 4. Governance should enable engineers

> Good governance removes ambiguity without slowing delivery down.

Standards and guardrails should reduce the number of decisions each engineer has to make from scratch, without adding approval bottlenecks. The compliant path should be the easiest one.

**In practice:** clear ownership, minimum standards encoded in templates, tests, CI, and repository configuration, self-service for common needs, and dropping controls that add friction without reducing risk.

**Where it shows up:** a GitHub Copilot custom-instructions file that encodes the team's PowerShell style guide so common anti-patterns are caught before review; automated Copilot budget governance through the GitHub billing API. ([Experience](/experience/))

## 5. Testing comes before trust

> Confidence should come from evidence, not familiarity.

Code isn't correct just because it's been running for a long time. Until its important behavior is verified, I treat it as unproven, and that applies equally to AI-generated code.

**In practice:** characterization tests before refactoring, separating side effects from decision logic, testing failure paths as well as success paths, and CI that catches regressions on every push.

**Where it shows up:** the first Pester unit-test suite and shared test infrastructure for an existing codebase, with CI running on every push and pull request. Refactoring behind those tests turned up a latent production bug. ([Experience](/experience/))

## 6. Documentation is engineering work

> If the next engineer can't understand or operate the system, the implementation isn't finished.

Documentation is part of a system's operational interface, so it's maintained alongside the code instead of written after the fact.

**In practice:** recording purpose, assumptions, and ownership; runbooks for operations and recovery; recording design decisions and the tradeoffs behind them; and handoffs that don't rely on knowledge that lives in one person's head.

**Where it shows up:** organization-wide documentation and handover standards, consolidated into one place; clean handoffs of identity automation and certificate lifecycle management to other teams; documentation for shared helpers and the test system. ([Experience](/experience/))

---

Principles are easy to state and harder to demonstrate. The [projects](/projects/) section walks through specific decisions: what the constraints were, which options I considered, and which of these principles shaped the outcome.
