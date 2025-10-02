"""
Logging utilities for the DDoS tool
"""

import os
import datetime
from threading import Lock


class AttackLogger:
    """Thread-safe logger for attack activities"""

    def __init__(self, log_file="ddos_attack.log"):
        self.log_file = os.path.join("logs", log_file)
        self.lock = Lock()

        os.makedirs("logs", exist_ok=True)

    def log_event(self, message, level="INFO"):
        """Log an event with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        with self.lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)

    def log_attack_start(self, target, threads):
        """Log attack start event"""
        self.log_event(f"Attack started on {target} with {threads} threads", "ATTACK")

    def log_attack_stop(self, stats):
        """Log attack stop event with statistics"""
        self.log_event(f"Attack stopped. Stats: {stats}", "ATTACK")

    def log_error(self, error_message):
        """Log an error"""
        self.log_event(error_message, "ERROR")


# Global logger instance
attack_logger = AttackLogger()


def get_logger():
    """Get the global logger instance"""
    return attack_logger
