---
title: "Running GitHub's Actions egress firewall on a small Go project"
description: What I learned putting gh-baseline's CI behind GitHub's native egress firewall in enforce mode, from a one-host allow list to a passing test that proved nothing.
date: 2026-11-10
principles: [Testing comes before trust, Automation must reduce risk]
---

GitHub's native egress firewall for Actions now runs gh-baseline's CI in enforce mode. The allow list is one host, `proxy.golang.org`, on top of GitHub's own endpoints. Getting there taught me three things:

- **Log mode first, and the log is short.** A typical Go CI job contacts far fewer hosts than you'd guess.
- **A passing enforce run can prove nothing.** My first one passed because the Go module cache meant the blocked host was never contacted.
- **Blocks don't announce themselves.** The failing step said `server misbehaving`, and only the run artifact said the firewall did it.

The runtime cost was small: 13–23 seconds per run against a 19-second median without the firewall. Everything here is technical-preview behavior and may change.

## The project

[gh-baseline](https://github.com/jackson-asmith/gh-baseline) is a small Go `gh` extension that audits GitHub repositories against a declared security baseline. Its CI is one job of about 20 seconds: checkout, `setup-go`, `gofmt`, `go vet`, `go test -race`, and a smoke test of the built binary. It has one third-party dependency, `gopkg.in/yaml.v3`.

The security gain here is modest. CI has no secrets, its token is read-only, and all three actions are pinned to commit SHAs. I tried the firewall anyway: to see what CI actually talks to, and because a tool about checking your assumptions should check its own.

GitHub-hosted runners normally reach any host on the internet. The [firewall](https://github.com/github-early-access/actions-native-egress-firewall) sits outside the runner VM, logs DNS and HTTP(S) traffic, and in `enforce` mode blocks hosts not on an allow list.

## Setup: one label, one file

The firewall is opt-in per job. On standard GitHub-hosted runners you change the runner label; no admin setup is needed. Linux is the only platform in the preview.

```yaml
jobs:
  test:
    runs-on: ubuntu-24.04-firewall
```

The policy lives in `.github/egress-firewall.yaml`, directly under `.github/`, not in `.github/workflows/`. One file covers every firewall job in the repository.

```yaml
mode: log        # or: enforce
allow:
  - proxy.golang.org
```

GitHub's own endpoints are allowed by default: `github.com`, `codeload.github.com`, and the Actions and storage hosts from the `/meta` API.

Two details are easy to miss:

- **The job needs `contents: read`** so the firewall can read the policy. Without it, no policy is enforced and nothing warns you.
- **The policy is read from the run's own ref.** A tag gets the policy that existed when it was cut.

## Log mode: what CI actually contacts

One log-mode run was enough to build the allow list: every host but one was a GitHub default. The firewall writes a `firewall-decisions-*` artifact with one JSON entry per request, including the host, the URL, the process that made it and the response status.

| Host | Made by | Requests | Allowed by default |
| --- | --- | --- | --- |
| `*.actions.githubusercontent.com` (results, broker, job control) | the runner | 44 | yes |
| `productionresultssa*.blob.core.windows.net` | the runner, and `setup-go`'s cache | 12 | yes |
| `github.com` | `git` (checkout) | 3 | yes |
| `codeload.github.com` | downloading `actions/setup-go` | 2 | yes |
| **`proxy.golang.org`** | **`go`, fetching `yaml.v3`** | **3** | **no** |

A few things weren't there that I expected. CI never contacted `sum.golang.org`, because `go.sum` already pins the checksums. It made no HTTP requests to `api.github.com`; the runner only looked it up in DNS. And there was no Go toolchain download: `setup-go` found Go 1.24.13 preinstalled on the image.

## Testing enforce: the cache trap

To trust an allow list, I wanted to see it block something. So I switched to `enforce` and deliberately left `proxy.golang.org` off. CI passed.

That looked like the policy wasn't loaded. It wasn't the firewall's fault: `setup-go` had restored the Go module cache, `yaml.v3` included, from the Actions cache. Nothing ever asked for the blocked host, so the run would have passed with or without a working policy.

The fix was a temporary step that empties the module cache and downloads again, forcing a request to the proxy:

```yaml
- run: go clean -modcache && go mod download -x
```

| Run | Policy | Result | What it showed |
| --- | --- | --- | --- |
| 1 | `log` | passed | the one non-default host: `proxy.golang.org` |
| 2 | `enforce`, proxy left off | passed | nothing: modules came from the cache |
| 3 | `enforce`, proxy left off, forced download | **failed** | the policy is enforced: `DNS BLOCKED`, reason `NotInAllowList` |
| 4 | `enforce`, proxy allowed, forced download | passed | the allow list works: `yaml.v3` fetched with HTTP 200 |

The cache also matters day to day. Most runs never contact the proxy, so a log from a cached run would miss it entirely. It still belongs on the list: the first run after a dependency change, or a cache eviction, needs it.

## Diagnosing a block: read the artifact

When the firewall blocked the proxy, the job log didn't mention it. `go` reported a DNS failure:

```text
dial tcp: lookup proxy.golang.org on 127.0.0.53:53: server misbehaving
```

The only annotation on the job was "Process completed with exit code 1." Without knowing the firewall was there, this reads like flaky DNS on the runner.

The artifact was the only place that said what happened: five `DNS BLOCKED` entries for `proxy.golang.org`, reason `NotInAllowList`. It also showed packets to `ntp.ubuntu.com` blocked, the runner's own clock sync, with no effect on the job.

Log mode doesn't help you predict blocks either. Every entry in my log-mode run had `wouldBlock: false`, including `proxy.golang.org`, which enforce mode later blocked. So build the allow list from the hosts in the log, not from that field.

I now keep a comment in the policy file: a DNS or connection error in CI means check the `firewall-decisions-*` artifact first.

## Cost: barely measurable

After the first run, firewall runs took 13–23 seconds, no slower than without the firewall.

| Runs | CI job time |
| --- | --- |
| Without the firewall (5 runs on main) | 15–48 s, median 19 s |
| With the firewall, first run | 57 s |
| With the firewall, next 4 completed runs | 13–23 s |

The one slow firewall run was the first, which started with an empty Go module cache and saved a new one. I've left out the deliberately failing test run, which stopped after its third step. Ten runs is a small sample, but nothing here suggests GitHub's warning of a 15–20% slowdown matters for a job this short.

## If you try it

1. **Start in `log` mode** and read the artifact, not just the run summary. Build the allow list from the hosts listed there.
2. **Defeat your caches before trusting the list.** Clear the module or package cache in a temporary step, so the run actually has to reach every host it might need.
3. **Prove enforcement both ways.** Leave a needed host off and watch the run fail; add it back and watch it pass. A green enforce run on its own proves nothing.
4. **Write down how to diagnose a block,** because the error won't say. A DNS or connection error in CI means check the artifact first.
5. **Expect the list to grow** when your toolchain changes. My likely next addition is the Go download host, the first time `go.mod` needs a Go version the runner image doesn't have.

Is it worth it on a project this small? For CI with no secrets and a read-only token, the protection is modest. Even in enforce mode, `github.com` stays allowed, so a malicious step could still send data to a GitHub repository it controls. What I got was visibility. I now know CI contacts exactly one host outside GitHub, and that will change only when a dependency does. That was worth one afternoon and a three-line policy.

The job that would really benefit is a release job, whose token can write releases. I'll move gh-baseline's release job behind the firewall once it leaves technical preview.

## Caveats and sources

This is one small Go project on standard Linux runners, tested on November 10, 2026, during the technical preview. GitHub says the policy format, file location and APIs may change before public preview. The timing figures come from ten runs, five with the firewall and five without.

- [Actions native egress firewall: early access](https://github.com/github-early-access/actions-native-egress-firewall), GitHub's preview documentation
- [What's coming to our GitHub Actions 2026 security roadmap](https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/), GitHub blog, March 2026
- [Disrupting supply chain attacks on npm and GitHub Actions](https://github.blog/security/supply-chain-security/disrupting-supply-chain-attacks-on-npm-and-github-actions/), GitHub blog, July 2026
- [gh-baseline PR #23](https://github.com/jackson-asmith/gh-baseline/pull/23): the policy, the test runs, and their artifacts
