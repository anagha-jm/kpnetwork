from network_scanner import scan_network


def get_dashboard_stats():

    devices = scan_network()

    total = len(devices)

    windows = 0
    routers = 0
    unknown = 0

    for device in devices:

        device_type = device["device_type"]

        if device_type == "Windows PC":
            windows += 1

        elif device_type == "Router":
            routers += 1

        else:
            unknown += 1

    return {
        "total_devices": total,
        "windows_devices": windows,
        "routers": routers,
        "unknown_devices": unknown
    }