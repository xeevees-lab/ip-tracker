#!/usr/bin/env python3

import requests
import json
import sys
import os
import socket
import datetime
import argparse
from colorama import Fore, Style, init

# Try optional imports
try:
    from tabulate import tabulate
    TABULATE = True
except ImportError:
    TABULATE = False

try:
    import dns.resolver
    import dns.reversename
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}
  ██╗██████╗     ████████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
  ██║██╔══██╗    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
  ██║██████╔╝       ██║   ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
  ██║██╔═══╝        ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
  ██║██║            ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
  ╚═╝╚═╝            ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{Fore.YELLOW}           [ IP Geolocation & Intelligence Tool ]
{Fore.RED}           [ For Educational & Ethical Use Only  ]
{Style.RESET_ALL}
"""

def print_banner():
    print(BANNER)

def resolve_domain_to_ip(target):
    """Convert domain name to IP address."""
    try:
        ip = socket.gethostbyname(target)
        print(f"{Fore.GREEN}[+] Resolved {target} → {ip}")
        return ip
    except socket.gaierror:
        print(f"{Fore.RED}[-] Could not resolve domain: {target}")
        return None

def validate_ip(ip):
    """Basic IP address format validation."""
    parts = ip.split('.')
    if len(parts) == 4:
        try:
            return all(0 <= int(p) <= 255 for p in parts)
        except ValueError:
            return False
    return False

def get_my_ip():
    """Get your own public IP address."""
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=5)
        return r.json()["ip"]
    except:
        return None

def lookup_ip(ip):
    """
    Look up geolocation data for an IP using ip-api.com (free, no key needed).
    Returns a dict of results or None on failure.
    """
    url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query,reverse,mobile,proxy,hosting"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("status") == "success":
            return data
        else:
            print(f"{Fore.RED}[-] API Error: {data.get('message', 'Unknown error')}")
            return None
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}[-] No internet connection.")
        return None
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}[-] Request timed out.")
        return None

def reverse_dns(ip):
    """Get the hostname from an IP via reverse DNS lookup."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        return "N/A"

def port_scan(ip, ports="21,22,23,25,53,80,110,143,443,3306,3389,8080"):
    """Run a basic port scan using nmap."""
    if not NMAP_AVAILABLE:
        return None
    try:
        nm = nmap.PortScanner()
        print(f"\n{Fore.YELLOW}[*] Running port scan on {ip} (this may take a moment)...")
        nm.scan(ip, ports, arguments='-T4 --open')
        results = []
        if ip in nm.all_hosts():
            for proto in nm[ip].all_protocols():
                lport = nm[ip][proto].keys()
                for port in lport:
                    state = nm[ip][proto][port]['state']
                    service = nm[ip][proto][port]['name']
                    results.append((port, proto.upper(), state, service))
        return results
    except Exception as e:
        print(f"{Fore.RED}[-] Port scan failed: {e}")
        return None

def display_results(data, hostname=None, ports=None):
    """Display the geolocation results in a formatted table."""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}  📍 GEOLOCATION RESULTS FOR: {Fore.WHITE}{data['query']}")
    print(f"{Fore.CYAN}{'='*60}\n")

    rows = [
        ["🌐 IP Address",      data.get("query", "N/A")],
        ["🏳️  Country",         f"{data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})"],
        ["🗺️  Region",          data.get("regionName", "N/A")],
        ["🏙️  City",            data.get("city", "N/A")],
        ["📮 ZIP Code",         data.get("zip", "N/A")],
        ["📍 Latitude",         data.get("lat", "N/A")],
        ["📍 Longitude",        data.get("lon", "N/A")],
        ["⏰ Timezone",         data.get("timezone", "N/A")],
        ["📡 ISP",              data.get("isp", "N/A")],
        ["🏢 Organization",     data.get("org", "N/A")],
        ["🔢 AS Number",        data.get("as", "N/A")],
        ["🔁 Reverse DNS",      hostname or data.get("reverse", "N/A")],
        ["📱 Mobile",           "Yes" if data.get("mobile") else "No"],
        ["🔒 Proxy/VPN",        "Yes" if data.get("proxy") else "No"],
        ["🖥️  Hosting/DC",      "Yes" if data.get("hosting") else "No"],
        ["🗺️  Google Maps",
         f"https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}"],
    ]

    if TABULATE:
        print(tabulate(rows, headers=["Field", "Value"], tablefmt="fancy_grid"))
    else:
        for row in rows:
            print(f"  {Fore.GREEN}{row[0]:<20}{Fore.WHITE}{row[1]}")

    if ports is not None:
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}  🔍 OPEN PORTS")
        print(f"{Fore.CYAN}{'='*60}")
        if ports:
            port_rows = [(p, proto, state, svc) for p, proto, state, svc in ports]
            if TABULATE:
                print(tabulate(port_rows,
                    headers=["Port", "Protocol", "State", "Service"],
                    tablefmt="fancy_grid"))
            else:
                for p, proto, state, svc in port_rows:
                    print(f"  {Fore.GREEN}{p}/{proto}  {state}  {svc}")
        else:
            print(f"  {Fore.RED}No open ports found.")

