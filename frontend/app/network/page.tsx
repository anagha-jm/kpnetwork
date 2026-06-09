"use client";

import { useState } from "react";
import Navbar from "../components/Navbar";
import Link from "next/link";

export default function NetworkPage() {

  const [devices, setDevices] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const scanNetwork = async () => {

    setLoading(true);
    setError("");

    try {

      const response = await fetch(
        "http://127.0.0.1:5000/api/network-scan"
      );

      const data = await response.json();

      console.log("Network Scan Response:", data);

      if (
        data.status === "success" &&
        Array.isArray(data.devices)
      ) {

        setDevices(data.devices);

      } else {

        setDevices([]);

        setError(
          data.message ||
          "Invalid response from server"
        );
      }

    } catch (err) {

      console.error(err);

      setDevices([]);

      setError(
        "Could not connect to backend server."
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <>
      <Navbar />

      <div className="p-6">

        <h1 className="text-3xl font-bold mb-6">
          Network Devices
        </h1>

        <button
          onClick={scanNetwork}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          {loading ? "Scanning..." : "Scan Network"}
        </button>

        {error && (
          <div className="mt-4 p-3 border rounded bg-red-100 text-red-700">
            {error}
          </div>
        )}

        <table className="mt-6 w-full border border-collapse">

          <thead className="bg-gray-100">

            <tr>

              <th className="border p-2">
                Hostname
              </th>

              <th className="border p-2">
                IP Address
              </th>

              <th className="border p-2">
                MAC Address
              </th>

              <th className="border p-2">
                Vendor
              </th>

              <th className="border p-2">
                Device Type
              </th>

            </tr>

          </thead>

          <tbody>

            {devices.length > 0 ? (

              devices.map((device, index) => (

                <tr key={index}>

                  <td className="border p-2">

                    <Link
                      href={`/ip/${device.ip}`}
                      className="text-blue-600 hover:underline"
                    >
                      {device.hostname || "Unknown"}
                    </Link>

                  </td>

                  <td className="border p-2">
                    {device.ip || "-"}
                  </td>

                  <td className="border p-2">
                    {device.mac || "-"}
                  </td>

                  <td className="border p-2">
                    {device.vendor || "Unknown"}
                  </td>

                  <td className="border p-2">
                    {device.device_type || "Unknown"}
                  </td>

                </tr>

              ))

            ) : (

              !loading && (

                <tr>

                  <td
                    colSpan={5}
                    className="border p-4 text-center"
                  >
                    Click "Scan Network" to discover devices.
                  </td>

                </tr>

              )

            )}

          </tbody>

        </table>

      </div>
    </>
  );
}