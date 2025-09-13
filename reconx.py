import bs4
import json
import os
import requests
import time
import socket
import sys
import re
import threading
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Animation effects
class Effects:
    @staticmethod
    def typing_effect(text, delay=0.03):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    @staticmethod
    def loading_animation(duration=2, message="Loading"):
        symbols = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            print(f"\r{Colors.CYAN}{message} {symbols[i % len(symbols)]}{Colors.END}", end="")
            time.sleep(0.1)
            i += 1
        print("\r" + " " * (len(message) + 2) + "\r", end="")

    @staticmethod
    def print_separator():
        print(f"{Colors.PURPLE}{'='*60}{Colors.END}")

    @staticmethod
    def print_success(message):
        print(f"{Colors.GREEN}[✓] {message}{Colors.END}")

    @staticmethod
    def print_warning(message):
        print(f"{Colors.YELLOW}[!] {message}{Colors.END}")

    @staticmethod
    def print_error(message):
        print(f"{Colors.RED}[✗] {message}{Colors.END}")

    @staticmethod
    def print_info(message):
        print(f"{Colors.CYAN}[i] {message}{Colors.END}")

class Utils:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def check_os():
        if os.name == 'nt':
            print(f'{Colors.RED}[!] ReconX does not have full Windows support yet{Colors.END}')
            return False
        return True

    @staticmethod
    def check_dependencies():
        dependencies = ['nmap', 'dig', 'whois', 'mtr']
        missing = []
        for dep in dependencies:
            if not Utils.which(dep):
                missing.append(dep)
        return missing

    @staticmethod
    def which(program):
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, _ = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

