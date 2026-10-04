"use client";

import { useState, useEffect, useRef } from "react";
import { useParams } from "next/navigation";
import Editor from "@monaco-editor/react";
import { saveSubmission, getMySubmissions, getSolutionCode } from "./actions";
import Description from "@/components/Description";

export default function QuestionPage() {
  const params = useParams();
  const { difficulty, questionId } = params as { difficulty: string, questionId: string };
  
  const [questionData, setQuestionData] = useState<any>(null);
  const [code, setCode] = useState<string>("");
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [isTabLoading, setIsTabLoading] = useState<boolean>(false);
  
  // Tabs State
  const [activeTab, setActiveTab] = useState<"description" | "solutions" | "submissions">("description");
  const [submissions, setSubmissions] = useState<any[]>([]);
  const [solution, setSolution] = useState<string | null>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/v1/questions/${difficulty}/${questionId}`, {
      credentials: "include"
    })
      .then(async (res) => {
        if (!res.ok) {
          const errText = await res.text();
          throw new Error(`HTTP ${res.status}: ${errText}`);
        }
        return res.json();
      })
      .then((data) => {
        setQuestionData(data);
        setCode(data.starter_code);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load question:", err);
        setLoading(false);
      });
  }, [difficulty, questionId]);

  const loadSubmissions = async () => {
    setIsTabLoading(true);
    const subs = await getMySubmissions(`${difficulty}/${questionId}`);
    setSubmissions(subs);
    setIsTabLoading(false);
  };

  const loadSolution = async () => {
    setIsTabLoading(true);
    const sol = await getSolutionCode(`${difficulty}/${questionId}`);
    setSolution(sol);
    setIsTabLoading(false);
  };

  useEffect(() => {
    if (activeTab === "submissions") {
      loadSubmissions();
    } else if (activeTab === "solutions") {
      loadSolution();
    }
  }, [activeTab]);

  const handleSubmit = async () => {
    setSubmitting(true);
    setResults(null);
    try {
      const res = await fetch(
        `http://localhost:8000/api/v1/questions/${difficulty}/${questionId}/evaluate`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({ code }),
        }
      );
      const data = await res.json();
      setResults(data);
      
      // Save to database asynchronously
      await saveSubmission({
        questionId: `${difficulty}/${questionId}`,
        code: code,
        status: data.status || "FAILURE",
        score: data.points_earned || 0
      });

      if (activeTab === "submissions") {
        loadSubmissions();
      }
    } catch (err) {
      console.error(err);
      setResults({ status: "FAILURE", error: "Failed to connect to grading server." });
    }
    setSubmitting(false);
  };

  const wsRef = useRef<WebSocket | null>(null);
  const resolversRef = useRef<Record<string, (val: any) => void>>({});

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/api/v1/autocomplete/ws");
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.id && resolversRef.current[data.id]) {
        resolversRef.current[data.id](data);
        delete resolversRef.current[data.id];
      }
    };
    wsRef.current = ws;
    return () => ws.close();
  }, []);

  const handleEditorMount = (editor: any, monaco: any) => {
    monaco.languages.registerCompletionItemProvider("python", {
      triggerCharacters: ["."],
      provideCompletionItems: async (model: any, position: any) => {
        if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return { suggestions: [] };
        const code = model.getValue();
        const wordInfo = model.getWordUntilPosition(position);
        const reqId = Date.now().toString() + Math.random().toString();
        
        return new Promise((resolve) => {
          resolversRef.current[reqId] = (data: any) => {
            const kindMap: Record<string, any> = {
              function: monaco.languages.CompletionItemKind.Method,
              class: monaco.languages.CompletionItemKind.Class,
              module: monaco.languages.CompletionItemKind.Module,
            };
            const suggestions = data.suggestions.map((s: any) => ({
              label: s.label,
              kind: kindMap[s.kind] || monaco.languages.CompletionItemKind.Property,
              insertText: s.insertText,
              range: {
                startLineNumber: position.lineNumber,
                endLineNumber: position.lineNumber,
                startColumn: wordInfo.startColumn,
                endColumn: wordInfo.endColumn
              }
            }));
            resolve({ suggestions });
          };
          wsRef.current?.send(JSON.stringify({ id: reqId, code, line: position.lineNumber, column: position.column - 1 }));
        });
      },
    });
  };

  if (loading) return <div className="p-8 text-white">Loading question...</div>;
  if (!questionData) return <div className="p-8 text-red-500">Failed to load question. Does it exist?</div>;

  return (
    <div className="flex h-screen bg-[#0d1117] text-white overflow-hidden">
      {/* Left Pane: Tabs (Description, Solutions, Submissions) */}
      <div className="w-1/2 flex flex-col border-r border-[#30363d] h-full overflow-hidden">
        {/* Tab Header */}
        <div className="flex bg-[#161b22] border-b border-[#30363d] pt-2 px-2 shrink-0">
          <button 
            onClick={() => setActiveTab("description")}
            className={`px-4 py-2 font-semibold text-sm rounded-t-lg transition-colors ${activeTab === "description" ? "bg-[#0d1117] text-white border-t border-l border-r border-[#30363d]" : "text-gray-400 hover:text-white"}`}
          >
            Description
          </button>
          <button 
            onClick={() => setActiveTab("solutions")}
            className={`px-4 py-2 font-semibold text-sm rounded-t-lg transition-colors ${activeTab === "solutions" ? "bg-[#0d1117] text-white border-t border-l border-r border-[#30363d]" : "text-gray-400 hover:text-white"}`}
          >
            Solutions
          </button>
          <button 
            onClick={() => setActiveTab("submissions")}
            className={`px-4 py-2 font-semibold text-sm rounded-t-lg transition-colors ${activeTab === "submissions" ? "bg-[#0d1117] text-white border-t border-l border-r border-[#30363d]" : "text-gray-400 hover:text-white"}`}
          >
            Submissions
          </button>
        </div>

        {/* Tab Content */}
        <div className="flex-grow overflow-y-auto bg-[#0d1117]">
          {activeTab === "description" && (
            <>
              <div className="p-4 border-b border-[#30363d] shrink-0">
                <h1 className="text-2xl font-bold text-blue-400">{questionData.title}</h1>
                <div className="flex gap-4 mt-2">
                  <span className="px-2 py-1 bg-green-900/30 text-green-400 text-xs font-bold rounded-md capitalize">
                    {questionData.difficulty}
                  </span>
                  <span className="px-2 py-1 bg-purple-900/30 text-purple-400 text-xs font-bold rounded-md">
                    Max Points: {questionData.max_points}
                  </span>
                </div>
              </div>
              <Description questionData={questionData} />
            </>
          )}

          {activeTab === "solutions" && (
            <div className="p-6">
              <h2 className="text-xl font-bold text-green-400 mb-4">Official Solution</h2>
              {isTabLoading ? (
                <div className="animate-pulse flex space-x-4">
                  <div className="flex-1 space-y-4 py-1">
                    <div className="h-4 bg-[#30363d] rounded w-3/4"></div>
                    <div className="h-4 bg-[#30363d] rounded w-1/2"></div>
                    <div className="h-4 bg-[#30363d] rounded w-5/6"></div>
                  </div>
                </div>
              ) : solution ? (
                <div className="bg-[#161b22] border border-[#30363d] rounded-xl overflow-hidden">
                  <div className="bg-[#21262d] px-4 py-2 text-xs text-gray-400 font-mono border-b border-[#30363d]">
                    solution.py
                  </div>
                  <pre className="p-4 text-sm font-mono text-gray-300 overflow-x-auto whitespace-pre-wrap">
                    {solution}
                  </pre>
                </div>
              ) : (
                <p className="text-gray-500">Solution not available.</p>
              )}
            </div>
          )}

          {activeTab === "submissions" && (
            <div className="p-6">
              <h2 className="text-xl font-bold mb-4">Your Submissions</h2>
              {isTabLoading ? (
                <div className="animate-pulse space-y-3">
                  <div className="h-20 bg-[#30363d] rounded-lg w-full"></div>
                  <div className="h-20 bg-[#30363d] rounded-lg w-full"></div>
                </div>
              ) : submissions.length === 0 ? (
                <p className="text-gray-500">You haven't submitted any code yet.</p>
              ) : (
                <div className="space-y-3">
                  {submissions.map((sub, idx) => (
                    <div 
                      key={sub.id} 
                      className={`p-4 rounded-lg border cursor-pointer hover:bg-opacity-80 transition-all ${sub.status === 'SUCCESS' ? 'border-green-900/50 bg-green-900/10' : 'border-red-900/50 bg-red-900/10'}`}
                      onClick={() => setCode(sub.code)}
                    >
                      <div className="flex justify-between items-center">
                        <span className={`font-bold ${sub.status === 'SUCCESS' ? 'text-green-400' : 'text-red-400'}`}>
                          {sub.status === 'SUCCESS' ? 'Accepted' : 'Failed'}
                        </span>
                        <span className="text-sm text-gray-400">
                          {new Date(sub.createdAt).toLocaleString()}
                        </span>
                      </div>
                      <p className="text-sm text-gray-300 mt-1">Score: {sub.score}</p>
                      <p className="text-xs text-blue-400 mt-2 hover:underline">Click to restore code</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Right Pane: Editor & Results */}
      <div className="w-1/2 flex flex-col h-full overflow-hidden">
        {/* Editor Section (Top Half) */}
        <div className="flex flex-col flex-grow min-h-0 border-b border-[#30363d]">
          <div className="bg-[#161b22] px-4 py-2 border-b border-[#30363d] text-sm text-gray-400 font-mono shrink-0">
            editor.py
          </div>
          <div className="flex-grow relative">
            <div className="absolute inset-0">
              <Editor
                height="100%"
                defaultLanguage="python"
                theme="vs-dark"
                value={code}
                onChange={(value) => setCode(value || "")}
                onMount={handleEditorMount}
                options={{
                  minimap: { enabled: false },
                  fontSize: 15,
                  padding: { top: 16 },
                  scrollBeyondLastLine: false,
                }}
              />
            </div>
          </div>
        </div>

        {/* Results Panel (Bottom Half) */}
        <div className="h-[35%] min-h-[250px] shrink-0 bg-[#0d1117] flex flex-col">
          <div className="p-3 border-b border-[#30363d] bg-[#161b22] flex justify-between items-center shrink-0">
            <h3 className="font-semibold text-gray-300">Execution Results</h3>
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className={`px-5 py-2 rounded-md text-sm font-bold transition-colors shadow-lg ${
                submitting
                  ? "bg-gray-600 text-gray-400 cursor-not-allowed"
                  : "bg-green-600 hover:bg-green-500 text-white"
              }`}
            >
              {submitting ? "Running..." : "Submit Code"}
            </button>
          </div>
          <div className="p-4 overflow-y-auto flex-grow text-sm">
            {!results && <p className="text-gray-500 italic">Run your code to see test results.</p>}
            
            {results && results.status === "FAILURE" && results.error && (
              <div className="text-red-400 p-3 bg-red-900/20 rounded-md whitespace-pre-wrap font-mono border border-red-900/50">
                {results.error}
              </div>
            )}

            {results && results.test_results && results.test_results.length > 0 && (
              <div className="space-y-4">
                <div className="flex items-center gap-4 mb-4">
                  <span className={`px-3 py-1 rounded-md font-bold text-lg ${results.status === 'SUCCESS' ? 'bg-green-900/50 text-green-400 border border-green-500/30' : 'bg-red-900/50 text-red-400 border border-red-500/30'}`}>
                    {results.status}
                  </span>
                  <span className="text-gray-300 font-semibold">
                    Score: {results.points_earned} / {results.max_points} Points
                  </span>
                </div>

                <div className="grid grid-cols-1 gap-3">
                  {results.test_results.map((tc: any, i: number) => (
                    <div key={i} className={`p-4 rounded-md border ${tc.passed ? 'border-green-900/50 bg-green-900/10' : 'border-red-900/50 bg-red-900/10'}`}>
                      <div className="font-semibold mb-1 flex items-center gap-2">
                        <span>{tc.passed ? '✅' : '❌'}</span>
                        <span className={tc.passed ? 'text-green-400' : 'text-red-400'}>Test Case {i + 1}</span>
                      </div>
                      {!tc.passed && tc.mismatches && tc.mismatches.length > 0 && (
                        <ul className="list-disc pl-7 mt-2 text-red-300 space-y-1 font-mono text-xs">
                          {tc.mismatches.map((m: string, j: number) => (
                            <li key={j}>{m}</li>
                          ))}
                        </ul>
                      )}
                    </div>
                  ))}
                </div>

                {results.summary && results.summary.feedback && (
                  <div className="mt-4 p-4 border border-blue-900/50 bg-blue-900/10 rounded-md">
                    <h4 className="font-bold text-blue-400 mb-1 flex items-center gap-2">
                      <span>🤖</span> AI Mentor Feedback
                    </h4>
                    <p className="text-gray-300 mt-2">{results.summary.feedback}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
