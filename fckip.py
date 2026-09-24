#!/usr/bin/env python3
import os, sys, time, json, socket, ssl, subprocess, threading
import warnings, re, importlib, csv, ipaddress
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings("ignore")

class K:
    R="\033[38;5;196m"; O="\033[38;5;208m"; Y="\033[38;5;226m"
    G="\033[38;5;46m";  C="\033[38;5;51m";  B="\033[38;5;33m"
    M="\033[38;5;201m"; P="\033[38;5;135m"; W="\033[38;5;255m"
    GR="\033[38;5;245m"; BOLD="\033[1m"; DIM="\033[2m"
    RST="\033[0m"; CLR="\033[K"; IT="\033[3m"

BANNER = f"""
{K.C}{K.BOLD}
     ██╗██████╗     ██╗      ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██████╗
     ██║██╔══██╗    ██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║   ██║██╔══██╗
     ██║██████╔╝    ██║     ██║   ██║██║   ██║█████╔╝ ██║   ██║██████╔╝
     ██║██╔═══╝     ██║     ██║   ██║██║   ██║██╔═██╗ ██║   ██║██╔═══╝
     ██║██║         ██║     ╚██████╔╝╚██████╔╝██║  ██╗╚██████╔╝██║
     ╚═╝╚═╝         ╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝
{K.RST}
{K.M}{K.BOLD}                      powered by ACC  {K.RST}
{K.R}{K.BOLD}             REMEMBER YOU ARE NOT SAFE  —  Mark Assassin{K.RST}
{K.GR}{K.DIM}     ──────────────────────────────────────────────────────{K.RST}
{K.P}{K.IT}        Work with  Parallel Recon Engine  · {K.RST}
"""

REPORT = {}

def clear(): os.system("clear")
def hr(ch="━", w=64, color=None):
    print(f"{color or K.M}{ch*w}{K.RST}")
def head(n, title, icon="◈"):
    print()
    hr("━", 64, K.M)
    print(f"  {K.BOLD}{K.C}⟦{n:02d}⟧{K.RST} {K.Y}{icon}{K.RST} "
          f"{K.BOLD}{K.W}{title}{K.RST}")
    hr("━", 64, K.M)
def f(label, value, color=None):
    if value in (None, "", [], {}): value = f"{K.GR}—{K.RST}"
    print(f"  {K.C}▸{K.RST} {K.BOLD}{K.W}{str(label):<22}{K.RST} "
          f"{color or K.W}{value}{K.RST}")
def note(text, color=None):
    print(f"    {color or K.GR}{text}{K.RST}")
def div():
    print(f"  {K.GR}{'·'*60}{K.RST}")

FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

def spin(text, func, *args, **kw):
    stop = threading.Event(); result = [None]
    def run():
        try: result[0] = func(*args, **kw)
        except Exception: result[0] = None
    def anim():
        i = 0
        while not stop.is_set():
            sys.stdout.write(f"\r  {K.C}{FRAMES[i%10]}{K.RST} "
                             f"{K.W}{text:<52}{K.RST}{K.CLR}")
            sys.stdout.flush(); i += 1; time.sleep(0.06)
    t1 = threading.Thread(target=anim, daemon=True)
    t2 = threading.Thread(target=run, daemon=True)
    t1.start(); t2.start(); t2.join()
    stop.set(); time.sleep(0.04)
    ok = result[0] is not None
    mark = f"{K.G}✔{K.RST}" if ok else f"{K.GR}·{K.RST}"
    sys.stdout.write(f"\r  {mark} {K.W}{text:<52}{K.RST}{K.CLR}\n")
    sys.stdout.flush()
    return result[0]

def D(x):
    return x if isinstance(x, dict) else {}
def L(x):
    return x if isinstance(x, list) else []
def S(x):
    return x if isinstance(x, str) else ("" if x is None else str(x))
def V(x):
    if x is None: return None
    if isinstance(x, (str, int, float, bool)): return x
    if isinstance(x, list):
        parts = []
        for i in x:
            if isinstance(i, (str, int, float, bool)): parts.append(str(i))
            elif isinstance(i, dict): parts.append(", ".join(f"{k}={v}" for k, v in list(i.items())[:3]))
            else: parts.append(str(i))
        return ", ".join(parts)
    if isinstance(x, dict):
        return ", ".join(f"{k}={v}" for k, v in list(x.items())[:6])
    return str(x)

try:
    import requests, urllib3
    urllib3.disable_warnings()
except ImportError:
    os.system(f"{sys.executable} -m pip install requests -q")
    import requests, urllib3
    urllib3.disable_warnings()

UA = {"User-Agent": "Mozilla/5.0 (Linux; Android 14) IntelBot/5.0"}

def _get(url, timeout=10, headers=None, j=True):
    h = dict(UA)
    if headers: h.update(headers)
    try:
        r = requests.get(url, timeout=timeout, headers=h, verify=False)
        if j:
            try: return r.json()
            except Exception: return None
        return r.text
    except Exception: return None

def _post(url, data=None, timeout=12, headers=None):
    h = dict(UA)
    if headers: h.update(headers)
    try:
        r = requests.post(url, data=data, timeout=timeout, headers=h, verify=False)
        try: return r.json()
        except Exception: return r.text
    except Exception: return None

