#!/usr/bin/env python3
"""
Launcher to run the ddos_tool package from the root directory.
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
if SRC not in sys.path:
    sys.path.insert(0, SRC)


def main():
    """Main function to handle command line arguments and launch the tool"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--use-free-proxies":
            try:
                try:
                    from ddos_tool.client.ddos_client import create_ddos_client
                    from ddos_tool.utils.validators import validate_url, validate_threads
                except ImportError:
                    from src.ddos_tool.client.ddos_client import create_ddos_client
                    from src.ddos_tool.utils.validators import validate_url, validate_threads

                print("DDoS Penetration Testing Tool with Proxy Support")
                print("=" * 50)
                print("WARNING: Authorized testing only!")
                print("Only use on systems you own or have explicit permission to test")
                print("=" * 50)

                if len(sys.argv) >= 4:
                    target = sys.argv[2]
                    threads = int(sys.argv[3]) if len(sys.argv) > 3 else 10
                else:
                    target = input("Enter target URL (include http://): ")
                    threads = int(input("Enter number of threads (default 10): ") or "10")

                print(f"\nCreating DDoS client for {target} with {threads} threads")
                client = create_ddos_client(target, threads)
                client.use_sample_free_proxies()
                client.attack()

            except ImportError as e:
                print(f"Import error: {e}")
                print("Make sure you're in the correct directory and dependencies are installed")
                print("Current working directory:", os.getcwd())
                print("Python path:", sys.path[:5])
            except Exception as e:
                print(f"Error: {e}")

        elif sys.argv[1] == "--use-paid-proxies":
            try:
                try:
                    from ddos_tool.client.ddos_client import create_ddos_client
                    from ddos_tool.utils.validators import validate_url, validate_threads
                except ImportError:
                    from src.ddos_tool.client.ddos_client import create_ddos_client
                    from src.ddos_tool.utils.validators import validate_url, validate_threads

                print("DDoS Penetration Testing Tool with Paid Proxy Support")
                print("=" * 50)
                print("WARNING: Authorized testing only!")
                print("Only use on systems you own or have explicit permission to test")
                print("=" * 50)

                if len(sys.argv) >= 4:
                    target = sys.argv[2]
                    threads = int(sys.argv[3]) if len(sys.argv) > 3 else 10
                else:
                    target = input("Enter target URL (include http://): ")
                    threads = int(input("Enter number of threads (default 10): ") or "10")

                print(f"\nCreating DDoS client for {target} with {threads} threads")
                client = create_ddos_client(target, threads)

                if not client.use_paid_proxies():
                    print("Cannot proceed without paid proxies configured. Exiting.")
                    return

                client.attack()

            except ImportError as e:
                print(f"Import error: {e}")
                print("Make sure you're in the correct directory and dependencies are installed")
                print("Current working directory:", os.getcwd())
                print("Python path:", sys.path[:5])
            except Exception as e:
                print(f"Error: {e}")
        else:
            try:
                import runpy
                try:
                    runpy.run_module("ddos_tool.ddos_tool", run_name="__main__")
                except ImportError:
                    try:
                        runpy.run_module("src.ddos_tool.ddos_tool", run_name="__main__")
                    except ImportError:
                        ddos_tool_path = os.path.join(SRC, "ddos_tool", "ddos_tool.py")
                        if os.path.exists(ddos_tool_path):
                            runpy.run_path(ddos_tool_path, run_name="__main__")
                        else:
                            print("Could not find ddos_tool module")
                            print("Please ensure the project structure is correct")
            except Exception as e:
                print(f"Error running main module: {e}")
    else:
        try:
            import runpy
            try:
                runpy.run_module("ddos_tool.ddos_tool", run_name="__main__")
            except ImportError:
                try:
                    runpy.run_module("src.ddos_tool.ddos_tool", run_name="__main__")
                except ImportError:
                    ddos_tool_path = os.path.join(SRC, "ddos_tool", "ddos_tool.py")
                    if os.path.exists(ddos_tool_path):
                        runpy.run_path(ddos_tool_path, run_name="__main__")
                    else:
                        print("Could not find ddos_tool module")
                        print("Please ensure the project structure is correct")
        except Exception as e:
            print(f"Error running main module: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print("DDoS Penetration Testing Tool")
        print("Usage:")
        print("  python main.py                     - Run normal interface")
        print("  python main.py --use-free-proxies  - Run with sample free proxies")
        print("  python main.py --use-paid-proxies  - Run with paid proxies")
        print("  python main.py --use-free-proxies <target> <threads> - Direct free proxy mode")
        print("  python main.py --use-paid-proxies <target> <threads> - Direct paid proxy mode")
        print("")
        print("Examples:")
        print("  python main.py")
        print("  python main.py --use-free-proxies")
        print("  python main.py --use-paid-proxies")
        print("  python main.py --use-free-proxies http://localhost:8000 20")
        print("  python main.py --use-paid-proxies http://localhost:8000 20")
    else:
        main()
