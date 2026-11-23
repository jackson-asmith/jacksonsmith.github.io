---
title: "Checks that parsed their own evidence"
image: /assets/img/social/post-checks-evidence.png
description: Using an LLM code review to surface a real architectural flaw in gh-baseline — and knowing which ten percent of the review was right.
date: 2026-11-17
principles: [Automation must reduce risk, Testing comes before trust]
---

You read a post about LLM slop, and your first thought is "wait, does that include my code?"

A few weeks ago I read Boris Tane's post on slop creep — the quiet enshittification of software by LLMs producing fluent mediocrity that gets accepted because it's hard to distinguish from competent work. I'd been building a tool partly with LLM assistance, and his framing made me curious: could another LLM usefully critique an LLM-assisted codebase? So I asked GitHub Copilot to act as a senior engineer and review the architecture.

The result was about what you'd expect — and more useful than I expected.

gh-baseline is a gh extension for auditing GitHub repository security baselines. Its core design is a collect-then-evaluate pipeline: GitHub API calls produce a snapshot, and a set of pure functions evaluate the snapshot against a policy. The boundary keeps checks fast, testable, and reproducible without network access.

Copilot's review flagged ten items across P0, P1, and P2. It opened with a disclaimer: direct retrieval of the source tree was blocked, so confidence was high in architectural recommendations and medium in implementation-level observations. That honesty mattered.

The P0 items — strict unknown handling, schema versioning, hardened redirect handling — were largely already done. `--fail-on-unknown` existed. Schema versioning was at v3. The redirect protection was in place. Copilot couldn't see the code, so it reasonably flagged the things any thoughtful reviewer would flag for a tool at this stage. That's not a failure of the review; it's just the information it had.

The package restructure recommendation was wrong. Copilot suggested splitting into eight packages: `internal/collector`, `internal/finding`, `internal/report`, `internal/exitpolicy`, and so on. For a tool with five real users and one maintainer, that's premature architecture — the kind of structure you grow into once the seams actually hurt, not something you impose to satisfy a diagram. I filed it as "revisit at scale" and moved on.

But one item was genuinely worth acting on.

The review flagged the workflow inspection boundary as the weakest part of the architecture. Workflow checks were being run against raw YAML strings stored in the snapshot — the checks were parsing their own evidence at evaluation time, every time, including during offline re-evaluation with `--snapshot`. That meant a workflow YAML change between collection and evaluation would produce different results. The effective check inputs weren't stable.

I'd been aware of this vaguely. Seeing it written out clearly — "checks parse at evaluation time, not at collection time" — was enough to make it the actual problem rather than a known rough edge.

The fix: parse each workflow's YAML at collection time and store the structured domain facts in the snapshot. Triggers, top-level permissions, referenced actions, secrets. The snapshot then captures what was true when it was collected. Offline re-evaluation uses those facts, not a re-parse of the original YAML. The check functions become table lookups against structured data rather than parsers embedded in policy logic.

This became `WorkflowEvidence` in the snapshot schema. The collector runs `workflowparse` once per file and stores the result. Checks consume `w.Evidence.Actions`, `w.Evidence.Permissions`, `w.Evidence.Triggers`. The boundary between collection and evaluation, which is the core design of the tool, got meaningful for workflows for the first time.

It also unlocked two new checks in the same release cycle: `workflow.token-permissions-scope`, which catches `permissions: write-all` (declared permissions, but not least-privilege), and `workflow.reusable-callee-pinned`, which catches reusable workflow calls not pinned to a commit SHA — a supply-chain risk identical to unpinned actions, just at a different layer.

The slop creep post is about the danger of accepting LLM output uncritically — of the fluency becoming a substitute for the judgment that should follow it. The antidote isn't refusing to use LLMs; it's applying the domain knowledge the LLM explicitly said it lacked.

Copilot told me upfront it couldn't read the source. That meant every implementation-level observation needed to be checked against reality. Several P0 items were already done — not because the review was wrong, but because I had context it didn't. The package restructure was the wrong call at this scale — not because the structure was bad in principle, but because I knew where the actual friction was. And the workflow inspection boundary was real — not because I hadn't thought about it, but because having it written as a crisp diagnosis made it easier to act on.

The value wasn't in the review. It was in having enough context to know which ten percent of the review was right.

gh-baseline is at [github.com/jackson-asmith/gh-baseline](https://github.com/jackson-asmith/gh-baseline). The `WorkflowEvidence` change landed in v0.8.0.
