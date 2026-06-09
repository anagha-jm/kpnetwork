import socket
import uuid
import platform
import psutil

def get_device_info():
    hostname = socket.gethostname()

    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "Unknown"

    mac_address = ':'.join(
        ['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
         for ele in range(0, 8 * 6, 8)][::-1]
    )

    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()

    return {
        "hostname": hostname,
        "ip": ip_address,
        "mac": mac_address,
        "cpu": cpu_usage,
        "ram_percent": ram.percent,
        "ram_total_gb": round(ram.total / (1024 ** 3), 2),
        "os": platform.platform()
    }