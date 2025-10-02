"""
Input validation utilities for the DDoS tool
"""

from urllib.parse import urlparse


def validate_target(target):
    """Validate if target is a proper URL or IP"""
    if not target:
        return False, "Target cannot be empty"

    try:
        ip_parts = target.split('.')
        if len(ip_parts) == 4:
            if all(0 <= int(part) <= 255 for part in ip_parts):
                return True, "Valid IP address"
    except:
        pass

    try:
        result = urlparse(target if target.startswith(('http://', 'https://')) else f"http://{target}")
        if result.netloc:
            return True, "Valid URL"
    except:
        pass

    return False, "Invalid target format"


def get_target():
    """Get target URL or IP from user"""
    while True:
        target = input("Enter target URL or IP: ").strip()
        is_valid, message = validate_target(target)
        if is_valid:
            return target
        else:
            print(f"[!] {message}. Please try again.")


def get_thread_count():
    """Get number of threads from user"""
    while True:
        try:
            threads = input("Enter number of threads (1-1000) [default 50]: ").strip()
            if not threads:
                return 50
            threads = int(threads)
            if 1 <= threads <= 1000:
                return threads
            else:
                print("[!] Please enter a number between 1 and 1000.")
        except ValueError:
            print("[!] Please enter a valid number.")
