import concurrent.futures
import ipaddress
import platform
import socket
import subprocess
import re

from mac_vendor import get_vendor
from port_scanner import scan_ports


try:
    from scapy.all import ARP, Ether, srp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False


def _ping_host(ip: str, timeout_ms: int = 1000) -> bool:
    if platform.system() == "Windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout_ms), ip]
    else:
        cmd = ["ping", "-c", "1", "-W", str(max(1, timeout_ms // 1000)), ip]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=(timeout_ms / 1000) + 1,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False
    


def _fallback_scan(network: str):
    try:
        net = ipaddress.ip_network(network, strict=False)
    except ValueError:
        net = ipaddress.ip_network("192.168.1.0/24")

    devices = []
    hosts = [str(ip) for ip in net.hosts()]

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        alive_results = list(executor.map(_ping_host, hosts))

    for ip, is_alive in zip(hosts, alive_results):
        if not is_alive:
            continue

        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except OSError:
            hostname = "Unknown"

        try:
            result = subprocess.run(
                ["arp", "-a", ip],
                capture_output=True,
                text=True,
                timeout=5
            )

            match = re.search(
                r'([0-9a-fA-F]{2}(?:-[0-9a-fA-F]{2}){5})',
                result.stdout,
            )

            if match:
                mac_address = match.group(1)
        except Exception:
            pass

        # Get vendor from MAC
        vendor = (
            get_vendor(mac_address)
            if mac_address != "Unknown"
            else "Unknown"
        )

        ports = scan_ports(ip)
        device_type = "Unknown"

        if ip.endswith(".1"):
            device_type = "Router"
        elif hostname.lower().startswith("desktop"):
            device_type = "Windows PC"
        elif hostname.lower().startswith("laptop"):
            device_type = "Laptop"
        elif any(
            brand in vendor.lower()
            for brand in [
                "tp-link",
                "d-link",
                "netgear",
                "cisco",
                "mikrotik",
                "huawei",
            ]
        ):
            device_type = "Router"
        elif any(port["service"] == "Printer" for port in ports):
            device_type = "Printer"
        elif any(
            port["service"] in ["SMB", "RDP", "WinRM"]
            for port in ports
        ):
            device_type = "Windows Device"

        devices.append({
            "hostname": hostname,
            "ip": ip,
            "mac": mac_address,
            "vendor": vendor,
            "device_type": device_type,
            "ports": ports,
        })

    return devices


def scan_network(network="192.168.1.0/24"):
    if not SCAPY_AVAILABLE:
        return _fallback_scan(network)

    try:
        arp = ARP(pdst=network)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=2, verbose=0)[0]


        devices = []

        for _, received in result:
            ip = received.psrc
            
            
            result = subprocess.run(
                ["arp", "-a", ip],
                capture_output=True,
                text=True,  
                timeout=5
            )

            arp_output = result.stdout

            match = re.search(r'([0-9a-fA-F]{2}(?:-[0-9a-fA-F]{2}){5})', arp_output)

            if match:
                mac_address = match.group(1)

                print(f"IP: {ip}, MAC: {mac_address}")

            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except OSError:
                hostname = "Unknown"

            vendor = get_vendor(mac_address)
            ports = scan_ports(ip)
            device_type = "Unknown"

            if ip.endswith(".1"):
                device_type = "Router"
            elif hostname.lower().startswith("desktop"):
                device_type = "Windows PC"
            elif hostname.lower().startswith("laptop"):
                device_type = "Laptop"
            elif any(
                brand in vendor.lower()
                for brand in [
                    "tp-link",
                    "d-link",
                    "netgear",
                    "cisco",
                    "mikrotik",
                    "huawei",
                ]
            ):
                device_type = "Router"
            elif any(port["service"] == "Printer" for port in ports):
                device_type = "Printer"
            elif any(port["service"] in ["SMB", "RDP", "WinRM"] for port in ports):
                device_type = "Windows Device"

            devices.append({
                "hostname": hostname,
                "ip": ip,
                "mac": mac_address,
                "vendor": vendor,
                "device_type": device_type,
                "ports": ports,
            })

        return devices

    except Exception as exc:
        error_text = str(exc).lower()
        if "winpcap" in error_text or "layer 2" in error_text:
            return _fallback_scan(network)
        raise
