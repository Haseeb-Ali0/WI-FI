
#!/usr/bin/env python3

import os
import time
import socket
import platform
import urllib.request
import urllib.error
import statistics

# Terminal colors
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
WHITE = "\033[97m"
RESET = "\033[0m"

DOWNLOAD_URL = (
    "https://speed.cloudflare.com/__down?bytes=5000000"
)


def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")


def show_banner():
    clear_screen()

    print(CYAN + r"""
███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝
██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ 
██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗ 
██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
       WI-FI CHECKER v1.0
    """ + RESET)

    print(BLUE + "=" * 46 + RESET)
    print(GREEN + " [+] MODE   : NETWORK DIAGNOSTICS" + RESET)
    print(GREEN + " [+] OWNER  : Haseeb Ali" + RESET)
    print(GREEN + " [+] SYSTEM : " + platform.system() + RESET)
    print(BLUE + "=" * 46 + RESET)


def check_internet():
    print(CYAN + "\n[+] Checking internet connection..." + RESET)

    try:
        with socket.create_connection(
            ("1.1.1.1", 443), timeout=4
        ):
            print(GREEN + "[OK] Internet is connected!" + RESET)
            return True

    except OSError:
        print(RED + "[!] Internet connection failed." + RESET)
        return False


def system_information():
    print(CYAN + "\n[+] SYSTEM INFORMATION" + RESET)
    print(WHITE + "-" * 35 + RESET)

    print("Operating System :", platform.platform())
    print("Python Version   :", platform.python_version())
    print("Computer Name    :", platform.node())
    print("Architecture     :", platform.machine())

    input("\nPress Enter to return to menu...")


def latency_test():
    print(CYAN + "\n[+] LATENCY SCANNER" + RESET)
    print("Testing connection to 1.1.1.1...")

    samples = []

    for attempt in range(5):
        start = time.perf_counter()

        try:
            with socket.create_connection(
                ("1.1.1.1", 443), timeout=4
            ):
                elapsed = (time.perf_counter() - start) * 1000
                samples.append(elapsed)
                print(
                    GREEN
                    + f"Test {attempt + 1}: {elapsed:.2f} ms"
                    + RESET
                )

        except OSError:
            print(RED + f"Test {attempt + 1}: Failed" + RESET)

        time.sleep(0.2)

    if samples:
        print(
            GREEN
            + f"\nAverage latency: {statistics.mean(samples):.2f} ms"
            + RESET
        )
    else:
        print(RED + "\nLatency test failed." + RESET)

    input("\nPress Enter to return to menu...")


def wifi_speed_test():
    print(CYAN + "\n[+] WI-FI SPEED SCANNER" + RESET)
    print(YELLOW + "Downloading a test file (about 5 MB)..." + RESET)

    try:
        request = urllib.request.Request(
            DOWNLOAD_URL,
            headers={
                "User-Agent": "WI-FI-Checker/1.0",
                "Cache-Control": "no-cache",
            },
        )

        start = time.perf_counter()
        total_bytes = 0

        with urllib.request.urlopen(request, timeout=25) as response:
            while True:
                data = response.read(65536)

                if not data:
                    break

                total_bytes += len(data)

        elapsed = max(time.perf_counter() - start, 0.001)

        if total_bytes == 0:
            print(RED + "No data received." + RESET)
        else:
            speed = total_bytes * 8 / elapsed / 1_000_000

            print(BLUE + "\n" + "=" * 38 + RESET)
            print(GREEN + "       SPEED TEST RESULTS" + RESET)
            print(BLUE + "=" * 38 + RESET)

            print(
                WHITE
                + f"Download Speed : {speed:.2f} Mbps"
                + RESET
            )
            print(
                WHITE
                + f"Data Downloaded: {total_bytes / 1_000_000:.2f} MB"
                + RESET
            )
            print(
                WHITE
                + f"Time Taken     : {elapsed:.2f} seconds"
                + RESET
            )

            print(BLUE + "=" * 38 + RESET)

    except urllib.error.HTTPError as error:
        print(RED + f"Server returned HTTP {error.code}." + RESET)
        print(YELLOW + "The speed-test server may block the request." + RESET)

    except (urllib.error.URLError, OSError, TimeoutError) as error:
        print(RED + f"Speed test failed: {error}" + RESET)

    input("\nPress Enter to return to menu...")


def public_ip_check():
    print(CYAN + "\n[+] PUBLIC IP CHECK" + RESET)

    try:
        request = urllib.request.Request(
            "https://api.ipify.org",
            headers={"User-Agent": "WI-FI-Checker/1.0"},
        )

        with urllib.request.urlopen(request, timeout=8) as response:
            ip = response.read(100).decode().strip()

        print(GREEN + "Public IP: " + ip + RESET)

    except (urllib.error.URLError, OSError, TimeoutError) as error:
        print(RED + f"Could not get public IP: {error}" + RESET)

    input("\nPress Enter to return to menu...")


def main_menu():
    while True:
        show_banner()

        print(CYAN + "\n[ NETWORK TOOLKIT ]" + RESET)
        print(WHITE + "[1] Check Internet Connection" + RESET)
        print(WHITE + "[2] System Information" + RESET)
        print(WHITE + "[3] Wi-Fi Internet Speed Test" + RESET)
        print(WHITE + "[4] Latency Test" + RESET)
        print(WHITE + "[5] Public IP Check" + RESET)
        print(RED + "[6] Exit" + RESET)

        print(BLUE + "\n" + "-" * 46 + RESET)

        choice = input(
            GREEN + "root@wifi-checker ~> " + RESET
        ).strip()

        if choice == "1":
            check_internet()
            input("\nPress Enter to return to menu...")

        elif choice == "2":
            system_information()

        elif choice == "3":
            wifi_speed_test()

        elif choice == "4":
            latency_test()

        elif choice == "5":
            public_ip_check()

        elif choice == "6":
            print(GREEN + "\n[+] WI-FI Checker closed. Goodbye!" + RESET)
            break

        else:
            print(RED + "\n[!] Invalid option. Choose 1 to 6." + RESET)
            time.sleep(1)


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(YELLOW + "\n\n[!] Tool stopped by user." + RESET)
