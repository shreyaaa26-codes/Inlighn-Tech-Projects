import subprocess
import ipaddress
import socket
import platform
import re

def ping(ip):
    """Ping an IP address to check if it's alive."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", str(ip)]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def get_arp_table():
    """Get the ARP table and parse IP-MAC mappings."""
    arp_output = subprocess.check_output("arp -a", shell=True).decode()
    arp_entries = []
    for line in arp_output.splitlines():
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([-\w]+)", line)
        if match:
            ip, mac = match.groups()
            if mac != "ff-ff-ff-ff-ff-ff":
                arp_entries.append((ip, mac))
    return dict(arp_entries)

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

def scan_network(cidr):
    print("Scanning network... Please wait.\n")
    active_ips = []
    arp_table = {}

    network = ipaddress.ip_network(cidr, strict=False)
    for ip in network.hosts():
        if ping(ip):
            active_ips.append(str(ip))

    arp_table = get_arp_table()

    print("IP Address".ljust(20) + "MAC Address".ljust(20) + "Hostname")
    print("-" * 60)
    for ip in active_ips:
        mac = arp_table.get(ip, "Unknown")
        hostname = get_hostname(ip)
        print(ip.ljust(20) + mac.ljust(20) + hostname)

if __name__ == "__main__":
    cidr = input("Enter network CIDR (e.g., 192.168.1.0/24): ")
    try:
        ipaddress.ip_network(cidr)  # validate
        scan_network(cidr)
    except ValueError:
        print("Invalid CIDR format.")
