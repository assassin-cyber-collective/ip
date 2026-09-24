
Advanced IP Intelligence & Network Reconnaissance Tool

FCK IP is a Python-based terminal reconnaissance tool that collects publicly available information about an IP address or hostname from multiple sources.

It combines IP geolocation, ASN/BGP information, DNS analysis, RDAP, WHOIS, threat intelligence, DNSBL reputation checks, HTTP/HTTPS fingerprinting, SSL/TLS analysis, latency testing, traceroute, and common TCP port scanning into one terminal-based interface.

Powered by ACC — Assassin Cyber Collective

---

Features

Target Validation

The tool first validates the supplied target and determines whether it is an IP address or hostname.

Supported checks include:

- IPv4 validation
- IPv6 validation
- Hostname resolution
- IP version
- Private IP detection
- Loopback detection
- Multicast detection
- Reserved address detection
- Global address detection

---

IP Geolocation

FCK IP queries multiple public IP intelligence providers and compares their responses.

Supported sources include:

- ip-api.com
- ipwho.is
- ipinfo.io
- ipapi.co
- ipapi.is
- ipwhois.app
- ip.guide
- GeoPlugin
- IPLocation
- IP2Location
- IPData
- IPAPI
- IPAddress
- IPRegistry

Depending on source availability, results may include:

IP Address
Country
Country Code
Region
City
ZIP / Postal Code
Latitude
Longitude
Timezone
ISP
Organization
ASN
Proxy / VPN indicators
Hosting / Datacenter indicators
Mobile network indicators

Multiple sources are used because individual IP databases can contain different or outdated information.

---

Threat Intelligence

The tool performs several public reputation and threat-intelligence checks.

Sources include:

- IPAPI.is
- GreyNoise Community
- URLhaus
- IPQualityScore
- Tor Project exit list
- ThreatCrowd

Possible results include:

Proxy
VPN
TOR
Datacenter
Abuser
Crawler
Relay
Bogon
Fraud Score
Recent Abuse
Bot Status
Connection Type
GreyNoise Classification
Historical Resolutions
Malware-host information

Availability depends on the external service.

---

BGP & ASN Intelligence

FCK IP can collect network routing and ASN information using:

- BGPView
- RIPEstat
- PeeringDB
- Team Cymru

Possible information includes:

RIR
Allocation Date
Network Prefix
Origin ASN
ASN Name
ASN Country
ASN Type
ASN Route
ASN Neighbours
Peering Information
Routing Information

---

DNS Analysis

The DNS module performs reverse DNS and additional DNS record lookups.

Supported records include:

PTR
A
AAAA
MX
NS
TXT
CNAME
SOA
CAA

The tool uses "dnspython" for DNS queries.

---

RDAP

FCK IP attempts RDAP queries against multiple regional internet registries.

Supported registries include:

- ARIN
- RIPE NCC
- APNIC
- LACNIC
- AFRINIC

Possible information includes:

Handle
Network Name
Country
Start Address
End Address
IP Version
Registry Entities
Administrative Contacts
Technical Contacts

---

WHOIS

If the "whois" utility is available, the tool can retrieve registry information.

Possible fields include:

Netname
Organization
Country
CIDR
NetRange
INETNUM
Abuse Contact
Route
Origin
Registration Date
Updated Date
Administrative Information
Technical Information

---

Ping & Traceroute

The network diagnostics module can perform:

Ping

- Packet transmission
- Packet loss
- Response time
- RTT information

Traceroute

The tool attempts to display the network path toward the target.

The exact result depends on:

- Target configuration
- Firewall rules
- ISP filtering
- Network connectivity
- Local operating system

---

TCP Port Scanner

FCK IP contains a predefined list of commonly used TCP ports.

Examples include:

20      FTP-Data
21      FTP
22      SSH
23      Telnet
25      SMTP
53      DNS
80      HTTP
110     POP3
139     NetBIOS
143     IMAP
443     HTTPS
445     SMB
587     SMTP-TLS
993     IMAPS
995     POP3S
1433    MSSQL
1521    Oracle
1883    MQTT
2049    NFS
2375    Docker
3000    Dev-HTTP
3306    MySQL
3389    RDP
5000    Flask
5432    PostgreSQL
5601    Kibana
5900    VNC
6379    Redis
8080    HTTP-Proxy
8443    HTTPS
9200    Elasticsearch
11211   Memcached
27017   MongoDB
32400   Plex
50000   SAP

