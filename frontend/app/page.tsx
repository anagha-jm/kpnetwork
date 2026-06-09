import Link from "next/link";
import Navbar from "./components/Navbar";

export default function Home() {

  return (
    <>
      <Navbar />
      <main className="p-6">
        <div className="mx-auto max-w-4xl space-y-6">
          <section className="rounded-xl border bg-white p-8 shadow-sm">
            <h1 className="text-4xl font-bold mb-4">Network Inventory Dashboard</h1>
            <p className="text-base text-gray-600">
              Scan your network, view discovered devices, and inspect device details.
            </p>
          </section>

          <section className="grid gap-4 sm:grid-cols-2">
            <Link
              href="/network"
              className="rounded-xl border bg-blue-600 px-6 py-8 text-center text-white shadow-sm transition hover:bg-blue-700"
            >
              <h2 className="text-2xl font-semibold">Network Scan</h2>
              <p className="mt-2">Discover devices on your local network.</p>
            </Link>
            <Link
              href={`/ip`}
              className="rounded-xl border bg-gray-100 px-6 py-8 text-center text-gray-900 shadow-sm transition hover:bg-gray-200"
            >
              <h2 className="text-2xl font-semibold">Device Details</h2>
              <p className="mt-2">Open a device details page by IP address.</p>
            </Link>
          </section>
        </div>
      </main>
    </>
  );
}