def check_deps():
    print()
    hr("═", 64, K.C)
    print(f"  {K.BOLD}{K.Y}⚙  SYSTEM DEPENDENCY VERIFICATION{K.RST}")
    hr("═", 64, K.C)
    mods = [
        ("requests", "requests", "HTTP client"),
        ("urllib3", "urllib3", "SSL pool"),
        ("dns.resolver", "dnspython", "DNS engine"),
        ("socket", None, "Socket layer"),
        ("ssl", None, "TLS engine"),
        ("json", None, "JSON parser"),
        ("csv", None, "CSV reader"),
        ("ipaddress", None, "CIDR parser"),
    ]
    ok_all = True
    for mod, pip, desc in mods:
        sys.stdout.write(f"\r  {K.C}{FRAMES[0]}{K.RST} {K.W}"
                         f"checking {mod:<14}{K.GR}({desc}){K.RST}{K.CLR}")
        sys.stdout.flush(); time.sleep(0.08)
        try:
            m = importlib.import_module(mod)
            v = getattr(m, "__version__", "")
            vs = f" v{v}" if v else ""
            sys.stdout.write(f"\r  {K.G}✔{K.RST} {K.W}{mod:<14}"
                             f"{K.GR}({desc}){K.G} INSTALLED{vs}{K.RST}{K.CLR}\n")
        except ImportError:
            if pip is None:
                sys.stdout.write(f"\r  {K.R}✘{K.RST} {K.W}{mod:<14}"
                                 f"{K.R} MISSING{K.RST}{K.CLR}\n")
                ok_all = False; continue
            sys.stdout.write(f"\r  {K.Y}↓{K.RST} {K.W}{mod:<14}"
                             f"{K.Y} installing {pip}...{K.RST}{K.CLR}\n")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install",
                                pip, "-q", "--disable-pip-version-check"],
                               capture_output=True, timeout=180)
                importlib.import_module(mod)
                sys.stdout.write(f"  {K.G}✔{K.RST} {K.W}{mod:<14}"
                                 f"{K.G} installed OK{K.RST}\n")
            except Exception:
                sys.stdout.write(f"  {K.R}✘{K.RST} {K.W}{mod:<14}"
                                 f"{K.R} install failed{K.RST}\n")
                ok_all = False
        sys.stdout.flush()
    div()
    print(f"  {K.BOLD}{K.Y}⚙  SYSTEM UTILITIES{K.RST}")
    for tool, desc in [("whois","WHOIS"),("ping","ICMP"),("traceroute","Trace"),
                       ("dig","DNS"),("nslookup","Resolver")]:
        try:
            subprocess.run(["which", tool], capture_output=True, timeout=3, check=True)
            st = f"{K.G}AVAILABLE{K.RST}"
        except Exception:
            st = f"{K.GR}optional{K.RST}"
        print(f"  {K.C}▸{K.RST} {K.W}{tool:<12}{K.GR}{desc:<14}{K.RST} {st}")
    hr("═", 64, K.C)
    print(f"  {K.G}{K.BOLD}✔  ENGINE READY{K.RST}" if ok_all
          else f"  {K.Y}{K.BOLD}⚠  PARTIAL MODE{K.RST}")
    hr("═", 64, K.C)

def src_ipapi(ip):       return _get(f"http://ip-api.com/json/{ip}?fields=66846719")
def src_ipwho(ip):       return _get(f"https://ipwho.is/{ip}")
def src_ipinfo(ip):      return _get(f"https://ipinfo.io/{ip}/json")
def src_ipapico(ip):     return _get(f"https://ipapi.co/{ip}/json/")
def src_ipapiis(ip):     return _get(f"https://api.ipapi.is/?q={ip}")
def src_geoip(ip):       return _get(f"http://www.geoplugin.net/json.gp?ip={ip}")
def src_ipguide(ip):     return _get(f"https://ip.guide/{ip}")
def src_ipwhoisapp(ip):  return _get(f"https://ipwhois.app/json/{ip}")
def src_iplocation(ip):  return _get(f"https://api.iplocation.net/?ip={ip}")
def src_ip2loc(ip):      return _get(f"https://api.ip2location.io/?ip={ip}")
def src_abstract(ip):    return _get(f"https://ipgeolocation.abstractapi.com/v1/?ip_address={ip}")
def src_ipdataco(ip):    return _get(f"https://ipdata.co/{ip}")
def src_ipapicom(ip):    return _get(f"https://ipapi.com/ip_api.php?ip={ip}")
def src_ipaddress(ip):   return _get(f"https://api.ipaddress.com/ip/{ip}")
def src_bgpview(ip):     return _get(f"https://api.bgpview.io/ip/{ip}")
def src_ripestat(ip):    return _get(f"https://stat.ripe.net/data/network-info/data.json?resource={ip}")
def src_ripe_asn(ip):
    d = D(_get(f"https://stat.ripe.net/data/network-info/data.json?resource={ip}"))
    asns = L(D(d.get("data")).get("asns"))
    if asns: return _get(f"https://stat.ripe.net/data/asn-neighbours/data.json?resource=AS{asns[0]}")
    return None
def src_peeringdb(ip):
    d = D(_get(f"https://stat.ripe.net/data/network-info/data.json?resource={ip}"))
    asns = L(D(d.get("data")).get("asns"))
    if asns: return _get(f"https://www.peeringdb.com/api/net?asn={asns[0]}")
    return None
def src_cymru(ip):
    try:
        r = subprocess.run(["whois","-h","whois.cymru.com",ip],
                           capture_output=True,text=True,timeout=15)
        return r.stdout.strip()
    except Exception: return None
