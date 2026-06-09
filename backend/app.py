from flask import Flask, jsonify
from flask_cors import CORS

from device_info import get_device_info
from network_scanner import scan_network
from dashboard import get_dashboard_stats

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Network Inventory Backend Running",
        "version": "1.0"
    })


# ==========================================
# Local Device Information
# ==========================================
@app.route("/api/device")
def device():

    try:
        return jsonify(
            get_device_info()
        )

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==========================================
# Network Scan
# ==========================================
@app.route("/api/network-scan")
def network_scan():

    try:

        devices = scan_network()

        return jsonify({
            "status": "success",
            "count": len(devices),
            "devices": devices
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==========================================
# Dashboard Statistics
# ==========================================
@app.route("/api/dashboard")
def dashboard():

    try:

        stats = get_dashboard_stats()

        return jsonify({
            "status": "success",
            "data": stats
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==========================================
# Device Details by IP
# ==========================================
@app.route("/api/device/<ip>")
def device_details(ip):

    try:

        devices = scan_network()

        for device in devices:

            if device["ip"] == ip:
                return jsonify({
                    "status": "success",
                    "device": device
                })

        return jsonify({
            "status": "error",
            "message": "Device not found"
        }), 404

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==========================================
# Debug Routes
# ==========================================
@app.route("/api/health")
def health():

    return jsonify({
        "status": "running"
    })


if __name__ == "__main__":

    print("\n========== REGISTERED ROUTES ==========")
    print(app.url_map)
    print("=======================================\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )