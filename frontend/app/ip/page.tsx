"use client";

import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { useParams } from "next/navigation";

export default function DevicePage() {
  const [device, setDevice] = useState<any>(null);
  const [error, setError] = useState("");


  useEffect(() => {
    const fetchDeviceDetails = async () => {
      const res = await fetch(`http://127.0.0.1:5000/api/device`)

      const data = await res.json();
      setDevice(data);
    }

    fetchDeviceDetails()
  }, [])

  if (error) {
    return (
      <>
        <Navbar />
        <div className="p-6 text-red-700">{error}</div>
      </>
    );
  }

  if (!device) {
    return (
      <>
        <Navbar />
        <div className="p-6">Loading device details...</div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="p-6 space-y-4">
        <h1 className="text-3xl font-bold">Device Details</h1>
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <p>
            <strong>Hostname:</strong> {device.hostname || "Unknown"}
          </p>
          <p>
            <strong>IP Address:</strong> {device.ip || "Unknown"}
          </p>
          <p>
            <strong>MAC Address:</strong> {device.mac || "Unknown"}
          </p>
          <p>
            <strong>OS:</strong> {device.os || "Unknown"}
          </p>
          <p>
            <strong> RAM Percentage:</strong> {device.ram_percent || "Unknown"}
          </p>
               <p>
            <strong> RAM gb:</strong> {device.ram_total_gb || "Unknown"}
          </p>
               <p>
            <strong> CPU Percentage:</strong> {device.cpu || "Unknown"}
          </p>
        </div>
      </div>
    </>
  );
}
