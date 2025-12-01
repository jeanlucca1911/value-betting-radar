"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function RegisterPage() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        setLoading(true);

        try {
            const res = await fetch("http://localhost:8000/api/v1/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || "Registration failed");
            }

            // Auto-login after successful registration
            const formData = new FormData();
            formData.append("username", email);
            formData.append("password", password);

            const loginRes = await fetch("http://localhost:8000/api/v1/auth/token", {
                method: "POST",
                body: formData,
            });

            if (loginRes.ok) {
                const data = await loginRes.json();
                localStorage.setItem("access_token", data.access_token);
                router.push("/");
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : "Registration failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-900">
            <div className="max-w-md w-full space-y-8 p-8 bg-slate-800 rounded-lg border border-slate-700">
                <div>
                    <h2 className="text-center text-3xl font-bold text-slate-100">
                        Create your account
                    </h2>
                    <p className="mt-2 text-center text-sm text-slate-400">
                        Or{" "}
                        <Link href="/login" className="font-medium text-emerald-400 hover:text-emerald-300">
                            sign in to existing account
                        </Link>
                    </p>
                </div>
                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    {error && (
                        <div className="bg-red-900/20 border border-red-500 text-red-400 px-4 py-3 rounded">
                            {error}
                        </div>
                    )}
                    <div className="space-y-4">
                        <div>
                            <label htmlFor="email" className="sr-only">
                                Email address
                            </label>
                            <input
                                id="email"
                                name="email"
                                type="email"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="appearance-none rounded relative block w-full px-3 py-2 border border-slate-600 bg-slate-900 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
                                placeholder="Email address"
                            />
                        </div>
                        <div>
                            <label htmlFor="password" className="sr-only">
                                Password
                            </label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="appearance-none rounded relative block w-full px-3 py-2 border border-slate-600 bg-slate-900 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
                                placeholder="Password"
                            />
                        </div>
                        <div>
                            <label htmlFor="confirm-password" className="sr-only">
                                Confirm Password
                            </label>
                            <input
                                id="confirm-password"
                                name="confirm-password"
                                type="password"
                                required
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                className="appearance-none rounded relative block w-full px-3 py-2 border border-slate-600 bg-slate-900 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
                                placeholder="Confirm Password"
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-emerald-600 hover:bg-emerald-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50"
                    >
                        {loading ? "Creating account..." : "Create account"}
                    </button>
                </form>
            </div>
        </div>
    );
}
