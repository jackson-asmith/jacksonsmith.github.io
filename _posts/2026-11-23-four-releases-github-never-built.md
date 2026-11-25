---
title: "Four releases GitHub never built"
image: /assets/img/social/post-four-releases.png
description: Four gh-baseline tags never got releases, and nothing failed, because nothing ran. Why GitHub skipped them, why the obvious fix was blocked, and the release-workflow change that filled the gap without touching a tag.
date: 2026-11-23
principles: [Automation must reduce risk, Testing comes before trust]
---

[gh-baseline](/projects/gh-baseline/)'s Releases page went from v0.6.2 straight to v0.11.0. The tags for v0.7.0 through v0.10.0 existed, and the changelog described all four. None of them had a release, and none had binaries. Anyone who tried to install one of those versions got source code and nothing to run.

Nothing had failed. There was no red run in the Actions tab, because there was no run at all. Nothing in CI could have noticed, because nothing ran.

## Why the release workflow never ran

gh-baseline's release workflow runs when a `v*` tag is pushed. It builds binaries for 12 platforms, attaches them to a GitHub release, then installs the release on Linux, macOS, and Windows and runs a smoke test.

GitHub's [documentation for the push event](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#push) has a note I'd never read: when more than three tags are pushed at once, GitHub doesn't create events for them. No event, no workflow. The four tags went up together, so none of them started a release. v0.11.0 went up on its own and released normally.

Installing was never broken. `gh extension install` takes the latest release, and that was v0.11.0. The gap only hurt someone who wanted a specific older version, which is the kind of problem nobody reports.

## The obvious fix was blocked, and it should have been

The usual advice is to delete the tag and push it again, so GitHub sees a new push:

```bash
git push origin :refs/tags/v0.7.0 && git push origin refs/tags/v0.7.0
```

GitHub refused:

```text
remote: error: GH013: Repository rule violations found for refs/tags/v0.7.0.
remote: - Cannot delete this tag
```

The repository has a ruleset that stops tags from being deleted. A release tag should point at the same commit forever, so anyone who pinned to it gets what they pinned. That's the same kind of protection gh-baseline audits branches for, and loosening it to fix a cosmetic gap would have been the wrong trade. The fix had to work with the ruleset, not around it.

## Building a release from a tag that already exists

The workflow uses [`cli/gh-extension-precompile`](https://github.com/cli/gh-extension-precompile), which normally takes the release tag from the push that triggered it. It also accepts a `release_tag` input. So the workflow gained a manual trigger with a `tag` input, and a first job that decides what to build:

- The input must look like a version (`v1.2.3`). It's passed through an environment variable, not pasted into the script, so a strange value can't become a command.
- The tag must already exist. A manual run can't create one.
- The tag must not already have a release. The action re-uploads over an existing release's binaries, and a backfill should never be able to replace binaries people have already downloaded.

Then the build and the smoke tests check out that tag's own code. An older version gets tested against its own test fixture, not today's.

## Who becomes "Latest"

Creating a release for an older version raised a question I hadn't considered: which release is "Latest" afterwards? It matters, because Latest is what `gh extension install` installs.

The release action creates releases without saying. GitHub's REST API documents new releases as becoming Latest by default. The `gh` CLI describes its default as automatic, based on date and version. Those don't obviously agree, and the place to find out which one wins isn't the install path for everyone using the tool.

So a manual run ends with one more job: it finds the highest released version and marks it Latest. It runs even if a smoke test fails, as long as a release was created. That doesn’t remove a release whose binaries fail a smoke test; it only makes sure a failed backfill can’t leave an older version as Latest.

## The result

Four manual runs, one tag at a time. Each passed all six jobs: resolving the tag, building, a smoke test on each of three operating systems, and restoring Latest. Each release has its 12 binaries, and v0.11.0 was still Latest after each run completed.

The validation got its first real test the same afternoon. A run was started with the tag `vX.Y.Z`, a placeholder I'd written in an example command and that got pasted as-is. The first job rejected it, and nothing after it ran.

## What I'd take from it

- **Push tags one at a time.** `git push origin v0.12.0`, not `git push --tags` after tagging several versions.
- **A workflow that never ran doesn't look like a failure.** Nothing turned red. The gap was visible only by comparing what should exist, a release for every tag, with what did. That's the same lesson as treating "I couldn't check" as its own outcome instead of a pass.
- **When a protection blocks your fix, check the fix before the protection.** The tag ruleset was right. The better fix didn't need to break it.

The workflow change and its reasoning are in [gh-baseline PR #38](https://github.com/jackson-asmith/gh-baseline/pull/38) and an amendment to [ADR 0003](https://github.com/jackson-asmith/gh-baseline/blob/main/docs/adr/0003-precompiled-releases.md).
