"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [metrics, setMetrics] = useState<any>(null);
  const [devices, setDevices] = useState<any[]>([]);

 useEffect(() => {
  const loadData = () => {
    fetch("http://127.0.0.1:8000/metrics")
      .then((res) => res.json())
      .then((data) => setMetrics(data))
      .catch((err) => console.error(err));

    fetch("http://127.0.0.1:8000/scan")
      .then((res) => res.json())
      .then((data) => setDevices(data))
      .catch((err) => console.error(err));
  };

  loadData();

  const interval = setInterval(loadData, 5000);

  return () => clearInterval(interval);
}, []);

  return (
    <main className="min-h-screen bg-zinc-100 p-10">
      <h1 className="text-4xl font-bold mb-8">
        KPNetwork Dashboard
      </h1>

      {!metrics ? (
        <p>Loading metrics...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl p-6 shadow">
            <h2 className="text-lg font-semibold">Hostname</h2>
            <p className="text-2xl mt-2">{metrics.hostname}</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow">
            <h2 className="text-lg font-semibold">CPU Usage</h2>
            <p className="text-2xl mt-2">{metrics.cpu_percent}%</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow">
            <h2 className="text-lg font-semibold">Memory Usage</h2>
            <p className="text-2xl mt-2">{metrics.memory_percent}%</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow">
            <h2 className="text-lg font-semibold">Disk Usage</h2>
            <p className="text-2xl mt-2">{metrics.disk_percent}%</p>
          </div>
        </div>
      )}
      <h2 className="text-2xl font-bold mt-10 mb-4">
  Devices
</h2>

<div className="space-y-3">
  {devices.map((device, index) => (
    <div
      key={index}
      className="bg-white rounded-xl p-4 shadow"
    >
      <p><strong>Hostname:</strong> {device.hostname}</p>
      <p><strong>IP:</strong> {device.ip}</p>
      <p><strong>Status:</strong> {device.status}</p>
    </div>
  ))}
</div>
    </main>
  );
}