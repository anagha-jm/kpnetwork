def classify_device(open_ports):

    ports = {p["port"] for p in open_ports}

    if 445 in ports or 135 in ports:
        return "Windows Device"

    if 3389 in ports:
        return "Windows Workstation"

    if 80 in ports or 443 in ports:
        return "Web Device"

    if 22 in ports:
        return "Linux Device"

    return "Unknown Device"

def classify_device(hostname, ip):

    hostname = hostname.lower()

    if ip.endswith(".1"):
        return "Router"

    if "desktop" in hostname:
        return "Windows PC"

    if "laptop" in hostname:
        return "Laptop"

    return "Unknown Device"