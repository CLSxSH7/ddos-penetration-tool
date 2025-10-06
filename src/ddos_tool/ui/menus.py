"""
User interface menus for the DDoS tool
"""

import sys
from ddos_tool.core.ddos_client import DDoSClient
from ddos_tool.ui.validators import get_target, get_thread_count


def show_main_menu():
    """Display the main menu"""
    ddos_client = None

    while True:
        print("\n" + "=" * 50)
        print("     DDoS PENETRATION TESTING TOOL")
        print("=" * 50)
        print("WARNING: Authorized testing only!")
        print("Only use on systems you own or have explicit permission to test")
        print("=" * 50)
        print("1. Configure and Start Attack")
        print("2. Exit")
        print("-" * 50)

        choice = input("Select an option: ").strip()

        if choice == "1":
            # Configure attack
            if ddos_client is None:
                target = get_target()
                threads = get_thread_count()
                ddos_client = DDoSClient(target, threads)

            show_attack_menu(ddos_client)

        elif choice == "2":
            # Exit
            print("[+] Exiting...")
            sys.exit(0)

        else:
            print("[!] Invalid option. Please try again.")


def show_attack_menu(ddos_client):
    """Display attack configuration menu"""
    while True:
        print("\n" + "=" * 50)
        print("     ATTACK CONFIGURATION")
        print("=" * 50)
        print(f"Target: {ddos_client.target}")
        print(f"Threads: {ddos_client.num_threads}")
        print("=" * 50)
        print("1. Start Attack")
        print("2. Change Target")
        print("3. Change Thread Count")
        print("4. Back to Main Menu")
        print("-" * 50)

        attack_choice = input("Select an option: ").strip()

        if attack_choice == "1":
            try:
                ddos_client.attack()
            except Exception as e:
                print(f"[!] Attack failed: {str(e)}")

        elif attack_choice == "2":
            target = get_target()
            ddos_client.target = ddos_client._format_target(target)
            print(f"[+] Target updated to: {ddos_client.target}")

        elif attack_choice == "3":
            threads = get_thread_count()
            ddos_client.num_threads = threads
            print(f"[+] Thread count updated to: {threads}")

        elif attack_choice == "4":
            break

        else:
            print("[!] Invalid option. Please try again.")
