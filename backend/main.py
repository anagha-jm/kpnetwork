from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import psutil
import socket

app = FastAPI(title="KPNetwork API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "KPNetwork Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/metrics")
def metrics():
    return {
        "hostname": socket.gethostname(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }


@app.get("/network")
def network():
    hostname = socket.gethostname()

    try:
        ip_address = socket.gethostbyname(hostname)
    except Exception:
        ip_address = "Unknown"

    return {
        "hostname": hostname,
        "ip_address": ip_address
    }


@app.get("/processes")
def processes():
    process_list = []

    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            process_list.append({
                "pid": proc.info["pid"],
                "name": proc.info["name"],
                "status": proc.info["status"]
            })
        except Exception:
            pass

    return process_list[:25]


@app.get("/scan")
def scan():
    hostname = socket.gethostname()

    try:
        ip_address = socket.gethostbyname(hostname)
    except Exception:
        ip_address = "Unknown"

    return [
        {
            "hostname": hostname,
            "ip": ip_address,
            "status": "online"
        }
    ]