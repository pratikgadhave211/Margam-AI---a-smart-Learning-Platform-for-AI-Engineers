"use client";

import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0d1117] text-white">
      <div className="max-w-3xl text-center space-y-8">
        <h1 className="text-6xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 pb-2">
          Margam AI
        </h1>
        <p className="text-xl text-gray-400">
          The ultimate Zero-to-Hero platform for AI Engineers. Master LLMs, RAG, and Agentic Systems through real-world coding challenges.
        </p>
        
        <div className="pt-8">
          <Link 
            href="/questions"
            className="inline-block px-8 py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-bold text-lg transition-all hover:scale-105 shadow-lg shadow-blue-900/50"
          >
            Start the Curriculum 🚀
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
          <div className="p-6 bg-[#161b22] border border-[#30363d] rounded-xl">
            <h3 className="font-bold text-green-400 text-lg mb-2">🟢 The Basics</h3>
            <p className="text-gray-400 text-sm">Master prompt engineering, structured outputs, and basic token management.</p>
          </div>
          <div className="p-6 bg-[#161b22] border border-[#30363d] rounded-xl">
            <h3 className="font-bold text-yellow-400 text-lg mb-2">🟡 RAG Systems</h3>
            <p className="text-gray-400 text-sm">Build production-grade retrieval pipelines with Hybrid Search and Re-ranking.</p>
          </div>
          <div className="p-6 bg-[#161b22] border border-[#30363d] rounded-xl">
            <h3 className="font-bold text-red-400 text-lg mb-2">🔴 AI Agents</h3>
            <p className="text-gray-400 text-sm">Architect ReAct loops and multi-agent orchestrators from scratch.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
