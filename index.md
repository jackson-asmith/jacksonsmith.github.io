<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-5J2GCC14GK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-5J2GCC14GK');
</script>

<meta name="description" content="The personal website of Jackson Smith, an engineer who builds strong systems helping others do their best work.">

![Oh look, it's Jackson](https://avatars.githubusercontent.com/u/42005615?v=4)

## About me

[Email](mailto:jackson@jacksonasmith.com) | [GitHub](https://github.com/jackson-asmith) | [LinkedIn](https://www.linkedin.com/in/jackson-a-smith/)

Hi, I'm Jackson! I'm a well-rounded infrastructure engineer with over 10 years of experience designing, building, and maintaining cross-platform systems. Proven expertise in Linux and Windows environments, including cloud platforms like AWS and Azure.

I'm known for taking ownership of business-critical projects and leading high-impact initiatives, such as backup system replacement and managing pre-EOL adoption of modern operating systems. I am proficient in technical problem-solving and committed to delivering durable, foundational infrastructure solutions.

Outside of work, I enjoy skiing and cooking, which fuel my creativity and problem-solving skills.

### Operations Engineer | Lincoln Investment; Remote -- April 2022-Present

- Production engineering for 300+ offices nationwide across a hybrid-cloud environment in Azure and multiple data centers
- Automate repeated tasks such as software deployment and system reporting via Bash, Ruby, and PowerShell allowing teams to scale with organization growth
- Design and maintain software defined data centers running bare metal hypervisors on enterprise hardware via tools like HCL, PowerCLI, etc.
- Trusted to mentor peers, communicate clearly across teams, document legacy systems, and take on critical but unglamorous projects ensuring long-term operational stability
- Lead operations engineer from my team on a cross-functional storage modernization project, replacing legacy Dell PowerMax SANs with Nimble or Pure solutions to enhance capacity, reliability, and support long-term Azure migration plans
- Led data driven patch automation insourcing project using Satellite and SCCM, reducing open vulnerabilities by 70% and cutting costs by $400,000 annually
- Led my team’s replacement of aging enterprise backup infrastructure with a modern hybrid cloud solution, increasing capacity by 118 TiB, achieving zero downtime, and strengthening disaster recovery posture and operational visibility across mission-critical systems
- Designed and maintained enterprise monitoring with New Relic and Zabbix, tracking system utilization, latency, and network performance to ensure platform reliability and partnered with developers to extend observability into high-value applications, implemented early SLI/SLO-based alerting, and reduced downtime by 35% across critical services
- Led certificate authority migration from Entrust to DigiCert in less than 6 months, including integration with Azure KeyVault for seamless management of certificates, and delivered clean handoff of operations to the Infrastructure Operations team
- Collaborated with senior developers on pruning hundreds of terabytes of legacy data, proposing and implementing a parallelized PowerShell solution using `ForEach-Object -Parallel` that reduced deletion time from days to hours, significantly improving operational efficiency and resource utilization
- Led the operations team’s biannual audit tasks for core line-of-business applications, validating backups and disaster recovery readiness
- Delivered clean handoff of user account automation via One Login and ADP then Okta and DayForce as well as SAML integration for application access for seamless employee lifecycle management by Digital Workspace team
- Partnered with InfoSec and development teams on all major security incidents, contributing operational expertise and ensuring rapid containment, mitigation, and post-incident analysis across critical services
- Lead organization-wide documentation standardization initiative, developed documentation standard, handover process, and update process centralizing all operational documentation in a single operations Confluence space
- Championed and implemented adoption of Windows Server 2022 and RHEL, well ahead of Windows Server 2012 R2, 2016, and CentOS end of life, increased Domain Functional Level from 2008 to Windows Server 2016

### Network Analyst | Chester County Library System; Remote -- February 2019-April 2022

- Rebuilt hardware provisioning pipeline in VMware using PowerShell and PowerCLI, saving 12 person-months annually through innovative process redesign
- Modernized a network spanning 18 public libraries by replacing legacy Cisco gear with Meraki, reducing support overhead and licensing costs
- Empowered librarians to own content updates via basic HTML and CSS training, reducing website update request time from 3-5 days to same day delivery
- Led early OS migration initiatives, securing senior stakeholder approval to adopt Windows 11 and Server 2019 ahead of Windows 10 and Server 2012/R2 end-of-life and built automated PowerShell and MDT workflows that validated the new platforms and ensured reliable deployment
- Leveraged prior experience as a key technical resource for the County’s Disaster Recovery and Business Continuity committees to enhance system reliability and connectivity, led initiatives on high availability, redundancy, VPN, and ISP failover strategies, and ensured seamless operations during the pandemic by migrating employees from desktop to laptop workstations over 2019
- Mentored two junior system administrators

### Service Analyst | County of Chester; West Chester, PA -- October 2016-February 2019

- Provided support for 2,500+ users in a mixed VMware/Windows/Linux environment while maintaining top CSAT scores across the team reflecting a consistent and communicative approach
- Served as a key technical resource for the County’s Disaster Recovery and Business Continuity committees, driving the development and implementation of plans focused on system reliability and connectivity, provided expertise on high availability, redundancy, VPN configurations, and ISP failover strategies to ensure uninterrupted operations during disaster scenarios

### IT Consultant | Robert Half Technology; Philadelphia, PA -- Feb 2016-Oct 2016

- Supported clients with diverse, multi-site infrastructure; successfully migrated from on-prem AD/Exchange to Azure AD + Microsoft 365
- Delivered 99.9% uptime across Windows and Linux servers, implementing configuration management and better patch workflows
- Coordinated clearly with vendor partners on deployments and structured cabling, ensuring consistency and alignment

### Technician | County of Chester; West Chester, PA -- April 2015-April 2016

- Provided L2 support to 900+ users across county agencies; scripted and documented quick fixes to reduce handoffs and promote consistency across teams

## Certificates

- Google IT Support Professional Certificate

## Projects

### Work Projects

- Migrated core SQL server from single to three node availability aware cluster for high availability and redundancy; eliminating key operational risks while also improving security posture
- Legacy refactoring initiatives: owned high-risk legacy cleanup (internal DNS, cert lifecycle, syslog normalization), reducing internal escalations by 50% over 12 months through consistent and strategic improvement
- Security awareness training: designed and led annual in-house training programs that significantly improved phishing simulation metrics and staff vigilance

### Home Projects

- Rocket.Chat Cloud Deployment: Deployed and managed Rocket.Chat in the public cloud on a Debian cluster (Node.js, MongoDB, NGINX). Provisioned with Ruby/Shell (Chef) and monitored via Prometheus + Grafana

## Technical Skills

### Operating Systems

    Linux: Debian, CentOS, RHEL 
    Unix: macOS versions 10-15, openBSD, FreeBSD
    Windows: more than 400 years experience! NT 3.1-11 Server 2003-2025

### Boot managers

    GNU GRUB
    BOOTMGR
    PXE

### Init Systems

    SystemD

### Package Managers

    apt
    dpkg
    pkg
    yum
    chocolatey/nuget/winget (Windows)

### Automation Orchestration

    Ansible
    Chef
    (familiar with Puppet and Salt)

### Directory Services

    Active Directory
    389 Directory Service
    Samba

### Identity and Access Management/Unified Access Management

    OneLogin
    Okta

### Containers

    Docker

### Hypervisors

    VMware
    HyperV
    VirtualBox

### Monitoring

    Grafana
    Logstash (ELK Stack)
    New Relic
    Prometheus (used in conjunction with Grafana)
    syslog (rsyslog)
    Zabbix

### Databases

    SQL
    Microsoft SQL Server
    MongoDB
    MySQL

### Web Servers

    Apache httpd
    IIS
    NGINX

### Load Balancers, Proxies, and VPNs

    NGINX
    HAProxy
    AnyConnect
    GlobalProtect
    OpenVPN
    Zscaler

### Backup Solutions

    Dell Avamar
    Veritas HubStor (NetBackup SaaS Protection)
    Veritas NetBackup
    Dell NetWorker
    Veeam

### Public Cloud Infrastructure

    AWS
    Azure

### Local Development Tools

    strace/truss
    vim
    git
    vscode
    vagrant
    Valgrind
    VirtualBox

### Languages

    Bash: config and utility scripts < 100 lines
    PowerShell: utility scripts, tools < 500 lines, advanced functions, modules
    Ruby: utility scripts, probes/parsers, extending bash functionality
    Query Languages: enough to query CIM, WMI, etc. which use derivatives of ANSI SQL

### Misc Software

    Ticketing and project management systems
    Jira
    BitBucket
    GitHub
    GitLab
    Slack/Rocket.Chat/Teams

## Soft Skills

Communication, collaboration, consistency, commitment

## Education

- Bachelor's West Chester University
