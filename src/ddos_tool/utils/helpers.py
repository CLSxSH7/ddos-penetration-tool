"""
Helper functions for the DDoS tool
"""

import json
import os
from urllib.parse import urlparse


def is_valid_url(url):
    """Check if a string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def is_valid_ip(ip):
    """Check if a string is a valid IPv4 address"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    except:
        return False


def load_config(config_file="config.json"):
    """Load configuration from JSON file"""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}


def save_config(config, config_file="config.json"):
    """Save configuration to JSON file"""
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)


def format_bytes(bytes_value):
    """Format bytes into human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"
