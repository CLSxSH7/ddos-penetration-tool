#!/usr/bin/env python3
"""
Main entry point for the DDoS Penetration Testing Tool
"""

import sys
import os

# Add src to path for relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ddos_tool.ui.menus import show_main_menu


def main():
    """Main application entry point"""
    try:
        show_main_menu()
    except KeyboardInterrupt:
        print("\n[+] Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
