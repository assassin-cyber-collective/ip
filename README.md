
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
FCK IP

<p align="center">
  <b>Advanced IP Intelligence & Network Reconnaissance Tool</b>
</p><p align="center">
  Python • Termux • Linux • ACC
</p><p align="center">
  <a href="https://github.com/assassin-cyber-collective/ip">GitHub Repository</a>
</p>---

Features

- IP & Hostname Lookup
- Geolocation & ISP
- ASN / BGP Information
- DNS & RDAP
- WHOIS
- Threat Intelligence
- DNSBL Checks
- TCP Port Scanning
- HTTP / HTTPS Analysis
- SSL / TLS Analysis
- Ping & Traceroute
- JSON Reports

---

Installation

git clone https://github.com/assassin-cyber-collective/ip.git
cd ip

pkg update && pkg upgrade -y
pkg install python whois dnsutils traceroute -y

pip install requests dnspython
python fckip.py

No "chmod" is required.

---

Usage

Run:

python fckip.py

Then choose:

[1] Full Deep Recon
[2] Quick Scan
[3] Exit

Enter an IP address or hostname when requested.

---

Requirements

- Python 3
- Termux or Linux
- Internet connection
- "requests"
- "dnspython"
- "whois"
- "dnsutils"
- "traceroute"

---

Disclaimer

Use FCK IP only for authorized security research, education, troubleshooting, CTFs, and systems you own or have permission to test.

The project uses third-party services, so results may vary depending on availability, rate limits and external API changes.

---

<p align="center">
  <b>FCK IP v5.0</b><br>
  Powered by ACC — Assassin Cyber Collective
</p>
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