def src_urlhaus(ip):     return _post("https://urlhaus-api.abuse.ch/v1/host/", {"host": ip})
def src_rdap(ip):
    for tld in ["https://rdap.arin.net/registry/ip/",
                "https://rdap.db.ripe.net/ip/",
                "https://rdap.apnic.net/ip/",
                "https://rdap.lacnic.net/rdap/ip/",
                "https://rdap.afrinic.net/rdap/ip/"]:
        d = _get(f"{tld}{ip}", 8)
        if d and D(d).get("handle"): return d
    return None
def src_rdns(ip):
    try: return socket.gethostbyaddr(ip)
    except Exception: return None
def src_dns(ip):
    try:
        import dns.resolver, dns.reversename
        out = {}
        try:
            rev = dns.reversename.from_address(ip)
            a = dns.resolver.resolve(rev, "PTR", lifetime=5)
            out["PTR"] = [str(x) for x in a]
        except Exception: pass
        host = L(out.get("PTR"))[0] if out.get("PTR") else None
        if host:
            for t in ["A","AAAA","MX","NS","TXT","CNAME","SOA","CAA"]:
                try:
                    a = dns.resolver.resolve(host, t, lifetime=5)
                    out[t] = [str(x) for x in a][:6]
                except Exception: pass
        return out
    except Exception: return None
def src_ping(ip):
    try:
        r = subprocess.run(["ping","-c","4","-W","2",ip],
                           capture_output=True,text=True,timeout=15)
        return r.stdout
    except Exception: return None
def src_trace(ip):
    try:
        r = subprocess.run(["traceroute","-m","15","-w","2","-q","1",ip],
                           capture_output=True,text=True,timeout=60)
        return r.stdout
    except Exception: return None
def src_greynoise(ip):
    return _get(f"https://api.greynoise.io/v3/community/{ip}", 12)
def src_tor(ip):
    try:
        r = requests.get("https://check.torproject.org/torbulkexitlist",
                         timeout=15, headers=UA, verify=False)
        return "TOR-EXIT" if ip in r.text else "clean"
    except Exception: return None
def src_threatcrowd(ip):
    return _get(f"https://ci-www.threatcrowd.org/api/v2/resolve.json?ip={ip}", 12)
def src_ipqualityscore(ip):
    return _get(f"https://ipqualityscore.com/api/json/ip/free/{ip}")
def src_ipregistry(ip):
    return _get(f"https://api.ipregistry.co/{ip}?key=tryout")

PORTS = {
    20:"FTP-Data",21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",43:"WHOIS",
    53:"DNS",67:"DHCP",69:"TFTP",79:"Finger",80:"HTTP",81:"HTTP-Alt",
    88:"Kerberos",110:"POP3",111:"RPC",113:"Ident",119:"NNTP",123:"NTP",
    135:"MSRPC",137:"NetBIOS",138:"NetBIOS-DGM",139:"NetBIOS-SSN",
    143:"IMAP",161:"SNMP",179:"BGP",194:"IRC",389:"LDAP",443:"HTTPS",
    445:"SMB",465:"SMTPS",500:"ISAKMP",512:"rexec",513:"rlogin",
    514:"Syslog",515:"LPD",520:"RIP",554:"RTSP",587:"SMTP-TLS",
    623:"IPMI",631:"IPP",636:"LDAPS",646:"LDP",873:"Rsync",
    902:"VMware",989:"FTPS-Data",990:"FTPS",993:"IMAPS",995:"POP3S",
    1025:"NFS",1080:"SOCKS",1088:"RDP-Alt",1194:"OpenVPN",
    1433:"MSSQL",1521:"Oracle",1701:"L2TP",1723:"PPTP",1812:"RADIUS",
    1883:"MQTT",1900:"SSDP",2049:"NFS",2082:"cPanel",2083:"cPanel-SSL",
    2086:"WHM",2087:"WHM-SSL",2181:"Zookeeper",2222:"SSH-Alt",
    2375:"Docker",2376:"Docker-TLS",3000:"Dev-HTTP",3128:"Squid",
    3306:"MySQL",3389:"RDP",3690:"SVN",4443:"HTTPS-Alt",5000:"Flask",
    5060:"SIP",5222:"XMPP",5353:"mDNS",5432:"PostgreSQL",5555:"ADB",
    5601:"Kibana",5672:"RabbitMQ",5900:"VNC",5984:"CouchDB",
    5985:"WinRM",5986:"WinRM-SSL",6379:"Redis",6443:"K8s-API",
    6667:"IRC",7001:"WebLogic",7077:"Spark",7199:"Cassandra-JMX",
    7443:"HTTPS-Alt",7474:"Neo4j",7547:"TR-069",8000:"HTTP-Alt",
    8008:"HTTP-Alt",8009:"AJP",8080:"HTTP-Proxy",8081:"HTTP-Alt",
    8086:"InfluxDB",8088:"HTTP-Alt",8090:"HTTP-Alt",8161:"ActiveMQ",
    8180:"HTTP-Alt",8200:"Vault",8443:"HTTPS-Alt",8500:"Consul",
    8880:"HTTP-Alt",8888:"HTTP-Alt",8983:"Solr",9000:"PHP-FPM",
    9001:"Supervisor",9042:"Cassandra",9090:"Prometheus",
    9092:"Kafka",9100:"Printer",9200:"Elasticsearch",9300:"ES-Node",
    9443:"HTTPS-Alt",9999:"HTTP-Alt",10000:"Webmin",10250:"Kubelet",
    11211:"Memcached",15672:"RabbitMQ-Mgmt",16379:"Redis-Alt",
    25565:"Minecraft",27017:"MongoDB",27018:"Mongo-Shard",
    27019:"Mongo-Config",32400:"Plex",37777:"Dahua-DVR",
    50000:"SAP",50070:"Hadoop-NameNode",61616:"ActiveMQ-OpenWire"
}