The scanner uses parallel TCP connection attempts to check multiple ports efficiently.

For detected open ports, the tool may attempt a basic banner read.

---

HTTP / HTTPS Fingerprinting

The HTTP module attempts to identify web services running on the target.

Information may include:

HTTP / HTTPS
Status Code
Server
Page Title
Content-Type
X-Powered-By
X-Frame-Options
Strict-Transport-Security
Content-Security-Policy
Location
Set-Cookie
CF-Ray
X-Cache
X-Varnish
X-AspNet-Version
X-Generator

This can provide basic information about the web service and its response headers.

---

SSL / TLS Analysis

The SSL/TLS module connects to port "443" and attempts to retrieve certificate information.

Possible information includes:

Certificate Subject
Certificate Issuer
Valid From
Valid Until
Days Until Expiry
Subject Alternative Names

The tool also attempts to test:

TLS 1.0
TLS 1.1
TLS 1.2
TLS 1.3

Results depend on the target's TLS configuration and the local Python/OpenSSL implementation.

---

DNSBL / Blacklist Check

FCK IP checks the target IP against multiple DNS-based reputation lists.

Examples include:

Spamhaus
Barracuda
SpamCop
SORBS
CBL
PSBL
UCEPROTECT
Backscatterer
SpamRATS
Blocklist.de
WPBL
InterServer

Results can show:

LISTED
CLEAN
UNKNOWN

A DNSBL listing is a reputation signal and does not by itself prove malicious activity.

---

Parallel Recon Engine

One of the main features of FCK IP is its use of parallel processing.

Multiple independent information sources can be queried concurrently using Python's:

ThreadPoolExecutor

This is particularly useful for:

- Multi-source IP lookups
- Geolocation
- TCP port scanning

The terminal also displays progress while operations are running.

---

Scan Modes

The tool provides two main scan modes.

1. Full Deep Recon

Full mode performs the complete reconnaissance workflow.

Target Validation
        ↓
Geolocation
        ↓
Threat Intelligence
        ↓
BGP / ASN
        ↓
DNS
        ↓
RDAP
        ↓
WHOIS
        ↓
Ping
        ↓
Traceroute
        ↓
Port Scan
        ↓
HTTP / HTTPS
        ↓
SSL / TLS
        ↓
DNSBL
        ↓
Final Report

---

2. Quick Scan

Quick Scan is designed to provide a faster overview.

It checks:

- Target
- Country
- City
- ISP
- ASN
- Proxy indicator
- Hosting indicator
- Common TCP ports

---

Installation — Termux

FCK IP is designed to run easily in Termux.

Step 1 — Update Termux

pkg update && pkg upgrade -y

Step 2 — Install Required Packages

pkg install python whois dnsutils traceroute -y

Step 3 — Install Python Dependencies

pip install requests dnspython

Step 4 — Run the Tool

python fckip.py

---

Quick Installation

You can copy these commands directly into Termux:

pkg update && pkg upgrade -y
pkg install python whois dnsutils traceroute -y
pip install requests dnspython
python fckip.py

No "chmod" command is required because the program is executed directly through Python.

---

Usage

Start the tool:

python fckip.py

The main menu will appear:

[1] Full Deep Recon (all sources)
[2] Quick Scan (fast)
[3] Exit

---

Full Scan Example

Select:

1

Then enter a target:

IP / Hostname : 8.8.8.8

The tool will begin the full reconnaissance process.

---

Quick Scan Example

Select:

2

Then enter:

IP / Hostname : 8.8.8.8

The tool will perform the faster scan.

---

JSON Report

After a full reconnaissance scan, FCK IP asks:

Save JSON report? (y/n):

Enter:

y

A JSON report will be generated.

Example:

report_8_8_8_8_20260925_013500.json

The report can contain:

- Scan metadata
- Source responses
- Open ports
- DNSBL results
- IP intelligence information

The exact contents depend on which external sources responded successfully.

---

Example Workflow

$ python fckip.py

ULTRA IP LOOKUP

[1] Full Deep Recon (all sources)
[2] Quick Scan (fast)
[3] Exit

Choice : 1

IP / Hostname : example.com

The hostname is resolved to an IP address and the reconnaissance modules begin running.

---

Requirements

System

Android + Termux
Python 3
Internet Connection

Required Termux Packages

python
whois
dnsutils
traceroute

Python Packages

requests
dnspython

---

Project Structure

A basic setup looks like:

