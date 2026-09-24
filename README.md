FCK IP — ULTRA IP LOOKUP

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
- Network administration
- Troubleshooting
- OSINT research
- CTF environments
- Personal lab environments
- Infrastructure you own
- Systems where you have explicit authorization

Only scan systems you own or have permission to test.

Do not use this tool for unauthorized scanning, harassment, privacy invasion, disruption, or other unlawful activity.

---

Disclaimer

This project is provided for educational and authorized security-research purposes.

The author and contributors are not responsible for misuse of this software or for activity performed against systems without proper authorization.

Always obtain appropriate permission before performing reconnaissance or port scanning.

---

Credits

ULTRA IP LOOKUP v5.0

Powered by
ASSASSIN CYBER COLLECTIVE — ACC

Parallel Recon Engine
Python 3

---

License

If you publish this project publicly, add the license that matches how you want others to use, modify, and redistribute the software.

Example:

MIT License

or provide your own license terms.

---

Stay Safe

Scan what you own.
Test what you are authorized to test.
Learn responsibly.
