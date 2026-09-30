---
title: Experience
description: Ten-plus years across software, platform, and infrastructure engineering — roles, projects, and technical skills.
permalink: /experience/
---

# Experience

Want a copy of my résumé or a quick chat? [Email me](mailto:jackson@jacksonasmith.com) or connect on [LinkedIn](https://www.linkedin.com/in/jackson-a-smith/).

## Key Projects & Initiatives

* **FinOps & BI Engineering**: Designed end-to-end BI solution for GitHub Enterprise billing — ETL pipeline consuming the GitHub REST API (built in PowerShell, then re-platformed to Python for the data team), star schema semantic model, and DAX measures powering Power BI dashboards for cost visibility. Paired with automated GitHub Copilot budget governance (per-user overrides, cost center management) via the billing API.

* **High Availability Architecture**: Part of the operations team that removed the single point of failure in core SQL infrastructure with a three-node availability group (sub-15-minute RTO), one piece of taking the platform from 40–60% to 99.99% availability.

* **Legacy Infrastructure Modernization**: Led strategic refactoring of critical systems (internal DNS, certificate lifecycle, syslog normalization) reducing operational escalations by 50% over 12 months through systematic reliability improvements and automation.

* **Security Engineering**: Partnered with InfoSec as a trusted technical contributor across Zero Trust network deployment (Zscaler), certificate authority migration (Entrust → DigiCert with Azure KeyVault automation), PKI lifecycle management, and major security incident response.

## Roles

### Software Engineer | Public Consulting Group; Remote -- March 2026–Present

#### Systems Integration & Analytics

* Designed end-to-end BI solution for GitHub Enterprise billing: GitHub REST API ingestion, star schema semantic model, and DAX measures powering curated Power BI dashboards for cost visibility and budget governance.
* Re-platformed the ETL pipeline from PowerShell to Python so the data team could read, maintain, and extend it in their own stack.
* Built orchestration workflows connecting GitHub Enterprise and Entra ID REST APIs, implementing rate-limit handling, exponential backoff retry logic, and structured event logging for reliable unattended execution.
* Automated GitHub Copilot cost governance via the GitHub billing API, including per-user budget overrides and cost center management.

#### Testing & Code Quality

* Established foundational Pester unit test suite and reusable shared test infrastructure for an existing codebase, creating automated quality gates where none previously existed.
* Configured CI pipeline executing Pester tests on push and pull request events, enforcing code quality standards across the development workflow from day one.
* Authored a GitHub Copilot custom-instructions file codifying a team PowerShell style guide and Microsoft's recommended development practices, substantially reducing recurring AI-generated anti-patterns (e.g., non-idiomatic `return $var` usage) across the team's codebase before code reaches review.
* Adopted a structured AI-assisted development workflow — documenting research findings and implementation plans before generating code, with explicit review checkpoints to correct assumptions and scope — keeping architectural control over AI-authored changes rather than accepting output wholesale.

#### Platform Reliability & Modernization

* Centralized shared mail delivery on the Microsoft Graph API, migrating email delivery away from legacy SMTP dependencies.
* Implemented targeted input validation and hardening on critical workflows, reducing attack surface and improving operational resilience of production systems.

#### Architecture & Modernization Strategy

* Conducted architectural assessment of existing codebase, identifying strengths, gaps, and a prioritized improvement roadmap — balancing modernization velocity against production risk.
* Planned and began a phased modularization strategy: extracting notification and directory lookup logic from monolithic orchestration scripts before touching destructive workflows, ensuring each extraction is independently unit-testable and carries no production side effects.
* Built the team's internal PowerShell standard library of core, modular functions for automation shared across four engineers, now used in 24 production scripts (47 call sites) in its first repository, with shared test infrastructure and CI.
* Identified and fixed a latent production bug in a directory lookup, surfaced by the new test suite during refactoring.

#### Documentation

* Authored focused documentation for shared function helpers and the test system, improving developer onboarding and long-term maintainability.

### Operations Engineer | Lincoln Investment; Remote -- April 2022–January 2026

Core member of the operations team that took a 1,200-server hybrid Azure/VMware platform (900 Linux, 300 Windows) from frequent outages (40–60% availability) to 99.99%, serving 3,500 users across 300+ offices.

#### What I owned

* **Monitoring:** designed and ran the observability platform (New Relic, Zabbix) with SLI/SLO-based alerting, cutting unplanned downtime 35% and catching failures before users did.
* **Automation:** owned OS and infrastructure deployment automation and the team's GitHub repository. Built the Satellite/SCCM patching pipeline that reduced monthly vulnerability exposure 70% and eliminated $400K/yr in outsourced patching.
* **Three virtualized datacenters:** ran day-to-day operations and led the vSphere 6.5 → 8.0.3 upgrade, improving resource efficiency 30%.
* **Legacy systems:** refactored internal DNS, certificate lifecycle, and syslog normalization, cutting operational escalations 50% over 12 months.
* **Integrations:** built unattended workflows across CrowdStrike, Microsoft Graph, and Atlassian REST APIs with retry logic and structured logging.

#### How we got there (team efforts where I was a core contributor)

* Removed the SQL single point of failure with a three-node availability group (sub-15-minute RTO).
* Rebuilt backup on NetBackup with Azure archive tier, improving RTO from 24 hours to 4; ran biannual DR validation for line-of-business apps.
* Migrated workloads to Server 2022 and RHEL 8/9 18 months ahead of end of life.
* Federated identity across 20+ M365/Entra ID tenants from a single on-prem AD source.
* Moved the certificate authority from Entrust to DigiCert in six months, with Azure Key Vault automating renewals.

#### Also

* Helped manage our Azure environment.
* Partnered with InfoSec on the Zscaler Zero Trust rollout and incident response.
* Worked with developers on Java production issues, cutting MTTR 40%.

### Network Analyst | Chester County Library System; Remote -- February 2019–April 2022

#### Infrastructure Automation & Efficiency

* Replaced in-house Ghost imaging (several hours per machine, four at a time) with Dell factory provisioning via Image Assist and an automated PowerShell image-build pipeline, so devices were dropshipped plug-and-play to 18 branches. Lease refreshes across a 1,000-device fleet went from one library per day to several, freeing two of three technicians from several weeks of rollout work each cycle.
* Modernized network infrastructure across 18 public libraries by replacing legacy Cisco wireless controller with cloud-managed Meraki platform, reducing support overhead by 60% and cutting licensing costs by 40%.
* Empowered librarians to own content updates via basic HTML and CSS training, reducing website update request time from 3-5 days to same day delivery.

#### Proactive Modernization & Business Continuity

* Led early adoption of Windows 11 and Server 2019, migrating infrastructure 24 months ahead of Windows 10/Server 2012 R2 EOL, building automated deployment tooling using PowerShell and MDT to ensure zero-touch provisioning.
* Served as technical lead for County Disaster Recovery and Business Continuity planning, architecting high-availability solutions including VPN failover, ISP redundancy, and remote work enablement that ensured seamless operations during 2020 pandemic transition.
* Mentored two junior system administrators.

### Service Analyst | County of Chester; West Chester, PA -- October 2016–February 2019

* Delivered technical support for 2,500+ users across hybrid VMware/Windows/Linux environment while maintaining 95%+ CSAT scores through consistent communication and rapid resolution.
* Acted as technical advisor to County Disaster Recovery and Business Continuity committees, providing expertise on high-availability architecture, network redundancy strategies, and ISP failover configurations to ensure operational resilience.

### IT Consultant | Robert Half Technology; Philadelphia, PA -- February 2016–October 2016

* Executed cloud migration projects for multi-site clients, successfully transitioning from on-premise Active Directory/Exchange to Azure AD and Microsoft 365 with zero data loss.
* Maintained 99.9% uptime across diverse Windows and Linux server environments through proactive configuration management and optimized patching workflows.
* Coordinated infrastructure deployments with vendor partners, ensuring structured cabling and equipment installations met performance and compliance standards.

### Technician | County of Chester; West Chester, PA -- April 2015–April 2016

* Provided Level 2 technical support to 900+ users across county agencies, developing PowerShell automation scripts and documentation that reduced ticket escalations by 25%.

## Projects

### Home Projects

* Local LLM Infrastructure & Fine-Tuning: Built local AI experimentation environment running Mixtral 8x7B and 8x22B models via Ollama. Fine-tuned a custom Mixtral 8x7B model, gaining hands-on experience with model architecture, quantization, and GPU resource optimization.
* Rocket.Chat Cloud Deployment: Deployed and managed Rocket.Chat in the public cloud on a Debian cluster (Node.js, MongoDB, NGINX) with automated SSL/TLS certificate lifecycle via Certbot/Let's Encrypt. Provisioned with Ruby/Shell (Chef) and monitored via Prometheus + Grafana.

## Technical Skills

* **Cloud & Infrastructure:** AWS, Azure; VMware vSphere, Hyper-V, VirtualBox
* **Automation & Infrastructure as Code:** Ansible, Terraform; PowerShell, Bash, Ruby, Python, HCL; Chef (familiar with Puppet and Salt)
* **API Integration:** REST APIs: Microsoft Graph, GitHub, Atlassian, CrowdStrike, Power BI
* **Configuration Management:** SCCM, Satellite
* **Monitoring & Observability:** New Relic, Zabbix; Prometheus, Grafana; OpenTelemetry; rsyslog, Logstash (ELK Stack)
* **AI-Assisted Development:** GitHub Copilot, Claude, ChatGPT (daily development); Ollama (local LLM deployment); Mixtral (model fine-tuning and experimentation)
* **Application Support:** Java application troubleshooting; XML configuration; Application server middleware
* **Containerization:** Docker
* **Databases:** Microsoft SQL Server; PostgreSQL, MySQL, MariaDB; MongoDB, Cassandra
* **Data & Analytics:** Power BI, DAX; Semantic modeling (star schema); ETL pipeline design (Python, Jupyter, PowerShell)
* **Networking & Security:** Cisco, Meraki; DNS, PKI/Certificate Management; SSL/TLS Automation (Certbot, Let's Encrypt, ACME Protocol); OpenVPN, AnyConnect, GlobalProtect, Zscaler
* **Web Services & Load Balancers:** NGINX, HAProxy; Apache httpd, IIS
* **Backup Solutions:** Veritas NetBackup; Veritas HubStor (NetBackup SaaS Protection); Dell Avamar, Dell NetWorker; Veeam
* **Directory Services & IAM:** Active Directory; 389 Directory Service, Samba; OneLogin, Okta
* **Email & Messaging Platforms:** Microsoft Exchange (On-Premises & Online); Microsoft 365 & Teams Administration; Google Workspace Administration; Slack Administration (SAML/SSO Integration); Cisco Unified Communications; Email Authentication (DMARC, SPF, DKIM); SMTP Protocol & Relay Configuration (SendGrid, Mailgun, IIS); Compliance & eDiscovery (Purview, Smarsh)
* **Operating Systems:** Linux: Debian, CentOS, RHEL; Unix: macOS, OpenBSD, FreeBSD; Windows: NT 3.1-11, Server 2003-2025
* **Version Control & Development Tools:** Git, GitHub, GitLab, Bitbucket; VS Code, Vim; Vagrant, VirtualBox; strace/truss, Valgrind; PowerCLI, MDT; Pester
* **Package Managers:** apt, dpkg, pkg, yum; chocolatey, nuget, winget (Windows)
* **Collaboration Tools:** Jira, Confluence; Slack, Rocket.Chat, Microsoft Teams

## Education

**B.A., Political Science** | West Chester University, 2013