.
├── fckip.py
└── README.md

After running the tool and saving a report, you may also see:

.
├── fckip.py
├── README.md
└── report_<target>_<timestamp>.json

---

Important Limitations

IP intelligence is not equivalent to identifying a person.

An IP address generally cannot reliably provide:

Exact physical address
Exact device location
Exact identity of a user

Geolocation databases may only provide an approximate location associated with a network or ISP.

Different providers can also return different results.

---

External Services

This project communicates with various third-party services.

Their:

- APIs
- Rate limits
- Availability
- Response formats
- Terms of service
- Access policies

may change independently of this project.

A failed source does not necessarily mean that the target has no information.

---

Private IP Addresses

Private addresses are not publicly routable.

Common private IPv4 ranges include:

10.0.0.0/8
172.16.0.0/12
192.168.0.0/16

Public internet intelligence services generally cannot provide normal public-IP information for these addresses.

---

Security & Privacy

Do not enter sensitive information into third-party services unless you understand how that service handles the submitted data.

This tool sends target IP addresses to various external services as part of its lookup process.

Review the applicable third-party service policies before using the tool.

---

Ethical Use

FCK IP is intended for:

- Cybersecurity education
- Authorized security testing
FCK IP

Ultra IP Intelligence & Network Reconnaissance Toolkit

<p align="center">
  <b>FCK IP v5.0</b><br>
  Advanced IP intelligence, network reconnaissance and security analysis toolkit for Termux and Linux.
</p><p align="center">
  <img src="https://img.shields.io/badge/Version-5.0-111111?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.x-111111?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-111111?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-111111?style=for-the-badge">
</p><p align="center">
  <b>Powered by ACC — Assassin Cyber Collective</b>
</p>---

Overview

FCK IP is a terminal-based IP intelligence and network reconnaissance toolkit designed for security research, network troubleshooting, infrastructure analysis and authorized reconnaissance.

It combines multiple information sources and local network utilities into a single interactive command-line interface.

The tool can collect information about an IP address, perform DNS and network analysis, inspect HTTP/HTTPS services, check reputation sources and generate JSON reports.

«Use only on systems, IP addresses and infrastructure that you own or have explicit permission to test.»

---

Features

Module| Capability
IP Intelligence| Geolocation, ISP, organization and network information
ASN / BGP| ASN, prefix and routing information
DNS| Reverse DNS and DNS record analysis
RDAP| Regional Internet registry information
WHOIS| Domain/IP registration information
Threat Intel| Reputation and threat-source checks
Tor Detection| Tor exit-node checking
DNSBL| Blacklist checking
Port Scan| TCP connectivity checks
Banner Grab| Basic service banner detection
HTTP/HTTPS| Service and header inspection
TLS / SSL| Certificate and TLS analysis
Ping| Network reachability
Traceroute| Network path analysis
JSON Reports| Save scan results for later analysis

---

Requirements

- Android + Termux or Linux
- Python 3
- "requests"
- "dnspython"
- "whois"
- "dnsutils"
- "traceroute"
- Internet connection

---

Installation

1. Update Termux

pkg update && pkg upgrade -y

2. Install required packages

pkg install python whois dnsutils traceroute -y

3. Install Python dependencies

pip install requests dnspython

4. Run FCK IP

python fckip.py

No "chmod +x" command is required when running the script with Python.

---

Quick Start

git clone https://github.com/assassin-cyber-collective/FCK-IP.git
cd FCK-IP
pkg update && pkg upgrade -y
pkg install python whois dnsutils traceroute -y
pip install requests dnspython
python fckip.py

If the repository name or URL changes, use the current repository URL provided by the project.

---

Menu

After launching the tool, you can choose between:

[1] Full Deep Recon
[2] Quick Scan
[3] Exit

Full Deep Recon

Performs a broader analysis using the available intelligence, DNS, network, threat and service-analysis modules.

Quick Scan

Performs a faster analysis with the primary IP and network information.

---

Reconnaissance Modules

IP Intelligence

Collects information such as:

- IP address
- Country
- Region
- City
- ZIP / postal information
- Latitude / longitude
- ISP
- Organization
- ASN
- Timezone
- Network information

Multiple external intelligence sources may be queried to improve coverage.

---

ASN & BGP

The toolkit can query routing and autonomous-system information through available public sources.

Information may include:

- ASN
- ASN name
- Network prefix
- Route information
- Registry information
- BGP-related data

---

DNS Analysis

