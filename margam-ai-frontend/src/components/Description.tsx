import React from 'react';

interface DescriptionProps {
  questionData: any;
}

export default function Description({ questionData }: DescriptionProps) {
  const desc = questionData.description;

  return (
    <div className="p-6 text-gray-300 font-sans">
      {/* Scenario Section */}
      <div className="mb-8">
        <h2 className="text-xl font-bold text-white mb-2">Scenario</h2>
        {desc?.scenario ? (
          <p className="leading-relaxed text-sm">{desc.scenario}</p>
        ) : (
          <div className="p-3 bg-red-900/20 border border-red-500/50 rounded-md text-red-400 text-sm italic">
            ⚠️ No scenario provided for this question.
          </div>
        )}
      </div>

      {/* Tasks Section */}
      <div className="mb-10">
        <h2 className="text-xl font-bold text-white mb-3">The Task</h2>
        {desc?.tasks && desc.tasks.length > 0 ? (
          <ol className="list-decimal pl-5 space-y-3 text-sm">
            {desc.tasks.map((task: string, idx: number) => (
              <li key={idx} className="leading-relaxed pl-1">
                <span 
                  dangerouslySetInnerHTML={{ 
                    __html: task.replace(/`([^`]+)`/g, '<code class="bg-[#161b22] px-1.5 py-0.5 rounded text-blue-300 font-mono text-xs border border-[#30363d]">$1</code>') 
                  }} 
                />
              </li>
            ))}
          </ol>
        ) : (
          <div className="p-3 bg-red-900/20 border border-red-500/50 rounded-md text-red-400 text-sm italic">
            ⚠️ No tasks provided for this question.
          </div>
        )}
      </div>

      {/* Examples Section */}
      <div className="mt-10 space-y-6">
        <h2 className="text-xl font-bold text-white mb-3">Examples</h2>
        {questionData.examples?.length > 0 ? (
          questionData.examples.map((ex: any, idx: number) => (
            <div key={idx} className="space-y-2">
              <h3 className="font-bold text-gray-300 text-md">Example {idx + 1}:</h3>
              <div className="bg-[#161b22] border-l-4 border-gray-500 p-4 text-sm font-mono text-gray-300 rounded-r-md leading-relaxed">
                <p><span className="font-bold text-white">Input:</span> {ex.input}</p>
                <p><span className="font-bold text-white">Output:</span> {ex.output}</p>
                {ex.explanation && (
                  <p className="mt-2">
                    <span className="font-bold text-white font-sans">Explanation:</span>{" "}
                    <span className="font-sans">{ex.explanation}</span>
                  </p>
                )}
              </div>
            </div>
          ))
        ) : (
          <div className="text-sm text-gray-500 italic">No examples provided.</div>
        )}
      </div>

      {/* Hints Section */}
      <div className="mt-12 space-y-3">
        <h2 className="text-xl font-bold text-white mb-3">Hints</h2>
        {questionData.hints?.length > 0 ? (
          questionData.hints.map((hint: string, idx: number) => (
            <details key={idx} className="group cursor-pointer">
              <summary className="flex items-center text-sm font-medium text-gray-400 hover:text-gray-200 transition-colors bg-[#161b22] px-4 py-3 rounded-md border border-[#30363d] list-none select-none">
                <span className="mr-2">💡</span> Hint {idx + 1}
                <span className="ml-auto transform transition-transform group-open:rotate-180 text-xs">▼</span>
              </summary>
              <div className="px-10 py-4 text-sm text-gray-300 bg-[#0d1117] border border-t-0 border-[#30363d] rounded-b-md -mt-1 font-sans">
                {hint}
              </div>
            </details>
          ))
        ) : (
          <div className="text-sm text-gray-500 italic">No hints available.</div>
        )}
      </div>
    </div>
  );
}
