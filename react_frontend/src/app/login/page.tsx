"use client";

import { useState, useEffect } from "react";
import { toast } from "react-toastify";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: { preventDefault: () => void; }) => {
    e.preventDefault();

    try {
      setLoading(true);
      const response = await fetch("http://localhost:8080/api/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: email,
          password,
        }),
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      const data = await response.json();

      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);

      toast.success("Login successful!", {
                      position: "top-right",
                      autoClose: 5000,
                  });
      window.location.href = "http://localhost:3000"

    } catch (error) {
      toast.error("Login failed. Please check your credentials.", {
                      position: "top-right",
                      autoClose: 5000,
                  });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-white to-emerald-50 p-6">
      <div className="w-full max-w-md bg-white/90 backdrop-blur-md border border-gray-200 rounded-2xl shadow-lg p-8">
        <div className="flex flex-col items-center gap-4 mb-4">
          <img src="/images/default.png" alt="BrokerX Logo" />
        </div>

        <form className="flex flex-col gap-5" onSubmit={handleSubmit} aria-label="login form">

          <div className="relative">
            <input
              id="email"
              name="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder=" "
              className="peer w-full rounded-xl border border-gray-200 px-4 pt-6 pb-3 bg-white text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 transition"
              aria-label="Email"
              required
            />
            <label
              htmlFor="email"
              className="absolute left-4 top-3 text-base text-slate-500 transition-all duration-150
                peer-placeholder-shown:top-3 peer-placeholder-shown:text-base peer-placeholder-shown:text-slate-500
                peer-focus:-top-5 peer-focus:text-xs peer-focus:text-emerald-700
                peer-valid:-top-3 peer-valid:text-xs peer-valid:text-emerald-700"
            >
              Email
            </label>
          </div>

          <div className="relative">
            <input
              id="password"
              name="password"
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder=" "
              className="peer w-full rounded-xl border border-gray-200 px-4 pt-6 pb-3 bg-white text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-emerald-600 transition"
              aria-label="Password"
              required
            />
            <label
              htmlFor="password"
              className="absolute left-4 top-3 text-base text-slate-500 transition-all duration-150
                peer-placeholder-shown:top-3 peer-placeholder-shown:text-base peer-placeholder-shown:text-slate-500
                peer-focus:-top-5 peer-focus:text-xs peer-focus:text-emerald-700
                peer-valid:-top-3 peer-valid:text-xs peer-valid:text-emerald-700"
            >
              Password
            </label>

            <button
              type="button"
              onClick={() => setShowPassword((s) => !s)}
              className="absolute right-3 top-5 text-xs text-emerald-700 hover:text-emerald-900 focus:outline-none"
              aria-pressed={showPassword}
              aria-label={showPassword ? "Hide password" : "Show password"}
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>

          <div className="flex items-center justify-between text-sm">
            <a className="text-slate-600 hover:underline" href="/create_account">Create account</a>
          </div>

          <button
            className={`mt-1 py-3 rounded-xl text-white font-medium transition-transform duration-150 shadow-sm
              ${loading ? "bg-emerald-300 cursor-not-allowed" : "bg-emerald-700 hover:bg-emerald-800 active:scale-95"}`}
            type="submit"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign in"}
          </button>

        </form>
      </div>
    </div>
  );
}