DNS analysis can include:

- Reverse DNS
- A records
- AAAA records
- MX records
- NS records
- TXT records
- CNAME records

---

RDAP

The tool supports Regional Internet Registry RDAP lookups for available IP registration information.

Supported registries include:

ARIN
RIPE
APNIC
LACNIC
AFRINIC

---

WHOIS

If the required system utility is available, the tool can perform WHOIS lookups for additional registration and ownership information.

---

Threat Intelligence

FCK IP can query available public threat-intelligence sources to check information such as:

- Reputation
- Abuse reports
- Suspicious activity
- Threat indicators
- Tor exit-node status
- URL/domain-related intelligence

Results depend on the availability and response of each external service.

---

Port Scanning

The scanner can perform TCP connectivity checks against a collection of common ports.

It may identify:

OPEN
CLOSED
TIMEOUT
ERROR

Basic service banners may also be collected when available.

«Port scanning should only be performed against systems you own or are authorized to test.»

---

HTTP / HTTPS Analysis

The HTTP module can inspect accessible web services and collect information such as:

- HTTP status
- HTTPS availability
- Server headers
- Response headers
- Basic service information

---

SSL / TLS Analysis

The TLS module can attempt to inspect:

- TLS connectivity
- Supported TLS versions
- Certificate information
- TLS-related connection details

Results can vary depending on the target server and local OpenSSL/Python environment.

---

Ping & Traceroute

Network diagnostics can provide:

- Reachability
- Response time
- Network path
- Intermediate hops

The availability of traceroute depends on the installed system utility and environment.

---

Output & Reports

FCK IP can save reconnaissance results as JSON data.

Example:

reports/
└── target.json

JSON reports make it easier to:

- Store scan results
- Review previous reconnaissance
- Process results with other tools
- Build your own analysis workflow

---

Project Structure

FCK-IP/
│
├── fckip.py
├── README.md
└── reports/
    └── *.json

---

Third-Party Services

FCK IP communicates with various public or third-party services for information retrieval.

Depending on the selected modules, these may include services related to:

- IP geolocation
- ASN / BGP
- RDAP
- Threat intelligence
- DNS
- Reputation
- Network intelligence

Availability, rate limits, API requirements and returned data may change without notice.

Always review the terms and privacy policies of external services before using them in a production or automated environment.

---

Privacy

When performing external lookups, the target IP or related information may be sent to third-party services used by the selected modules.

Do not use the tool with information that you are not authorized to disclose to external services.

---

Ethical Use

FCK IP is intended for legitimate purposes such as:

- Security education
- Authorized penetration testing
- Network troubleshooting
- Infrastructure analysis
- Defensive security research
- CTF and laboratory environments
- Analysis of your own systems

Do not use it to:

- Scan unauthorized systems
- Attack networks
- Evade security controls
- Abuse third-party services
- Perform unauthorized reconnaissance
- Violate privacy or applicable laws

You are responsible for how you use this software.

---

Limitations

Results are not guaranteed to be complete or accurate.

Possible limitations include:

- Third-party API downtime
- Rate limiting
- Network failures
- Incomplete geolocation data
- Missing WHOIS/RDAP information
- Blocked requests
- TLS compatibility issues
- DNS resolution failures
- Restricted Termux permissions
- Services requiring API keys
- Changes to third-party APIs

A result from one intelligence provider should not automatically be treated as definitive.

---

Troubleshooting

"ModuleNotFoundError"

Run:

pip install requests dnspython

"whois: command not found"

Run:

pkg install whois -y

DNS-related errors

Run:

pkg install dnsutils -y

Traceroute unavailable

Run:

pkg install traceroute -y

Permission problems

Make sure Termux has the required network access and that the required packages are installed.

---

Security Notice

This project is a reconnaissance and information-gathering tool.

It does not guarantee the accuracy of third-party intelligence and should not be treated as a replacement for professional security assessment tools or independent verification.

Always obtain proper authorization before testing an external target.

---

Credits

Project: FCK IP
Version: 5.0
Organization: Assassin Cyber Collective
Short Name: ACC

Built for security research, learning and authorized network analysis.

---

License

This project is released under the MIT License.

See the "LICENSE" file for the complete license text.

---

<p align="center">
  <b>FCK IP v5.0</b><br>
  IP Intelligence • Network Recon • Security Research
</p><p align="center">
  <b>ASSASSIN CYBER COLLECTIVE — ACC</b>
</p>
