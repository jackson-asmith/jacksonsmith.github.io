---
title: Writing
description: Technical writing by Jackson Smith on automation, testing, PowerShell, GitHub governance, and reliability engineering.
permalink: /writing/
---

# Writing

{% if site.posts.size > 0 %}
{% for post in site.posts %}

* [**{{ post.title }}**]({{ post.url | relative_url }}) — <span class="tags">{{ post.date | date: "%B %Y" }}</span>{% if post.description %}<br>{{ post.description }}{% endif %}

{% endfor %}
{% else %}
Articles on PowerShell module design, testing existing automation with Pester, reliable unattended automation, and GitHub governance are on the way.
{% endif %}
