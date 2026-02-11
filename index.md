<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-5J2GCC14GK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-5J2GCC14GK');
</script>

<meta name="description" content="The personal website of Jackson Smith, an engineer who builds strong systems helping others do their best work.">

<style>
  nav {
    position: sticky;
    top: 0;
    background: Canvas;
    z-index: 10;
  }
</style>

<nav>
  <ul>
    <li><a href="#key-projects--initiatives">Key Projects</a></li>
    <li><a href="#experience">Experience</a></li>
    <li><a href="#certificates">Certificates</a></li>
    <li><a href="#projects">Projects</a></li>
    <li><a href="#technical-skills">Skills</a></li>
    <li><a href="#education">Education</a></li>
  </ul>
</nav>

![Oh look, it's Jackson](https://avatars.githubusercontent.com/u/42005615?v=4)

## About me

[Email](mailto:jackson@jacksonasmith.com) | [GitHub](https://github.com/jackson-asmith) | [LinkedIn](https://www.linkedin.com/in/jackson-a-smith/)

Hi, I'm Jackson! I'm an Infrastructure & Reliability Engineer with 10+ years of experience driving reliability, automation, and scalability across hybrid cloud environments. I specialize in designing resilient systems, implementing infrastructure-as-code, and leading high-impact modernization initiatives that reduce operational toil and improve business continuity. 

I have a proven track record of eliminating single points of failure, reducing vulnerabilities by 70%, and delivering $400K+ in cost savings through automation and strategic infrastructure improvements. I'm known for taking ownership of business-critical projects and delivering durable, foundational solutions.

Outside of work, I enjoy skiing and cooking

<div id="Key Projects & Initiatives">
## Key Projects & Initiatives

* **High Availability Architecture**: Eliminated single point of failure for core SQL infrastructure by architecting three-node availability group cluster, achieving 99.99% uptime and improved disaster recovery posture with sub-15-minute RTO.

* **Legacy Infrastructure Modernization**: Led strategic refactoring of critical systems (internal DNS, certificate lifecycle, syslog normalization) reducing operational escalations by 50% over 12 months through systematic reliability improvements and automation.

* **Security & Compliance Leadership**: Designed and delivered annual security awareness training programs, improving phishing simulation pass rates by 40% and establishing security-first culture across engineering teams.

<div id="Experience">
## Experience

### Operations Engineer | Lincoln Investment; Remote -- April 2022-January 2026

**Platform Reliability & Scalability**

* Architected and operate hybrid-cloud platform serving 300+ offices nationwide across Azure and multi-datacenter VMware environment, ensuring 99.9% availability for business-critical services.
* Eliminated technical debt through strategic virtualization platform evolution (vSphere 6.5 → 8.0.3), improving resource efficiency by 30% and enabling automated failover capabilities across datastore clusters.
* Leading enterprise storage modernization initiative, replacing aging Dell PowerMax SANs with high-performance Nimble/Pure solutions to support 5-year Azure migration roadmap and double available capacity.

**Automation & Operational Excellence**

* Implemented automated patching pipeline for Linux and Windows servers using Satellite and SCCM, reducing monthly vulnerability exposure by 70% and eliminating $400K in annual outsourcing costs.
* Designed enterprise observability platform using New Relic and Zabbix with SLI/SLO-based alerting, reducing unplanned downtime by 35% through proactive performance monitoring and capacity planning.
* Accelerated development velocity by leveraging AI-assisted tooling (GitHub Copilot, Claude, ChatGPT) for rapid prototyping of automation scripts and instrumenting applications with OpenTelemetry for enhanced observability.
* Collaborated with senior developers on pruning hundreds of terabytes of legacy data, proposing and implementing a parallelized PowerShell solution using `ForEach-Object -Parallel` that reduced deletion time from days to hours, significantly improving operational efficiency and resource utilization.
* Designed and led the implementation of organization-wide documentation standards, handover requirements, and maintenance processes, coordinating with engineering, operations, and platform teams to ensure consistency then centralized all system documentation in a single Confluence space.

**Cross-Functional Collaboration & Application Support**

* Partnered with development teams to troubleshoot production issues in Java applications, providing platform-level expertise on authentication failures, XML configuration errors, and middleware connectivity problems that reduced mean-time-to-resolution by 40%.
* Served as infrastructure liaison during critical incidents, analyzing application logs, reviewing production code, and identifying root causes related to network connectivity, certificate validation, and environment-specific configurations.
* Partnered with InfoSec team on security initiatives including Zscaler Zero Trust deployment (network integration, certificate configuration, application testing) and all major security incidents, contributing operational expertise and ensuring rapid containment, mitigation, and post-incident analysis across critical services.

**Business Continuity & Disaster Recovery**

* Architected and deployed modern hybrid-cloud backup solution (NetBackup on Flex Appliance with Azure archive tier), achieving zero-downtime migration while improving RTO from 24 hours to 4 hours and enhancing operational visibility.
* Led biannual disaster recovery validation for core line-of-business applications, ensuring backup integrity and recovery procedures meet business SLAs.
* Orchestrated certificate authority migration from Entrust to DigiCert in under 6 months, integrating with Azure KeyVault for automated certificate lifecycle management and seamless operational handoff.

**Strategic Initiatives & Risk Mitigation**

* Championed early adoption of Server 2022 and RHEL 8/9, proactively migrating workloads 18 months ahead of EOL deadlines (Server 2012 R2, Server 2016, CentOS), eliminating compliance risks and modernizing security posture.
* Elevated Active Directory Domain Functional Level from 2008 to 2016, unlocking modern security features and improving authentication reliability across enterprise.
* Architected and managed federated identity infrastructure connecting Lincoln's 
Active Directory with 20+ external Microsoft 365/Entra ID tenants for financial 
advisor offices nationwide. Designed automated provisioning workflow creating 
mail-enabled users in federated tenants with license assignment via OneLogin, 
enabling secure cross-organization collaboration while maintaining centralized 
identity management.
* Delivered clean handoff of user account automation via OneLogin/ADP then Okta/DayForce as well as SAML integration for application access for seamless employee lifecycle management by Digital Workspace team.

### Network Analyst | Chester County Library System; Remote -- February 2019-April 2022

**Infrastructure Automation & Efficiency**

* Eliminated manual provisioning bottlenecks by rebuilding hardware deployment pipeline using PowerShell and PowerCLI, reducing provisioning time from 4 hours to 15 minutes and saving 12 person-months annually.
* Modernized network infrastructure across 18 public libraries by replacing legacy Cisco wireless controller with cloud-managed Meraki platform, reducing support overhead by 60% and cutting licensing costs by 40%.
* Empowered librarians to own content updates via basic HTML and CSS training, reducing website update request time from 3-5 days to same day delivery.

**Proactive Modernization & Business Continuity**

* Led early adoption of Windows 11 and Server 2019, migrating infrastructure 24 months ahead of Windows 10/Server 2012 R2 EOL, building automated deployment tooling using PowerShell and MDT to ensure zero-touch provisioning.
* Served as technical lead for County Disaster Recovery and Business Continuity planning, architecting high-availability solutions including VPN failover, ISP redundancy, and remote work enablement that ensured seamless operations during 2020 pandemic transition.
* Mentored two junior system administrators.

### Service Analyst | County of Chester; West Chester, PA -- October 2016-February 2019

* Delivered technical support for 2,500+ users across hybrid VMware/Windows/Linux environment while maintaining 95%+ CSAT scores through consistent communication and rapid resolution.
* Acted as technical advisor to County Disaster Recovery and Business Continuity committees, providing expertise on high-availability architecture, network redundancy strategies, and ISP failover configurations to ensure operational resilience.

### IT Consultant | Robert Half Technology; Philadelphia, PA -- Feb 2016-Oct 2016

* Executed cloud migration projects for multi-site clients, successfully transitioning from on-premise Active Directory/Exchange to Azure AD and Microsoft 365 with zero data loss.
* Maintained 99.9% uptime across diverse Windows and Linux server environments through proactive configuration management and optimized patching workflows.
* Coordinated infrastructure deployments with vendor partners, ensuring structured cabling and equipment installations met performance and compliance standards.

### Technician | County of Chester; West Chester, PA -- April 2015-April 2016

* Provided Level 2 technical support to 900+ users across county agencies, developing PowerShell automation scripts and documentation that reduced ticket escalations by 25%.

<div id="Certificates">
## Certificates

- Google IT Support Professional Certificate

<div id="Home Projects">
## Home Projects

- Local LLM Infrastructure & Fine-Tuning: Built local AI experimentation environment running Mistral 8x7b and 8x22b models via Ollama. Fine-tuned custom Mixtral 8x7b model using official training guides, gaining hands-on experience with model architecture, quantization, and GPU resource optimization.
- * Rocket.Chat Cloud Deployment: Deployed and managed Rocket.Chat in the public cloud on a Debian cluster (Node.js, MongoDB, NGINX) with automated SSL/TLS certificate lifecycle via Certbot/Let's Encrypt. Provisioned with Ruby/Shell (Chef) and monitored via Prometheus + Grafana.

<div id="Technical Skills">
## Technical Skills

### Cloud & Infrastructure
```
AWS, Azure
VMware vSphere, Hyper-V, VirtualBox
```

### Automation & Infrastructure as Code
```
Ansible, Terraform
PowerShell, Bash, Ruby, Python, HCL
Chef (familiar with Puppet and Salt)
```

### Configuration Management
```
SCCM, Satellite
```

### Monitoring & Observability
```
New Relic, Zabbix
Prometheus, Grafana
OpenTelemetry
rsyslog, Logstash (ELK Stack)
```

### AI-Assisted Development
```
GitHub Copilot, Claude, ChatGPT (Production)
Ollama (local LLM deployment)
Mixtral/Mistral (model fine-tuning and experimentation)
```

### Application Support
```
Java application troubleshooting
XML configuration
Application server middleware
```

### Containerization
```
Docker
```

### Databases
```
Microsoft SQL Server
PostgreSQL, MySQL, MariaDB
MongoDB, Cassandra
```

### Networking & Security
```
Networking & Security
Cisco, Meraki
DNS, PKI/Certificate Management
SSL/TLS Automation (Certbot, Let's Encrypt, ACME Protocol)
OpenVPN, AnyConnect, GlobalProtect, Zscaler
```

### Web Services & Load Balancers
```
NGINX, HAProxy
Apache httpd, IIS
```

### Backup Solutions
```
Veritas NetBackup
Veritas HubStor (NetBackup SaaS Protection)
Dell Avamar, Dell NetWorker
Veeam
```

### Directory Services & IAM
```
Active Directory
389 Directory Service, Samba
OneLogin, Okta
```
### Email & Messaging Platforms
```
Microsoft Exchange (On-Premises & Online)
Microsoft 365 & Teams Administration
Google Workspace Administration  
Slack Administration (SAML/SSO Integration)
Cisco Unified Communications
Email Authentication (DMARC, SPF, DKIM)
SMTP Protocol & Relay Configuration (SendGrid, Mailgun, IIS)
Compliance & eDiscovery (Purview, Smarsh)
```

### Operating Systems
```
Linux: Debian, CentOS, RHEL
Unix: macOS, OpenBSD, FreeBSD
Windows: NT 3.1-11, Server 2003-2025
```

### Version Control & Development Tools
```
Git, GitHub, GitLab, Bitbucket
VS Code, Vim
Vagrant, VirtualBox
strace/truss, Valgrind
PowerCLI, MDT
```

### Init Systems & Boot Managers
```
SystemD
GNU GRUB, BOOTMGR, PXE
```

### Package Managers
```
apt, dpkg, pkg, yum
chocolatey, nuget, winget (Windows)
```

### Collaboration Tools
```
Jira, Confluence
Slack, Rocket.Chat, Microsoft Teams
```
<div id="Education">
## Education

**B.A.** | West Chester University
