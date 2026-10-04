"use client";

import { useState } from "react";
import { authClient } from "@/lib/auth-client";

type AuthState = "login" | "signup" | "forgot_password";

export default function AuthPage() {
  const [authState, setAuthState] = useState<AuthState>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleGoogleSignIn = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await authClient.signIn.social({ 
        provider: "google",
        callbackURL: "/"
      });
      if (res.error) {
        setError(res.error.message || "Failed to sign in with Google.");
      }
    } catch (err: any) {
      setError(err.message || "Network error during sign in.");
    } finally {
      setLoading(false);
    }
  };

  const handleEmailAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      if (authState === "login") {
        const res = await authClient.signIn.email({ email, password });
        if (res.error) throw new Error(res.error.message);
        window.location.href = "/";
      } else if (authState === "signup") {
        const res = await authClient.signUp.email({ email, password, name });
        if (res.error) throw new Error(res.error.message);
        setAuthState("login");
        setSuccess("Account created successfully. Please log in.");
      } else if (authState === "forgot_password") {
        const res = await authClient.forgetPassword({ email, redirectTo: "/auth/reset" });
        if (res.error) throw new Error(res.error.message);
        setSuccess("Password reset email sent! Please check your inbox.");
      }
    } catch (err: any) {
      setError(err.message || "Authentication failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0d1117] text-gray-200 relative overflow-hidden">
      {/* Premium Background Gradients */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[100px] pointer-events-none" />

      {/* Auth Card */}
      <div className="relative z-10 w-full max-w-md p-8 bg-[#161b22]/80 backdrop-blur-xl border border-[#30363d] rounded-2xl shadow-2xl">
        
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-white mb-2 tracking-tight">
            Margam AI
          </h1>
          <p className="text-gray-400 text-sm">
            {authState === "login" && "Welcome back! Please enter your details."}
            {authState === "signup" && "Create your account to start learning."}
            {authState === "forgot_password" && "Reset your password securely."}
          </p>
        </div>

        {/* Social Auth */}
        {authState !== "forgot_password" && (
          <div className="mb-6">
            <button
              onClick={handleGoogleSignIn}
              disabled={loading}
              className="w-full flex items-center justify-center gap-3 py-2.5 px-4 bg-white hover:bg-gray-100 text-gray-900 font-semibold rounded-lg transition-colors shadow-sm disabled:opacity-70 disabled:cursor-not-allowed"
            >
              <svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
                <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z" />
                <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z" />
                <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z" />
                <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z" />
              </svg>
              Continue with Google
            </button>

            <div className="flex items-center my-6">
              <div className="flex-grow border-t border-[#30363d]"></div>
              <span className="px-3 text-xs text-gray-500 uppercase font-medium">Or</span>
              <div className="flex-grow border-t border-[#30363d]"></div>
            </div>
          </div>
        )}

        {/* Alerts */}
        {error && <div className="mb-4 p-3 rounded-md bg-red-900/20 border border-red-900/50 text-red-400 text-sm font-medium">{error}</div>}
        {success && <div className="mb-4 p-3 rounded-md bg-green-900/20 border border-green-900/50 text-green-400 text-sm font-medium">{success}</div>}

        {/* Email Form */}
        <form onSubmit={handleEmailAuth} className="space-y-4">
          {authState === "signup" && (
            <div>
              <label className="block text-xs font-semibold text-gray-400 mb-1.5 uppercase">Full Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="w-full bg-[#0d1117] border border-[#30363d] focus:border-blue-500 focus:ring-1 focus:ring-blue-500 rounded-lg px-4 py-2.5 text-white placeholder-gray-500 transition-colors outline-none"
                placeholder="John Doe"
              />
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-gray-400 mb-1.5 uppercase">Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full bg-[#0d1117] border border-[#30363d] focus:border-blue-500 focus:ring-1 focus:ring-blue-500 rounded-lg px-4 py-2.5 text-white placeholder-gray-500 transition-colors outline-none"
              placeholder="you@example.com"
            />
          </div>

          {authState !== "forgot_password" && (
            <div>
              <div className="flex justify-between items-center mb-1.5">
                <label className="block text-xs font-semibold text-gray-400 uppercase">Password</label>
                {authState === "login" && (
                  <button
                    type="button"
                    onClick={() => setAuthState("forgot_password")}
                    className="text-xs text-blue-400 hover:text-blue-300 font-medium transition-colors"
                  >
                    Forgot password?
                  </button>
                )}
              </div>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full bg-[#0d1117] border border-[#30363d] focus:border-blue-500 focus:ring-1 focus:ring-blue-500 rounded-lg px-4 py-2.5 text-white placeholder-gray-500 transition-colors outline-none"
                placeholder="••••••••"
              />
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 mt-2 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg transition-colors shadow-md disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {loading ? "Processing..." : authState === "login" ? "Sign In" : authState === "signup" ? "Create Account" : "Send Reset Link"}
          </button>
        </form>

        {/* Footer Toggles */}
        <div className="mt-8 text-center text-sm text-gray-400">
          {authState === "login" ? (
            <p>
              Don't have an account?{" "}
              <button onClick={() => setAuthState("signup")} className="text-blue-400 hover:text-blue-300 font-semibold transition-colors">
                Sign up
              </button>
            </p>
          ) : (
            <p>
              Already have an account?{" "}
              <button onClick={() => setAuthState("login")} className="text-blue-400 hover:text-blue-300 font-semibold transition-colors">
                Log in
              </button>
            </p>
          )}
        </div>

      </div>
    </div>
  );
}
