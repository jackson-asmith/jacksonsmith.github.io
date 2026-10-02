---
title: Projects
description: Case studies and open-source work by Jackson Smith — the problem, the constraints, the decision, and the lessons.
permalink: /projects/
---

# Projects

Each case study follows the same structure: the problem, the existing state, the constraints, the options considered, the decision, the safeguards, the outcome, and what I'd change next time. Employer work is generalized; code shown is public or recreated from scratch.

## Case studies

{% assign studies = site.projects | sort: "order" %}
{% if studies.size > 0 %}
{% for study in studies %}

* [**{{ study.title }}**]({{ study.url | relative_url }}) — {{ study.summary }}{% if study.principles %} <span class="tags">({{ study.principles | join: ", " }})</span>{% endif %}

{% endfor %}
{% else %}
The first case studies are being written. In the meantime, the [experience](/experience/) page has summaries of the major projects.
{% endif %}

## Open source

* [**Keel**](https://github.com/jackson-asmith/keel) — PowerShell modules for unattended automation, CI-tested on Windows PowerShell 5.1 and PowerShell 7: bounded HTTP retries and Graph-first mail that won't resend after an ambiguous failure.
* [**Email alignment checker**](https://github.com/jackson-asmith/email-alignment-checker) — scheduled GitHub Actions workflow that monitors SPF, DKIM, and DMARC for this domain and commits only when something actually changes.
* [**LinuxConfig**](https://github.com/jackson-asmith/LinuxConfig) — modular Bash pipeline that bootstraps RHEL hosts into Active Directory and Red Hat Satellite, with dry-run mode on every stage and bats + ShellCheck in CI.
* [**adaptive-comm-tool**](https://github.com/jackson-asmith/adaptive-comm-tool) — Python CLI that uses Claude to score and rewrite a message for each teammate persona, with output validated against a schema so no persona is invented or dropped.