class ClickjackingTester:
    @staticmethod
    def test_clickjacking(target):
        try:
            url = ClickjackingTester.prepare_url(target)
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers

            Effects.print_separator()
            Effects.print_info(f"Clickjacking Test for {target}")
            Effects.print_separator()

            vulnerable = True
            protection_headers = {
                'X-Frame-Options': False,
                'Content-Security-Policy': False
            }

            # Check for X-Frame-Options header
            if 'X-Frame-Options' in headers:
                protection_headers['X-Frame-Options'] = True
                Effects.print_success(f"X-Frame-Options: {headers['X-Frame-Options']}")
                vulnerable = False
            else:
                Effects.print_warning("X-Frame-Options header missing")

            # Check for Content-Security-Policy with frame-ancestors
            if 'Content-Security-Policy' in headers:
                csp = headers['Content-Security-Policy']
                if 'frame-ancestors' in csp.lower():
                    protection_headers['Content-Security-Policy'] = True
                    Effects.print_success(f"Content-Security-Policy: {csp}")
                    vulnerable = False
                else:
                    Effects.print_warning("Content-Security-Policy present but no frame-ancestors directive")
            else:
                Effects.print_warning("Content-Security-Policy header missing")

            if vulnerable:
                Effects.print_error("Vulnerable to Clickjacking")
                # Generate PoC
                ClickjackingTester.generate_poc(target)
            else:
                Effects.print_success("Protected against Clickjacking")

            return vulnerable, protection_headers

        except Exception as e:
            Effects.print_error(f"Error: {e}")
            return False, {}

    @staticmethod
    def prepare_url(url):
        if not url.startswith(('http://', 'https://')):
            return 'https://' + url
        return url

    @staticmethod
    def generate_poc(target):
        try:
            # Create PoC directory if it doesn't exist
            poc_dir = 'poc'
            if not os.path.exists(poc_dir):
                os.makedirs(poc_dir)

            # Generate filename with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{poc_dir}/clickjacking_{target}_{timestamp}.html"

            # Create the PoC HTML
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Clickjacking PoC - {target}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #d93025;
            text-align: center;
        }}
        .iframe-container {{
            position: relative;
            width: 100%;
            height: 500px;
            border: 2px solid #d93025;
            margin: 20px 0;
        }}
        iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
            opacity: 0.5;
            z-index: 1;
        }}
        .overlay-button {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 15px 30px;
            background: #4285f4;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            z-index: 2;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}
        .instructions {{
            background: #fff8e1;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #ffc107;
        }}
        code {{
            background: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Clickjacking Proof of Concept</h1>
        <p>This page demonstrates a clickjacking vulnerability for <code>{target}</code>.</p>

        <div class="instructions">
            <h3>How to use this PoC:</h3>
            <ol>
                <li>The transparent iframe below contains the target website</li>
                <li>The blue button is overlayed on top of the iframe</li>
                <li>Users may be tricked into clicking the button, thinking it's part of the parent page</li>
                <li>Adjust the iframe opacity with the slider to make the deception more convincing</li>
            </ol>
        </div>

        <div>
            <label for="opacity">Iframe Opacity: </label>
            <input type="range" id="opacity" min="0" max="1" step="0.1" value="0.5" onchange="updateOpacity(this.value)">
            <span id="opacity-value">0.5</span>
        </div>

        <div class="iframe-container">
            <iframe id="victim-site" src="{ClickjackingTester.prepare_url(target)}"></iframe>
            <button class="overlay-button" onclick="alert('You have been clickjacked!')">Click Me</button>
        </div>

        <div>
            <h3>Remediation:</h3>
            <p>To protect against clickjacking, implement one of the following:</p>
            <ul>
                <li>Set the <code>X-Frame-Options</code> header to <code>DENY</code> or <code>SAMEORIGIN</code></li>
                <li>Use Content Security Policy with <code>frame-ancestors</code> directive</li>
                <li>Implement JavaScript frame-busting code</li>
            </ul>
        </div>
    </div>

    <script>
        function updateOpacity(value) {{
            document.getElementById('victim-site').style.opacity = value;
            document.getElementById('opacity-value').textContent = value;
        }}
    </script>
</body>
</html>"""

            # Save the HTML file
            with open(filename, 'w') as f:
                f.write(html_content)

            Effects.print_success(f"Clickjacking PoC generated: {filename}")
            Effects.print_info("Open this file in a web browser to test the vulnerability")

        except Exception as e:
            Effects.print_error(f"Failed to generate PoC: {e}")

class SubdomainScanner:
    def __init__(self, domain):
        self.domain = domain
        self.subdomains = set()
        self.lock = threading.Lock()

    def scan_rapiddns(self):
        try:
            url = f"https://rapiddns.io/subdomain/{self.domain}?full=1#result"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = bs4.BeautifulSoup(response.text, 'html.parser')
                for link in soup.select('td a'):
                    href = link.get('href', '')
                    if self.domain in href and 'http' in href:
                        subdomain = urlparse(href).netloc
                        with self.lock:
                            self.subdomains.add(subdomain)
        except Exception as e:
            pass

    def scan_wayback(self):
        try:
            url = f"http://web.archive.org/cdx/search/cdx?url=*.{self.domain}/*&output=text&fl=original&collapse=urlkey"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                for line in lines:
                    if self.domain in line:
                        subdomain = line.replace('https://', '').replace('http://', '').split('/')[0]
                        with self.lock:
                            self.subdomains.add(subdomain)
        except Exception as e:
            pass

    def scan_crtsh(self, wildcard_level=1):
        try:
            wildcards = '%' * wildcard_level
            url = f"https://crt.sh/?q={wildcards}.{self.domain}&output=json"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    name = item.get('name_value', '')
                    if self.domain in name:
                        names = name.split('\n')
                        for n in names:
                            n = n.strip()
                            if n.startswith('*.'):
                                n = n[2:]
                            if n.endswith(self.domain) and n != self.domain:
                                with self.lock:
                                    self.subdomains.add(n)
        except Exception as e:
            pass

    def scan_alienvault(self):
        try:
            url = f"https://otx.alienvault.com/api/v1/indicators/domain/{self.domain}/passive_dns"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                for record in data.get('passive_dns', []):
                    hostname = record.get('hostname', '')
                    if hostname.endswith(self.domain):
                        with self.lock:
                            self.subdomains.add(hostname)
        except Exception as e:
            pass

    def scan_threatcrowd(self):
        try:
            url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={self.domain}"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                for subdomain in data.get('subdomains', []):
                    if subdomain.endswith(self.domain):
                        with self.lock:
                            self.subdomains.add(subdomain)
        except Exception as e:
            pass

    def scan_hackertarget(self):
        try:
            url = f"https://api.hackertarget.com/hostsearch/?q={self.domain}"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                for line in lines:
                    if ',' in line:
                        subdomain = line.split(',')[0]
                        if subdomain.endswith(self.domain):
                            with self.lock:
                                self.subdomains.add(subdomain)
        except Exception as e:
            pass

    def scan_certspotter(self):
        try:
            url = f"https://certspotter.com/api/v0/certs?domain={self.domain}"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                for cert in data:
                    for dns_name in cert.get('dns_names', []):
                        if dns_name.endswith(self.domain) and dns_name != self.domain:
                            with self.lock:
                                self.subdomains.add(dns_name)
        except Exception as e:
            pass

    def scan_sonar(self):
        try:
            url = f"https://sonar.omnisint.io/subdomains/{self.domain}"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                for subdomain in data:
                    if subdomain.endswith(self.domain):
                        with self.lock:
                            self.subdomains.add(subdomain)
        except Exception as e:
            pass

    def scan_all_sources(self):
        Effects.print_info(f"Scanning subdomains for {self.domain}")
        Effects.print_warning("This may take a while...")

        scan_methods = [
            self.scan_rapiddns,
            self.scan_wayback,
            self.scan_alienvault,
            self.scan_threatcrowd,
            self.scan_hackertarget,
            self.scan_certspotter,
            self.scan_sonar,
        ]

        for level in range(1, 4):
            scan_methods.append(lambda l=level: self.scan_crtsh(l))

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(method) for method in scan_methods]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception:
                    continue

        filtered_subs = set()
        for subdomain in self.subdomains:
            subdomain = subdomain.replace('*.', '')
            if subdomain.endswith(self.domain) and subdomain != self.domain:
                filtered_subs.add(subdomain)

        return sorted(filtered_subs)

class ReconX:
    def __init__(self):
        self.log_dir = 'logs'
        self.target = ''
        self.setup_directories()

    def setup_directories(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def show_banner(self):
        Utils.clear_screen()
        banner = f"""
{Colors.PURPLE}    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗
    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝
    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝
    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗
    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗
    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝

    {Colors.CYAN}[+] ReconX - Advanced Reconnaissance Tool
    {Colors.GREEN}[+] GitHub: github.com/mrofcodyx/reconx{Colors.END}
"""
        Effects.typing_effect(banner, 0.005)

    def show_menu(self):
        Effects.print_separator()
        menu_options = [
            "WhoIs Lookup",
            "DNS Lookup",
            "Nmap Port Scan",
            "HTTP Header Grabber",
            "Clickjacking Test (with PoC)",
            "Robots.txt Scanner",
            "Link Grabber",
            "IP GeoLocation Finder",
            "Traceroute",
            "Subdomain Scanner (Advanced)",
            "Reverse IP Lookup",
            "Exit"
        ]

        for idx, option in enumerate(menu_options, 1):
            if idx == 12:
                print(f"{Colors.RED}[{idx}] {option}{Colors.END}")
            else:
                print(f"{Colors.YELLOW}[{idx}] {Colors.CYAN}{option}{Colors.END}")

        Effects.print_separator()

    def run(self):
        self.show_banner()

        missing_deps = Utils.check_dependencies()
        if missing_deps:
            Effects.print_warning(f"Missing dependencies: {', '.join(missing_deps)}")
            Effects.print_warning("Some features might not work properly\n")
            time.sleep(2)

        while True:
            self.show_menu()
            choice = input(f'\n{Colors.GREEN}[+] Select an option: {Colors.END}').strip()

            if choice == '12':
                print(f'\n{Colors.CYAN}[+] Thank you for using ReconX!{Colors.END}')
                time.sleep(1)
                break

            try:
                choice = int(choice)
                if 1 <= choice <= 11:
                    self.target = input(f'{Colors.GREEN}[+] Target: {Colors.END}').strip().lower()
                    if self.target:
                        Utils.clear_screen()
                        self.process_choice(choice)
                    else:
                        Effects.print_error("Please enter a valid target")
                else:
                    Effects.print_error("Invalid option")
            except ValueError:
                Effects.print_error("Invalid input")

            input(f'\n{Colors.YELLOW}[Press Enter to return to menu]{Colors.END}')
            Utils.clear_screen()
            self.show_banner()

    def process_choice(self, choice):
        actions = {
            1: self.whois_lookup,
            2: self.dns_lookup,
            3: self.nmap_scan,
            4: self.http_headers,
            5: self.clickjacking_test,
            6: self.robots_scanner,
            7: self.link_grabber,
            8: self.geolocation,
            9: self.traceroute,
            10: self.advanced_subdomain_scanner,
            11: self.reverse_ip
        }

        if choice in actions:
            Effects.loading_animation(1, "Processing")
            actions[choice]()

    def whois_lookup(self):
        try:
            Effects.print_separator()
            Effects.print_info(f"WhoIs Lookup Results for {self.target}")
            Effects.print_separator()
            os.system(f'whois {self.target}')
        except Exception as e:
            Effects.print_error(f"Error: {e}")

    def dns_lookup(self):
        try:
            Effects.print_separator()
            Effects.print_info(f"DNS Lookup Results for {self.target}")
            Effects.print_separator()
            os.system(f'dig {self.target} ANY +noall +answer')
        except Exception as e:
            Effects.print_error(f"Error: {e}")

    def nmap_scan(self):
        try:
            log_path = f'{self.log_dir}/nmap_{self.target}_{time.strftime("%Y%m%d_%H%M%S")}.txt'
            Effects.print_warning("Scanning...")
            os.system(f'nmap -sV -sC -oN {log_path} {self.target}')
            Effects.print_success(f"Results saved to: {log_path}")
        except Exception as e:
            Effects.print_error(f"Error: {e}")

    def http_headers(self):
        try:
            url = self.prepare_url(self.target)
            response = requests.get(url, timeout=10, verify=False)
            Effects.print_separator()
            Effects.print_info(f"HTTP Headers for {self.target}")
            Effects.print_separator()
            for key, value in response.headers.items():
                print(f"{Colors.YELLOW}{key}: {Colors.CYAN}{value}{Colors.END}")
        except Exception as e:
            Effects.print_error(f"Error: {e}")

    def clickjacking_test(self):
        vulnerable, protection_headers = ClickjackingTester.test_clickjacking(self.target)

    def robots_scanner(self):
        try:
            url = self.prepare_url(self.target)
            response = requests.get(f'{url}/robots.txt', timeout=10, verify=False)
            Effects.print_separator()
            Effects.print_info(f"Robots.txt for {self.target}")
            Effects.print_separator()
            print(response.text)
        except Exception as e:
            Effects.print_error(f"Error: {e}")

    def link_grabber(self):
        try:
            url = self.prepare_url(self.target)
            response = requests.get(url, timeout=10, verify=False)
            soup = bs4.BeautifulSoup(response.text, 'html.parser')

            Effects.print_separator()
            Effects.print_info(f"Links found on {self.target}")
            Effects.print_separator()

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    print(f"{Colors.YELLOW}{href}{Colors.END}")
        except Exception as e:
            Effects.print_error(f"Error: {e}")

    def geolocation(self):
        try:
            ip = self.target if self.is_ip() else socket.gethostbyname(self.target)
            response = requests.get(f'http://ip-api.com/json/{ip}').json()

            Effects.print_separator()
            Effects.print_info(f"Geolocation Data for {self.target}")
            Effects.print_separator()

            if response['status'] == 'success':
                print(f"""
{Colors.YELLOW}[+] IP: {Colors.CYAN}{response['query']}{Colors.END}
{Colors.YELLOW}[+] Country: {Colors.CYAN}{response['country']}{Colors.END}
{Colors.YELLOW}[+] City: {Colors.CYAN}{response['city']}{Colors.END}
{Colors.YELLOW}[+] ISP: {Colors.CYAN}{response['isp']}{Colors.END}
{Colors.YELLOW}[+] Lat/Lon: {Colors.CYAN}{response['lat']}, {response['lon']}{Colors.END}
{Colors.YELLOW}[+] AS: {Colors.CYAN}{response['as']}{Colors.END}
                """)
            else:
                Effects.print_error("Geolocation failed")
        except Exception as e:
            Effects.print_error(f"Error: {e}")

    def traceroute(self):
        try:
            Effects.print_separator()
            Effects.print_info(f"Traceroute to {self.target}")
            Effects.print_separator()
            os.system(f'mtr --report --report-wide {self.target}')
        except Exception as e:
            Effects.print_error(f"Error: {e}")

    def advanced_subdomain_scanner(self):
        try:
            scanner = SubdomainScanner(self.target)
            subdomains = scanner.scan_all_sources()

            Effects.print_separator()
            Effects.print_info(f"Subdomain Scan Results for {self.target}")
            Effects.print_separator()

            Effects.print_success(f"Found {len(subdomains)} subdomains\n")
            for subdomain in subdomains:
                print(f"  {Colors.YELLOW}{subdomain}{Colors.END}")

            log_path = f'{self.log_dir}/subdomains_{self.target}_{time.strftime("%Y%m%d_%H%M%S")}.txt'
            with open(log_path, 'w') as f:
                for subdomain in subdomains:
                    f.write(f"{subdomain}\n")

            Effects.print_success(f"Results saved to: {log_path}")
        except Exception as e:
            Effects.print_error(f"Error: {e}")

    def reverse_ip(self):
        try:
            ip = self.target if self.is_ip() else socket.gethostbyname(self.target)
            response = requests.get(f'https://api.hackertarget.com/reverseiplookup/?q={ip}').text

            Effects.print_separator()
            Effects.print_info(f"Reverse IP Lookup for {self.target}")
            Effects.print_separator()

            if "No DNS A records found" in response:
                Effects.print_error("No domains found on this IP")
            else:
                print(response)
        except Exception as e:
            Effects.print_error(f"Error: {e}")

    def prepare_url(self, url):
        if not url.startswith(('http://', 'https://')):
            return 'https://' + url
        return url

    def is_ip(self):
        try:
            socket.inet_aton(self.target)
            return True
        except socket.error:
            return False

if __name__ == '__main__':
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if not Utils.check_os():
        sys.exit(1)

    recon = ReconX()
    recon.run()