def _scan(ip,p,t=1.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(t)
    try:
        if s.connect_ex((ip,p)) == 0: return p, True
    except Exception: pass
    finally:
        try: s.close()
        except: pass
    return p, False

def src_scan(ip, ports=None):
    ports = ports or PORTS
    found = []
    with ThreadPoolExecutor(max_workers=150) as ex:
        futs = {ex.submit(_scan, ip, p): p for p in ports}
        for fu in as_completed(futs):
            p, ok = fu.result()
            if ok: found.append(p)
    return sorted(found)

def src_banner(ip, port):
    try:
        s = socket.socket(); s.settimeout(3)
        s.connect((ip, port))
        try: s.send(b"\r\n")
        except: pass
        data = s.recv(512)
        s.close()
        return data.decode(errors="ignore").strip()[:100]
    except Exception: return None

def src_http(ip):
    for sch in ("https","http"):
        try:
            r = requests.get(f"{sch}://{ip}", timeout=7, verify=False,
                             allow_redirects=False, headers=UA)
            t = re.search(r"<title[^>]*>(.*?)</title>", r.text, re.I|re.S)
            return {"scheme":sch,"status":r.status_code,
                    "headers":dict(r.headers),"server":r.headers.get("Server"),
                    "title":t.group(1).strip()[:80] if t else None}
        except Exception: continue
    return None

def src_ssl(ip):
    try:
        ctx = ssl.create_default_context(); ctx.check_hostname=False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((ip,443),timeout=7) as sock:
            with ctx.wrap_socket(sock, server_hostname=ip) as ss:
                return ss.getpeercert()
    except Exception: return None

def src_tls(ip):
    out = {}
    protos = []
    try: protos.append(("TLSv1.0", ssl.TLSVersion.TLSv1))
    except Exception: pass
    try: protos.append(("TLSv1.1", ssl.TLSVersion.TLSv1_1))
    except Exception: pass
    try: protos.append(("TLSv1.2", ssl.TLSVersion.TLSv1_2))
    except Exception: pass
    try: protos.append(("TLSv1.3", ssl.TLSVersion.TLSv1_3))
    except Exception: pass
    for name, proto in protos:
        try:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
            ctx.minimum_version = proto; ctx.maximum_version = proto
            with socket.create_connection((ip,443),timeout=4) as sock:
                with ctx.wrap_socket(sock, server_hostname=ip):
                    out[name] = "supported"
        except Exception:
            out[name] = "no"
    return out

DNSBL = ["zen.spamhaus.org","b.barracudacentral.org","bl.spamcop.net",
         "dnsbl.sorbs.net","cbl.abuseat.org","psbl.surriel.com",
         "ubl.unsubscore.com","dnsbl-1.uceprotect.net",
         "dnsbl-2.uceprotect.net","dnsbl-3.uceprotect.net",
         "ips.backscatterer.org","spam.spamrats.com","noptr.spamrats.com",
         "dyna.spamrats.com","bl.blocklist.de","db.wpbl.info",
         "rbl.interserver.net","spamsources.fabel.dk","truncate.gbudb.net",
         "black.junkemailfilter.com"]

def src_dnsbl(ip):
    rev = ".".join(reversed(ip.split(".")))
    out = {}
    for z in DNSBL:
        try:
            socket.gethostbyname(f"{rev}.{z}")
            out[z] = "LISTED"
        except socket.gaierror:
            out[z] = "clean"
        except Exception:
            out[z] = "unknown"
    return out

def src_whois(ip):
    try:
        r = subprocess.run(["whois", ip], capture_output=True, text=True, timeout=25)
        if r.returncode == 0: return r.stdout
    except Exception: pass
    return None

def is_private(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except Exception:
        return False

def validate_and_resolve(target):
    target = target.strip()
    try:
        ipaddress.ip_address(target)
        return target, "ip"
    except ValueError:
        pass
    try:
        if target.startswith("http://") or target.startswith("https://"):
            target = re.sub(r"^https?://", "", target).split("/")[0]
        ip = socket.gethostbyname(target)
        return ip, "hostname"
    except Exception:
        return None, None

def do_validate(target):
    head(0, "TARGET VALIDATION", "🎯")
    ip, kind = validate_and_resolve(target)
    if not ip:
        note(f"Invalid IP or unresolvable hostname: {target}", K.R)
        return None
    if kind == "hostname":
        f("Input", target)
        f("Resolved IP", ip, K.C)
    else:
        f("Input", target)
        f("Type", "IPv4/IPv6")
    try:
        obj = ipaddress.ip_address(ip)
        f("IP Version", f"IPv{obj.version}")
        f("Private", "YES" if obj.is_private else "No",
          K.Y if obj.is_private else K.G)
        f("Loopback", "YES" if obj.is_loopback else "No")
        f("Multicast", "YES" if obj.is_multicast else "No")
        f("Reserved", "YES" if obj.is_reserved else "No")
        f("Global", "YES" if obj.is_global else "No")
    except Exception: pass
    if is_private(ip):
        note("Private IP — public APIs will not return useful data.", K.Y)
    return ip

def do_geo_parallel(ip):
    head(1, "GEOLOCATION  ·  PARALLEL REAL-TIME FETCH", "🌐")
    sources = [
        ("ip-api.com", src_ipapi),
        ("ipwho.is", src_ipwho),
        ("ipinfo.io", src_ipinfo),
        ("ipapi.co", src_ipapico),
        ("ipapi.is", src_ipapiis),
        ("ipwhois.app", src_ipwhoisapp),
        ("ip.guide", src_ipguide),
        ("geoplugin.net", src_geoip),
        ("iplocation.net", src_iplocation),
        ("ip2location.io", src_ip2loc),
        ("ipdata.co", src_ipdataco),
        ("ipapi.com", src_ipapicom),
        ("ipaddress.com", src_ipaddress),
        ("ipregistry.co", src_ipregistry),
    ]
    results = {}
    lock = threading.Lock()
    done = [0]
    total = len(sources)

    def worker(name, fn):
        r = None
        try: r = fn(ip)
        except Exception: r = None
        with lock:
            results[name] = r
            done[0] += 1
            pct = int(done[0]*100/total)
            filled = int(30*done[0]/total)
            bar = "█"*filled + "░"*(30-filled)
            sys.stdout.write(f"\r  {K.C}[{bar}]{K.RST} {K.Y}{pct:>3}%{K.RST} "
                             f"{K.W}{name:<20}{K.RST}{K.CLR}")
            sys.stdout.flush()

    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = [ex.submit(worker, n, fn) for n, fn in sources]
        for fu in as_completed(futs): pass
    print()
    print()

    REPORT["sources"] = results

    a = D(results.get("ip-api.com"))
    if a.get("status") == "success":
        print(f"  {K.Y}{K.BOLD}◈  PRIMARY IDENTITY (ip-api.com){K.RST}")
        f("IP", a.get("query"))
        f("Country", f"{S(a.get('country'))} [{S(a.get('countryCode'))}]")
        f("Region", a.get("regionName"))
        f("City", a.get("city"))
        f("ZIP", a.get("zip"))
        f("Latitude", a.get("lat"))
        f("Longitude", a.get("lon"))
        f("Timezone", a.get("timezone"))
        div()
        f("ISP", a.get("isp"))
        f("Organization", a.get("org"))
        f("ASN", a.get("as"))
        div()
        pr = a.get("proxy"); ho = a.get("hosting"); mo = a.get("mobile")
        f("Proxy / VPN", "YES ⚠" if pr else "No", K.R if pr else K.G)
        f("Hosting / DC", "YES ⚠" if ho else "No", K.R if ho else K.G)
        f("Mobile Net", "Yes" if mo else "No")

    print()
    hr("─", 60, K.GR)
    print(f"  {K.BOLD}{K.Y}◈  CROSS-VERIFICATION FROM ALL SOURCES{K.RST}")
    hr("─", 60, K.GR)
    for name in ["ipwho.is","ipinfo.io","ipapi.co","ipapi.is","ipwhois.app",
                 "ip.guide","geoplugin.net","iplocation.net","ip2location.io",
                 "ipdata.co","ipapi.com","ipaddress.com","ipregistry.co"]:
        d = D(results.get(name))
        if not d: continue
        if d.get("error") or d.get("message") or d.get("success") is False:
            continue
        printed = False
        for k in ["ip","ip_address","query"]:
            if d.get(k) and not printed:
                if not printed:
                    print(f"  {K.C}┌─{K.RST} {K.BOLD}{K.W}{name}{K.RST}")
                    printed = True
                f("  IP", d.get(k))
                break
        if not printed and d:
            print(f"  {K.C}┌─{K.RST} {K.BOLD}{K.W}{name}{K.RST}")
            printed = True
        for k, v in list(d.items())[:16]:
            if k in ("ip","ip_address","query","success","status"): continue
            val = V(v)
            if val and len(str(val)) < 90:
                f(f"  {k}", val)

def do_threat(ip):
    head(2, "THREAT INTEL  ·  ANONYMITY  ·  REPUTATION", "🛡")
    d = D(spin("ipapi.is · abuse profile", src_ipapiis, ip))
    if d and not d.get("error"):
        for k in ["is_datacenter","is_tor","is_proxy","is_vpn","is_abuser",
                  "is_crawler","is_relay","is_bogon"]:
            v = d.get(k)
            f(k.replace("is_","").title(), v,
              (K.R if v else K.G) if isinstance(v, bool) else K.W)
        f("RIR", d.get("rir"))
        asn = D(d.get("asn"))
        if asn:
            div()
            f("ASN", asn.get("asn"))
            f("ASN Name", asn.get("org"))
            f("ASN Route", asn.get("route"))
            f("ASN Type", asn.get("type"))
            f("ASN Country", asn.get("country"))

    gn = D(spin("GreyNoise · internet noise", src_greynoise, ip))
    if gn and not gn.get("message"):
        div()
        note("GreyNoise Community", K.GR)
        f("Noise", gn.get("noise"))
        f("RIOT", gn.get("riot"))
        cl = gn.get("classification")
        f("Classification", cl, K.R if cl == "malicious" else K.G)
        f("Name", gn.get("name"))
        f("Last Seen", gn.get("last_seen"))
        f("Link", gn.get("link"))

    uh = D(spin("URLhaus · malware host check", src_urlhaus, ip))
    if uh:
        qs = uh.get("query_status")
        if qs:
            f("URLhaus", qs, K.R if qs == "is_host" else K.G)
            if qs == "is_host":
                f("URL Count", uh.get("url_count"))
                for u in L(uh.get("urls"))[:3]:
                    note(f"• {D(u).get('url')} — {D(u).get('threat')}", K.R)

    qs = D(spin("IPQualityScore · fraud score", src_ipqualityscore, ip))
    if qs and qs.get("success"):
        div()
        note("IPQualityScore", K.GR)
        sc = qs.get("fraud_score")
        f("Fraud Score", sc, K.R if (isinstance(sc,(int,float)) and sc>75) else K.Y if sc else K.G)
        f("Proxy", qs.get("proxy"))
        f("VPN", qs.get("vpn"))
        f("TOR", qs.get("tor"))
        f("Active VPN", qs.get("active_vpn"))
        f("Active TOR", qs.get("active_tor"))
        f("Recent Abuse", qs.get("recent_abuse"))
        f("Bot Status", qs.get("bot_status"))
        f("Connection Type", qs.get("connection_type"))
        f("Abuse Velocity", qs.get("abuse_velocity"))

    tor = spin("Tor exit list check", src_tor, ip)
    if tor:
        f("Tor Exit List", tor, K.R if tor == "TOR-EXIT" else K.G)

    tc = D(spin("ThreatCrowd · historical", src_threatcrowd, ip))
    if tc and L(tc.get("resolutions")):
        div()
        note("ThreatCrowd resolutions:", K.GR)
        for r in L(tc.get("resolutions"))[:5]:
            note(f"• {D(r).get('domain')} ({D(r).get('last_resolved')})", K.W)

def do_bgp(ip):
    head(3, "BGP ROUTING  ·  ASN  ·  PREFIX", "🧭")
    d = D(spin("bgpview.io", src_bgpview, ip))
    if d.get("status") == "ok":
        data = D(d.get("data"))
        rir = D(data.get("rir_allocation"))
        if rir:
            f("RIR", rir.get("rir_name"))
            f("Allocated", rir.get("date_allocated"))
            f("RIR Prefix", rir.get("prefix"))
        for i, p in enumerate(L(data.get("prefixes"))[:5]):
            div()
            f(f"Prefix #{i+1}", D(p).get("prefix"))
            f("Description", D(p).get("description"))
            asn = D(D(p).get("asn"))
            f("ASN", f"AS{asn.get('asn')}")
            f("ASN Name", asn.get("name"))
            f("ASN Country", asn.get("country_code"))

    r = D(spin("RIPEstat · network info", src_ripestat, ip))
    if r.get("data"):
        dd = D(r.get("data"))
        if dd.get("prefix"): f("Announced Prefix", dd.get("prefix"))
        asns = L(dd.get("asns"))
        if asns: f("Origin ASN(s)", ", ".join(f"AS{a}" for a in asns))

    n = D(spin("RIPEstat · ASN neighbours", src_ripe_asn, ip))
    if n.get("data"):
        nb = L(D(n.get("data")).get("neighbours"))
        if nb:
            note(f"{len(nb)} ASN neighbours:", K.G)
            for x in nb[:8]:
                note(f"• AS{D(x).get('asn')} — {D(x).get('type')}", K.W)

    p = D(spin("PeeringDB", src_peeringdb, ip))
    if p.get("data"):
        for net in L(p.get("data"))[:2]:
            n = D(net)
            div()
            f("Net Name", n.get("name"))
            f("Type", n.get("info_type"))
            f("Traffic", n.get("info_traffic"))
            f("Scope", n.get("info_scope"))
            f("Ratio", n.get("info_ratio"))
            f("Policy", n.get("policy_general"))

    cy = spin("Team Cymru · ASN whois", src_cymru, ip)
    if cy:
        for l in S(cy).splitlines()[-3:]:
            if l.strip() and "AS" in l: note(l.strip()[:90], K.W)

def do_dns(ip):
    head(4, "DNS  ·  REVERSE  ·  RECORDS", "🔗")
    r = spin("PTR / reverse DNS", src_rdns, ip)
    if r and isinstance(r, tuple):
        f("Hostname", r[0])
        f("Aliases", ", ".join(L(r[1])) if L(r[1]) else "—")
    rec = D(spin("DNS record enumeration", src_dns, ip))
    if rec:
        for t, vals in rec.items():
            if L(vals): f(t, ", ".join(L(vals))[:90])

def do_rdap(ip):
    head(5, "RDAP  ·  REGISTRY", "📋")
    d = D(spin("RDAP lookup", src_rdap, ip))
    if d:
        f("Handle", d.get("handle"))
        f("Name", d.get("name"))
        f("Type", d.get("type"))
        f("Country", d.get("country"))
        f("Start Address", d.get("startAddress"))
        f("End Address", d.get("endAddress"))
        f("IP Version", d.get("ipVersion"))
        for e in L(d.get("entities"))[:5]:
            e = D(e)
            roles = ", ".join(L(e.get("roles")))
            v = L(e.get("vcardArray"))
            nm = ""
            if v and len(v) > 1:
                for it in L(v[1]):
                    it = L(it)
                    if it and it[0] == "fn" and len(it) > 3:
                        nm = it[3]
            f(f"Entity [{roles}]", nm or e.get("handle"))

def do_whois(ip):
    head(6, "WHOIS REGISTRY", "📜")
    out = spin("Running whois", src_whois, ip)
    if out:
        keys = ["netname","orgname","organization","country","cidr","netrange",
                "inetnum","orgabuseemail","descr","route","origin","address",
                "city","regdate","updated","abuse-mailbox","e-mail","org-name",
                "orgabusehandle","tech-c","admin-c","parent","mnt-by","status"]
        shown = 0
        for l in S(out).splitlines():
            ls = l.strip()
            if not ls or ls.startswith("%") or ls.startswith("#"): continue
            if ":" in ls:
                k, v = ls.split(":", 1)
                if k.strip().lower() in keys and v.strip():
                    f(k.strip()[:22], v.strip()[:68]); shown += 1
                    if shown >= 22: break
        if shown == 0:
            for l in S(out).splitlines()[:14]:
                if l.strip(): note(l.strip()[:90], K.W)

def do_latency(ip):
    head(7, "LATENCY  ·  REACHABILITY  ·  PATH", "📶")
    out = spin("ICMP ping (4 packets)", src_ping, ip)
    if out:
        for l in S(out).splitlines():
            if any(x in l for x in ["packets transmitted","rtt","min/avg","time="]):
                note(l.strip()[:90], K.W)
        if "100% packet loss" in S(out):
            note("Host did NOT respond (ICMP may be filtered).", K.Y)
    tr = spin("Traceroute (15 hops)", src_trace, ip)
    if tr:
        div()
        note("Route:", K.GR)
        for l in S(tr).splitlines():
            if l.strip() and not l.startswith("traceroute"):
                note(l.strip()[:90], K.W)

def do_ports(ip):
    head(8, f"PORT SCAN  ·  {len(PORTS)} common ports", "🚪")
    open_ports = spin(f"Scanning {len(PORTS)} ports (parallel)", src_scan, ip, PORTS)
    REPORT["ports"] = open_ports
    if open_ports:
        note(f"{len(open_ports)} open port(s) discovered:", K.G)
        for p in open_ports:
            svc = PORTS.get(p, "unknown")
            crit = p in (23,21,3389,445,139,6379,27017,9200,11211,2375,50000,6667)
            col = K.R if crit else K.G
            bn = src_banner(ip, p)
            extra = f"  {K.GR}└─ {S(bn)[:70]}{K.RST}" if bn else ""
            print(f"  {K.M}│{K.RST}  {col}● OPEN{K.RST}  "
                  f"{K.C}{p:<6}{K.RST} {K.W}{svc}{K.RST}{extra}")
    else:
        note("No common ports open (firewalled or filtered).", K.GR)

def do_http(ip):
    head(9, "HTTP / HTTPS FINGERPRINT", "🌍")
    d = D(spin("Probing web service", src_http, ip))
    if d:
        code = d.get("status")
        f("Scheme", d.get("scheme"))
        f("Status Code", code, K.G if isinstance(code,int) and code < 400 else K.R)
        if d.get("server"): f("Server", d.get("server"))
        if d.get("title"): f("Page Title", d.get("title"))
        div()
        hdrs = D(d.get("headers"))
        for h in ["Content-Type","X-Powered-By","X-Frame-Options",
                  "Strict-Transport-Security","Content-Security-Policy",
                  "Location","Set-Cookie","Via","CF-Ray","X-Cache",
                  "X-Backend","X-Amz-Cf-Id","X-Varnish","X-AspNet-Version",
                  "X-Generator","X-Drupal-Cache","X-Shopify-Stage"]:
            if h in hdrs: f(h, S(hdrs[h])[:72])

def do_ssl(ip):
    head(10, "SSL / TLS ANALYSIS", "🔒")
    cert = D(spin("Fetching SSL certificate (port 443)", src_ssl, ip))
    if cert:
        for fl in ("subject","issuer"):
            val = L(cert.get(fl))
            s = ", ".join(f"{k}={v}" for tup in val for k, v in L(tup))
            f(fl.capitalize(), s[:86])
        f("Valid From", cert.get("notBefore"))
        f("Valid Until", cert.get("notAfter"), K.Y)
        try:
            exp = datetime.strptime(cert.get("notAfter"), "%b %d %H:%M:%S %Y %Z")
            days = (exp - datetime.utcnow()).days
            f("Days Until Expiry", days, K.R if days < 30 else K.G)
        except Exception: pass
        san = L(cert.get("subjectAltName"))
        if san:
            note("Subject Alt Names:", K.GR)
            for t, v in san[:8]: note(f"• {t}: {v}", K.W)
    tv = D(spin("TLS version probe", src_tls, ip))
    if tv:
        div()
        note("TLS Protocol Support:", K.GR)
        for k, v in tv.items():
            f(k, v, K.G if v == "supported" else K.GR)

def do_dnsbl(ip):
    head(11, f"DNSBL  ·  {len(DNSBL)} BLACKLIST ZONES", "🚫")
    d = D(spin("Querying blacklist zones", src_dnsbl, ip))
    if d:
        listed, clean = 0, 0
        for z, st in d.items():
            if st == "LISTED":
                f(z, "⚠ LISTED", K.R); listed += 1
            elif st == "clean":
                clean += 1
        div()
        f("Summary", f"{K.R}{listed} listed{K.RST} / {K.G}{clean} clean{K.RST}",
          K.W)
        REPORT["dnsbl"] = d

def do_final(ip):
    print()
    hr("═", 64, K.G)
    print(f"  {K.BOLD}{K.G}✔  RECONNAISSANCE COMPLETE{K.RST}")
    hr("═", 64, K.G)
    f("Target", ip, K.C)
    f("Scan Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    a = D(REPORT.get("sources", {}).get("ip-api.com"))
    if a.get("status") == "success":
        div()
        print(f"  {K.Y}{K.BOLD}◈  QUICK IDENTITY{K.RST}")
        f("Country", a.get("country"))
        f("City", a.get("city"))
        f("ISP", a.get("isp"))
        f("ASN", a.get("as"))
    ports = L(REPORT.get("ports"))
    if ports:
        div()
        print(f"  {K.Y}{K.BOLD}◈  EXPOSED ATTACK SURFACE{K.RST}")
        f("Open Ports", ", ".join(str(p) for p in ports), K.R)
    dnsbl = D(REPORT.get("dnsbl"))
    listed = [z for z, s in dnsbl.items() if s == "LISTED"]
    div()
    print(f"  {K.Y}{K.BOLD}◈  REPUTATION{K.RST}")
    if listed:
        f("Blacklist", f"LISTED on {len(listed)} zone(s)", K.R)
        for z in listed: note(f"• {z}", K.R)
    else:
        f("Blacklist", "Clean across all zones", K.G)
    hr("═", 64, K.G)
    print(f"  {K.R}{K.BOLD}⚠  Ethical use only! Scan what you own....{K.RST}")
    print(f"  {K.R}{K.BOLD}⚠  Unauthorized scanning is a criminal offense....{K.RST}")
    hr("═", 64, K.G)

def save_report(ip):
    try:
        c = input(f"\n  {K.Y}» Save JSON report? (y/n): {K.RST}").strip().lower()
    except Exception: return
    if c != "y": return
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"report_{ip.replace('.','_').replace(':','_')}_{ts}.json"
    try:
        with open(fn,"w") as f:
            json.dump(REPORT, f, indent=2, default=str)
        print(f"  {K.G}✔ Saved → {K.C}{fn}{K.RST}")
    except Exception as e:
        print(f"  {K.R}✘ Save failed: {e}{K.RST}")

def run_full(target):
    REPORT.clear()
    ip = do_validate(target)
    if not ip: return
    REPORT["meta"] = {"target": target, "ip": ip,
                      "started": datetime.now().isoformat(),
                      "tool": "ULTRA IP LOOKUP v5.0"}
    do_geo_parallel(ip)
    do_threat(ip)
    do_bgp(ip)
    do_dns(ip)
    do_rdap(ip)
    do_whois(ip)
    do_latency(ip)
    do_ports(ip)
    do_http(ip)
    do_ssl(ip)
    do_dnsbl(ip)
    do_final(ip)
    save_report(ip)

def quick_scan(target):
    ip = do_validate(target)
    if not ip: return
    print()
    hr("═", 64, K.G)
    print(f"  {K.BOLD}{K.G}◈  QUICK SCAN — {ip}{K.RST}")
    hr("═", 64, K.G)
    a = D(spin("ip-api.com", src_ipapi, ip))
    if a.get("status") == "success":
        f("Country", a.get("country"))
        f("City", a.get("city"))
        f("ISP", a.get("isp"))
        f("ASN", a.get("as"))
        f("Proxy", a.get("proxy"))
        f("Hosting", a.get("hosting"))
    ports = spin("Port scan (top 20)", src_scan, ip,
                 {22:"SSH",80:"HTTP",443:"HTTPS",21:"FTP",23:"Telnet",
                  25:"SMTP",53:"DNS",110:"POP3",143:"IMAP",3306:"MySQL",
                  3389:"RDP",8080:"HTTP-Alt",445:"SMB",139:"NetBIOS",
                  6379:"Redis",27017:"MongoDB",9200:"ES",11211:"Memcached",
                  5900:"VNC",8443:"HTTPS-Alt"})
    if ports:
        f("Open Ports", ", ".join(str(p) for p in ports), K.R)
    else:
        f("Open Ports", "none", K.G)
    hr("═", 64, K.G)

def menu():
    while True:
        clear()
        print(BANNER)
        print()
        hr("═", 64, K.C)
        print(f"  {K.BOLD}{K.C}◈  MAIN MENU{K.RST}")
        hr("═", 64, K.C)
        for n, t in [("1","Full Deep Recon (all sources)"),
                     ("2","Quick Scan (fast)"),
                     ("3","Exit")]:
            print(f"  {K.Y}[{n}]{K.RST}  {K.W}{t}{K.RST}")
        hr("═", 64, K.C)
        try:
            ch = input(f"  {K.C}┌──▶{K.RST} {K.Y}Choice :{K.RST} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); return
        if ch == "1":
            try:
                t = input(f"  {K.C}┌──▶{K.RST} {K.Y}IP / Hostname :{K.RST} ").strip()
            except Exception: continue
            if not t: continue
            try:
                run_full(t)
                input(f"\n  {K.Y}Press Enter...{K.RST}")
            except KeyboardInterrupt:
                print(f"\n  {K.R}Interrupted.{K.RST}"); time.sleep(1)
        elif ch == "2":
            try:
                t = input(f"  {K.C}┌──▶{K.RST} {K.Y}IP / Hostname :{K.RST} ").strip()
            except Exception: continue
            if not t: continue
            try:
                quick_scan(t)
                input(f"\n  {K.Y}Press Enter...{K.RST}")
            except KeyboardInterrupt:
                print(f"\n  {K.R}Interrupted.{K.RST}"); time.sleep(1)
        elif ch == "3":
            print(f"\n  {K.G}Goodbye. Stay safe —  but but but......you are not safe! {K.RST}\n")
            return

def main():
    clear()
    print(BANNER)
    time.sleep(0.3)
    check_deps()
    time.sleep(0.3)
    menu()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print(f"\n{K.R}Terminated.{K.RST}"); sys.exit(0)