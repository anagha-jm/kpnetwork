import socket

COMMON_PORTS = {
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP",
    5985: "WinRM",
    9100: "Printer",
    554: "RTSP Camera"
}


def scan_ports(ip):

    open_ports = []

    for port, service in COMMON_PORTS.items():

        try:

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(0.5)

            result = sock.connect_ex(
                (ip, port)
            )

            if result == 0:

                open_ports.append({
                    "port": port,
                    "service": service
                })

            sock.close()

        except:
            pass

    return open_ports