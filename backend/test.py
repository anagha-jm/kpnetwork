import subprocess
import re

result = subprocess.run(
    ["arp", "-a", "192.168.1.58"],
    capture_output=True,
    text=True,   # Get output as a string
    timeout=5
)

arp_output = result.stdout

match = re.search(r'([0-9a-fA-F]{2}(?:-[0-9a-fA-F]{2}){5})', arp_output)

if match:
    mac_address = match.group(1)
    print("MAC Address:", mac_address)
else:
    print("MAC address not found")