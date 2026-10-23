---
title: Experience
description: Ten-plus years across software, platform, and infrastructure engineering — roles, projects, and technical skills.
permalink: /experience/
---

# Experience

Want a copy of my résumé or a quick chat? [Email me](mailto:jackson@jacksonasmith.com) or connect on [LinkedIn](https://www.linkedin.com/in/jackson-a-smith/).

## Key Projects & Initiatives

* **Shared Library Engineering**: Replaced copy-pasted helpers across 12 repos with shared, versioned modules (retry, email, HTTP resilience, GitHub platform primitives). The email module is now the mail standard for other Corporate Technology teams. Brought core automation to library standards — manifests, versioning, public/private API separation, docs, and the team's first unit tests with CI on every push and PR.

* **High Availability Architecture**: Part of the operations team that removed the single point of failure in core SQL infrastructure with a three-node availability group (sub-15-minute RTO), one piece of taking the platform from 40–60% to 99.99% availability.

* **Legacy Infrastructure Modernization**: Led strategic refactoring of critical systems (internal DNS, certificate lifecycle, syslog normalization) reducing operational escalations by 50% over 12 months through systematic reliability improvements and automation.

* **Security Engineering**: Partnered with InfoSec as a trusted technical contributor across Zero Trust network deployment (Zscaler), certificate authority migration (Entrust → DigiCert with Azure KeyVault automation), PKI lifecycle management, and major security incident response.

## Roles

### Software Engineer | Public Consulting Group; Remote -- March 2026–Present

Technical owner of all code for prodapps, the Corporate Technology team that turns PCG's enterprise platforms into reliable, governed services and automation (four engineers, 12 repos). I turn one-off automation into reusable, tested engineering components.

#### Shared Libraries & Engineering Standards

* Replaced copy-pasted helpers with shared, versioned modules. Each app had its own retry and email logic, causing drift and unclear ownership. I made the case and built the modules; the email module is now the mail standard for other Corporate Technology teams and is rolling out across all 12 of our repos.
* Standardized HTTP resilience (bounded retries, backoff, Retry-After handling), ending per-app reimplementations.
* Modernized email with a backward-compatible drop-in for Send-MailMessage: Graph by default, SMTP fallback, transport hidden from callers.
* Brought core automation to library standards: manifests, versioning, public/private API separation, docs, and the team's first unit tests with CI on every push and PR.

#### GitHub Platform & Governance

* Built a shared GitHub platform layer (discovery, REST/GraphQL access, normalization) so governance and access-review tools share primitives instead of parallel implementations.
* Automated recurring GitHub access reviews on that layer, replacing manual examination.
* Put GitHub Copilot administration on a data-driven footing: consumption and seat-utilization reporting, policy assessment, governance standards for leadership, and cost controls automated through the billing API.
* Designed the BI solution for GitHub Enterprise billing (API ingestion, star-schema model, Power BI dashboards) and re-platformed the ETL to Python so the data team could own it.

#### Testing, CI & AI-Assisted Development

* Established the team's first Pester unit test suite and reusable shared test infrastructure for an existing codebase, creating automated quality gates where none previously existed.
* Configured CI executing Pester tests on every push and PR, enforcing code quality standards from day one.
* Authored a GitHub Copilot custom-instructions file codifying the team's PowerShell style guide, substantially reducing recurring AI-generated anti-patterns across the codebase before changes reach review.
* Use a structured AI-assisted development workflow daily: documenting research findings and implementation plans before generating code, with explicit review checkpoints to correct assumptions and scope, and the same tests and CI gates as any other change — keeping architectural control over AI-authored changes rather than accepting output wholesale.

#### Beyond the Team

* Partnered with a junior engineer outside prodapps to make Corporate Technology's license-assignment automation reliable.
* Identified a credential-exposure risk while reviewing onboarding automation, treating security as part of correctness.

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

* Local LLM Infrastructure & Fine-Tuning: Run local models through Ollama (currently Qwen and DeepSeek) for private experimentation. Previously ran Mixtral 8x7B and 8x22B and fine-tuned a custom Mixtral 8x7B model, gaining hands-on experience with model architecture, quantization, and GPU resource optimization.
* Rocket.Chat Cloud Deployment: Deployed and managed Rocket.Chat in the public cloud on a Debian cluster (Node.js, MongoDB, NGINX) with automated SSL/TLS certificate lifecycle via Certbot/Let's Encrypt. Provisioned with Ruby/Shell (Chef) and monitored via Prometheus + Grafana.

## Community

### Vice President (previously Secretary) | League of Professional Systems Administrators (LOPSA); Volunteer -- September 2021–2025

Board member of a nonprofit professional association for systems administrators: appointed in 2021 and re-elected in 2022, 2023, and 2024.

* Spent several years with the board trying to revitalize the organization. When its local chapters had all gone inactive, I proposed finding a larger organization to carry our members forward rather than letting LOPSA fade out.
* Helped lead the search, evaluating several potential partners before choosing the Association for Computing Machinery (ACM), the largest of them and the one that offered members the most.
* Dissolved LOPSA in 2025 and moved every current member to two years of ACM membership, with access to ACM's monthly publication, its Digital Library, and discounted O'Reilly Online Learning, after an open AMA with members.
* Quoted as a LOPSA board member in [Dice](https://www.dice.com/career-advice/systems-administrator-degree-do-you-need-one-to-succeed) on sysadmin careers.

## Technical Skills

* **Cloud & Infrastructure:** AWS, Azure; VMware vSphere, Hyper-V, VirtualBox
* **Automation & Infrastructure as Code:** Ansible, Terraform; PowerShell, Bash, Ruby, Python, HCL; Chef (familiar with Puppet and Salt)
* **API Integration:** REST APIs: Microsoft Graph, GitHub, Atlassian, CrowdStrike, Power BI
* **Configuration Management:** SCCM, Satellite
* **Monitoring & Observability:** New Relic, Zabbix; Prometheus, Grafana; OpenTelemetry; rsyslog, Logstash (ELK Stack)
* **AI-Assisted Development:** Claude Code, GitHub Copilot with custom instructions (daily development); Ollama with Qwen and DeepSeek (local models); Mixtral 8x7B (prior fine-tuning work)
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
