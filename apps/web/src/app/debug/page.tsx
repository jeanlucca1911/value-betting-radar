"use client";

import { API_BASE_URL } from "@/lib/api";

export default function DebugPage() {
    return (
        <div className="min-h-screen bg-slate-900 text-white p-8">
            <h1 className="text-3xl font-bold mb-4">Debug Info</h1>
            <div className="bg-slate-800 p-6 rounded-lg">
                <h2 className="text-xl font-semibold mb-2">API Configuration</h2>
                <p className="mb-2">
                    <strong>API_BASE_URL:</strong> <code className="bg-slate-700 px-2 py-1 rounded">{API_BASE_URL}</code>
                </p>
                <p className="mb-2">
                    <strong>NEXT_PUBLIC_API_URL:</strong> <code className="bg-slate-700 px-2 py-1 rounded">{process.env.NEXT_PUBLIC_API_URL || 'Not set'}</code>
                </p>
                <button
                    onClick={async () => {
                        try {
                            const res = await fetch(`${API_BASE_URL}/health`);
                            const data = await res.json();
                            alert(`Success! ${JSON.stringify(data)}`);
                        } catch (err) {
                            alert(`Error: ${err}`);
                        }
                    }}
                    className="mt-4 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded"
                >
                    Test Backend Connection
                </button>
            </div>
        </div>
    );
}