def save_report(data, hostname=None, ports=None, filename=None):
    """Save results to a text report file."""
    if not filename:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{data['query']}_{ts}.txt"

    with open(filename, 'w') as f:
        f.write(f"IP TRACKER REPORT\n")
        f.write(f"Generated: {datetime.datetime.now()}\n")
        f.write("="*50 + "\n\n")
        f.write(f"Target IP     : {data.get('query','N/A')}\n")
        f.write(f"Country       : {data.get('country','N/A')} ({data.get('countryCode','N/A')})\n")
        f.write(f"Region        : {data.get('regionName','N/A')}\n")
        f.write(f"City          : {data.get('city','N/A')}\n")
        f.write(f"ZIP           : {data.get('zip','N/A')}\n")
        f.write(f"Latitude      : {data.get('lat','N/A')}\n")
        f.write(f"Longitude     : {data.get('lon','N/A')}\n")
        f.write(f"Timezone      : {data.get('timezone','N/A')}\n")
        f.write(f"ISP           : {data.get('isp','N/A')}\n")
        f.write(f"Organization  : {data.get('org','N/A')}\n")
        f.write(f"AS Number     : {data.get('as','N/A')}\n")
        f.write(f"Reverse DNS   : {hostname or data.get('reverse','N/A')}\n")
        f.write(f"Mobile        : {'Yes' if data.get('mobile') else 'No'}\n")
        f.write(f"Proxy/VPN     : {'Yes' if data.get('proxy') else 'No'}\n")
        f.write(f"Hosting/DC    : {'Yes' if data.get('hosting') else 'No'}\n")
        f.write(f"Maps Link     : https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}\n")

        if ports:
            f.write("\n--- OPEN PORTS ---\n")
            for p, proto, state, svc in ports:
                f.write(f"  {p}/{proto}  {state}  {svc}\n")

    print(f"\n{Fore.GREEN}[+] Report saved to: {Fore.WHITE}{filename}")

def bulk_lookup(filepath, do_scan=False, save=False):
    """Look up multiple IPs from a file (one per line)."""
    if not os.path.exists(filepath):
        print(f"{Fore.RED}[-] File not found: {filepath}")
        return
    with open(filepath, 'r') as f:
        targets = [line.strip() for line in f if line.strip()]

    print(f"{Fore.YELLOW}[*] Loaded {len(targets)} targets from {filepath}\n")
    for target in targets:
        print(f"\n{Fore.MAGENTA}{'─'*50}")
        print(f"{Fore.CYAN}[>] Tracking: {target}")
        # Resolve if domain
        if not validate_ip(target):
            ip = resolve_domain_to_ip(target)
            if not ip:
                continue
        else:
            ip = target
        data = lookup_ip(ip)
        if data:
            hostname = reverse_dns(ip)
            ports = port_scan(ip) if do_scan else None
            display_results(data, hostname, ports)
            if save:
                save_report(data, hostname, ports)

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="IP Geolocation & Intelligence Tool",
        epilog="Examples:\n"
               "  python3 ip_tracker.py -t 8.8.8.8\n"
               "  python3 ip_tracker.py -t google.com\n"
               "  python3 ip_tracker.py -t 8.8.8.8 --scan\n"
               "  python3 ip_tracker.py -t 8.8.8.8 --save\n"
               "  python3 ip_tracker.py --myip\n"
               "  python3 ip_tracker.py --bulk targets.txt\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-t", "--target",  help="Single IP address or domain to look up")
    parser.add_argument("--scan",          help="Run port scan on target", action="store_true")
    parser.add_argument("--save",          help="Save results to a report file", action="store_true")
    parser.add_argument("--myip",          help="Show your own public IP location", action="store_true")
    parser.add_argument("--bulk",          help="File with list of IPs/domains (one per line)", metavar="FILE")

    args = parser.parse_args()

    # ── Your own IP ─────────────────────────────────────────────
    if args.myip:
        print(f"{Fore.YELLOW}[*] Fetching your public IP...")
        my_ip = get_my_ip()
        if my_ip:
            print(f"{Fore.GREEN}[+] Your Public IP: {Fore.WHITE}{my_ip}")
            data = lookup_ip(my_ip)
            if data:
                hostname = reverse_dns(my_ip)
                ports = port_scan(my_ip) if args.scan else None
                display_results(data, hostname, ports)
                if args.save:
                    save_report(data, hostname, ports)
        return

    # ── Bulk mode ───────────────────────────────────────────────
    if args.bulk:
        bulk_lookup(args.bulk, do_scan=args.scan, save=args.save)
        return

    # ── Single target ───────────────────────────────────────────
    if args.target:
        target = args.target.strip()

        # Resolve domain → IP if needed
        if not validate_ip(target):
            print(f"{Fore.YELLOW}[*] Resolving domain...")
            ip = resolve_domain_to_ip(target)
            if not ip:
                sys.exit(1)
        else:
            ip = target

        print(f"{Fore.YELLOW}[*] Looking up {ip}...\n")
        data = lookup_ip(ip)

        if data:
            hostname = reverse_dns(ip)
            ports = port_scan(ip) if args.scan else None
            display_results(data, hostname, ports)
            if args.save:
                save_report(data, hostname, ports)
    else:
        # Interactive mode if no args given
        print(f"{Fore.YELLOW}No arguments given. Entering interactive mode.\n")
        target = input(f"{Fore.CYAN}Enter IP address or domain: {Fore.WHITE}").strip()
        if not validate_ip(target):
            ip = resolve_domain_to_ip(target)
            if not ip:
                sys.exit(1)
        else:
            ip = target
        data = lookup_ip(ip)
        if data:
            hostname = reverse_dns(ip)
            scan_choice = input(f"\n{Fore.CYAN}Run port scan? (y/n): {Fore.WHITE}").lower() == 'y'
            ports = port_scan(ip) if scan_choice else None
            display_results(data, hostname, ports)
            save_choice = input(f"\n{Fore.CYAN}Save report? (y/n): {Fore.WHITE}").lower() == 'y'
            if save_choice:
                save_report(data, hostname, ports)

if __name__ == "__main__":
    main()
