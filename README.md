# ReconX — Advanced Reconnaissance Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]()  
[![Stars](https://img.shields.io/github/stars/mrofcodyx/reconx?style=social)]()  
[![Issues](https://img.shields.io/github/issues/mrofcodyx/reconx)]()  
[![Last Commit](https://img.shields.io/github/last-commit/mrofcodyx/reconx)]()  

> **ReconX** is a CLI reconnaissance and OSINT tool written in Python.  
> It integrates multiple passive and active enumeration techniques: whois, DNS, nmap, HTTP headers, clickjacking testing (with PoC), robots.txt, link extraction, IP geolocation, traceroute, advanced subdomain scanner, and reverse IP lookup.  

---

## Table of Contents

- [About](#about)  
- [Features](#features)  
- [Demo](#demo)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Dependencies](#dependencies)  
- [Logs & Output](#logs--output)  
- [Best Practices & Ethics](#best-practices--ethics)    
- [Contributing](#contributing)

---

## About

ReconX is designed for pentesters, bug bounty hunters, and OSINT enthusiasts who need a lightweight terminal-based reconnaissance tool with multiple integrated functions. It focuses on simplicity, readable terminal output, and automatic logging of results.

---

## Features

- ✅ **Whois Lookup** (`whois`)  
- ✅ **DNS Lookup** (`dig`)  
- ✅ **Nmap scan** with default flags (`-sV -sC`) + auto logging  
- ✅ **HTTP Headers grabber**  
- ✅ **Clickjacking Test** (auto-generates PoC HTML in `poc/`)  
- ✅ **Robots.txt scanner**  
- ✅ **Link extractor** (`<a href>`)  
- ✅ **IP Geolocation** (via `ip-api.com`)  
- ✅ **Traceroute** (`mtr` report)  
- ✅ **Subdomain Scanner** (crt.sh, Wayback, RapidDNS, ThreatCrowd, CertSpotter, Sonar, AlienVault, Hackertarget) with concurrency (`ThreadPoolExecutor`)  
- ✅ **Reverse IP Lookup** (hackertarget API)  
- ✔️ Results auto-saved into `logs/`  

---

## Demo
*Short caption: ReconX running in the terminal (click to view full size).*
![ReconX terminal screenshot](1.png)

Run the tool:

```bash
python3 reconx.py
```

Example menu:

```

    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗
    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝
    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝
    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗
    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗
    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝

    [+] ReconX - Advanced Reconnaissance Tool
    [+] GitHub: github.com/mrofcodyx/reconx

============================================================
[1] WhoIs Lookup
[2] DNS Lookup
[3] Nmap Port Scan
[4] HTTP Header Grabber
[5] Clickjacking Test (with PoC)
[6] Robots.txt Scanner
[7] Link Grabber
[8] IP GeoLocation Finder
[9] Traceroute
[10] Subdomain Scanner (Advanced)
[11] Reverse IP Lookup
[12] Exit
============================================================

[+] Select an option:
```

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/mrofcodyx/reconx.git
cd reconx
```

2. (Optional) Create and activate a virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

3. Install Python dependencies:

Install them:
```bash
pip install -r requirements.txt
```

4. Install required system tools:  

- `nmap` (port scanning)  
- `dig` (DNS queries, package: `dnsutils` or `bind-utils`)  
- `whois` (whois client)  
- `mtr` (traceroute reports)  

For Debian/Ubuntu:
```bash
sudo apt update
sudo apt install -y nmap dnsutils whois mtr
```

---

## Usage

Run interactively:

```bash
python3 reconx.py
```

Examples:

- Subdomain scanning → results saved to `logs/subdomains_example.com_YYYYMMDD_HHMMSS.txt`  
- Clickjacking PoC → generated under `poc/clickjacking_example.com_YYYYMMDD_HHMMSS.html`  

---

## Dependencies

- **Python 3.8+** recommended  
- Python libs: `requests`, `beautifulsoup4`  
- Relies on external system binaries (`nmap`, `dig`, `whois`, `mtr`) via `os.system()` calls  
- Subdomain enumeration uses multiple public sources (crt.sh, Wayback, Sonar, etc.) — be mindful of API limits  

---

## Logs & Output

- Logs are stored in `logs/` (nmap, subdomains, etc.)  
- Clickjacking PoCs in `poc/`  
- Terminal output is colorized for readability  

---

## Best Practices & Ethics

⚠️ **Important disclaimer**  
Use ReconX only on systems you **own or are explicitly authorized to test**. Unauthorized scanning may be **illegal**.  

- Run only in controlled environments or with written permission  
- Respect API limits and ToS from third-party services  
- Handle sensitive data (logs, domains, hosts) responsibly  

---

## Contributing

1. Fork the repo  
2. Create a branch: `git checkout -b feature/my-feature`  
3. Commit & push: `git commit -m "feat: description"` / `git push origin feature/my-feature`  
4. Open a Pull Request with a clear description  

---

## Author

- Created by **mr_ofcodyx**  
- GitHub: [@Mr_ofcodyx](https://github.com/mrofcodyx)

