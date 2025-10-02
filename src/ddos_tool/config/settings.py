"""
Global settings and configuration for the DDoS tool
"""

import os


class Settings:
    """Global application settings"""

    DEFAULT_THREADS = 50
    MAX_THREADS = 1000
    MIN_THREADS = 1

    REQUEST_TIMEOUT = 5  # seconds
    THREAD_START_DELAY = 0.01  # seconds between thread starts

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]

    LOG_DIRECTORY = "logs"
    DEFAULT_LOG_FILE = "ddos_attack.log"

    AUTHORIZED_TESTING_WARNING = "WARNING: Authorized testing only! Only use on systems you own or have explicit permission to test"

    @classmethod
    def get_user_agents(cls):
        """Get list of user agent strings"""
        return cls.USER_AGENTS

    @classmethod
    def get_thread_limits(cls):
        """Get thread configuration limits"""
        return {
            'min': cls.MIN_THREADS,
            'max': cls.MAX_THREADS,
            'default': cls.DEFAULT_THREADS
        }


# Environment-based configuration
def get_env_setting(name, default=None):
    """Get setting from environment variable"""
    return os.environ.get(name, default)

# Example usage:
# settings = Settings()
# user_agents = settings.get_user_agents()
# thread_limits = settings.get_thread_limits()
