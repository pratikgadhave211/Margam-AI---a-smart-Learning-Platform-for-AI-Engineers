import { questionsList } from "@/lib/curriculum/questions";
import { getSolvedQuestionIds } from "./actions";
import Link from "next/link";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

export default async function QuestionsDashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session?.user) {
    redirect("/auth");
  }

  const solvedIds = await getSolvedQuestionIds();
  const solvedCount = solvedIds.length;
  const totalCount = questionsList.length;

  return (
    <div className="min-h-screen bg-[#0d1117] text-white p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header section matching Leetcode aesthetic */}
        <div className="flex justify-between items-center bg-[#161b22] p-6 rounded-xl border border-[#30363d] shadow-lg">
          <div>
            <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
              Welcome back, {session.user.name}
            </h1>
            <p className="text-gray-400 mt-2">Ready to master AI Engineering?</p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-400 uppercase tracking-wider font-bold mb-1">Progress</p>
            <div className="text-2xl font-bold text-green-400">{solvedCount} / {totalCount} <span className="text-gray-500 text-lg">Solved</span></div>
          </div>
        </div>

        {/* Filter Bar (Static for now, but UI matches) */}
        <div className="flex space-x-3 mb-6 overflow-x-auto pb-2">
          <button className="px-4 py-2 bg-white text-black font-semibold rounded-full text-sm">All Topics</button>
          <button className="px-4 py-2 bg-[#21262d] hover:bg-[#30363d] text-gray-300 rounded-full text-sm transition-colors border border-[#30363d]">LangChain</button>
          <button className="px-4 py-2 bg-[#21262d] hover:bg-[#30363d] text-gray-300 rounded-full text-sm transition-colors border border-[#30363d]">Pydantic</button>
          <button className="px-4 py-2 bg-[#21262d] hover:bg-[#30363d] text-gray-300 rounded-full text-sm transition-colors border border-[#30363d]">Easy</button>
          <button className="px-4 py-2 bg-[#21262d] hover:bg-[#30363d] text-gray-300 rounded-full text-sm transition-colors border border-[#30363d]">Medium</button>
        </div>

        {/* Questions Table */}
        <div className="bg-[#0d1117] rounded-xl border border-[#30363d] overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#161b22] border-b border-[#30363d]">
                <th className="p-4 font-semibold text-gray-400 w-16 text-center">Status</th>
                <th className="p-4 font-semibold text-gray-400">Title</th>
                <th className="p-4 font-semibold text-gray-400 w-32">Difficulty</th>
              </tr>
            </thead>
            <tbody>
              {questionsList.map((q, idx) => {
                const isSolved = solvedIds.includes(q.id);
                return (
                  <tr key={q.id} className={`border-b border-[#21262d] hover:bg-[#161b22] transition-colors ${idx % 2 === 0 ? 'bg-[#0d1117]' : 'bg-[#0f1419]'}`}>
                    <td className="p-4 text-center">
                      {isSolved ? (
                        <span className="text-green-500 font-bold text-lg">✅</span>
                      ) : (
                        <span className="text-gray-600">-</span>
                      )}
                    </td>
                    <td className="p-4">
                      <Link href={`/questions/${q.id}`} className="text-blue-400 hover:text-blue-300 hover:underline font-medium text-lg">
                        {q.title}
                      </Link>
                      <div className="flex gap-2 mt-2">
                        {q.topics.map(t => (
                          <span key={t} className="text-xs bg-[#21262d] text-gray-400 px-2 py-1 rounded-md">{t}</span>
                        ))}
                      </div>
                    </td>
                    <td className="p-4">
                      <span className={`font-semibold ${q.difficulty === 'Easy' ? 'text-green-400' : q.difficulty === 'Medium' ? 'text-yellow-400' : 'text-red-500'}`}>
                        {q.difficulty}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

      </div>
    </div>
  );
}
