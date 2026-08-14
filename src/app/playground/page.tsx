"use client";
import React, { useState } from 'react';
import Link from 'next/link';

export default function Playground() {
  const [output, setOutput] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [code, setCode] = useState('// Welcome to the Doomslang Playground!\n\nint a = 10;\nint b = 20;\nprint("Sum is:", a + b);\n');

  const handleRun = async () => {
    setIsExecuting(true);
    setOutput('');
    try {
      const response = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      });
      const data = await response.json();
      if (data.output) {
        setOutput(data.output);
      } else if (data.error) {
        setOutput(data.error);
      } else {
        setOutput('No output received.');
      }
    } catch (err: any) {
      setOutput('Failed to execute code: ' + err.message);
    } finally {
      setIsExecuting(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Handle tab character insertion
    if (e.key === 'Tab') {
      e.preventDefault();
      const target = e.target as HTMLTextAreaElement;
      const start = target.selectionStart;
      const end = target.selectionEnd;
      
      setCode(code.substring(0, start) + '    ' + code.substring(end));
      
      // Put caret at right position again
      setTimeout(() => {
        target.selectionStart = target.selectionEnd = start + 4;
      }, 0);
    }
  };

  return (
    <div className="h-screen max-h-screen text-[#ededed] flex flex-col overflow-hidden">
      {/* Navigation Bar */}
      <nav className="border-b border-white/10 bg-[#0a0a0a]/90 backdrop-blur-md py-4 shadow-2xl z-50">
        <div className="max-w-[1600px] mx-auto flex justify-between items-center px-6 w-full">
          <Link href="/" className="flex items-center gap-2 text-2xl font-bold tracking-tighter text-white">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
            Doomslang
          </Link>
          <div className="flex items-center gap-6">
            <span className={`text-sm flex items-center gap-2 font-medium ${isExecuting ? 'text-yellow-400' : 'text-green-400'}`}>
              <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${isExecuting ? 'bg-yellow-400 animate-pulse' : 'bg-green-400 shadow-[0_0_8px_rgba(74,222,128,0.5)]'}`}></span>
              <span className="hidden sm:inline">{isExecuting ? 'Running...' : 'Engine Ready'}</span>
            </span>
            <button 
              onClick={handleRun}
              disabled={isExecuting}
              className={`btn-primary py-2! px-6! flex items-center gap-2 ${isExecuting && 'opacity-50 cursor-not-allowed'}`}
            >
              {isExecuting ? (
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="none"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
              )}
              {isExecuting ? 'Executing' : 'Run Code'}
            </button>
          </div>
        </div>
      </nav>

      {/* Editor & Terminal Layout */}
      <main className="flex-1 flex flex-col md:flex-row min-h-0">
        {/* Editor Pane */}
        <div className="flex-1 border-b md:border-b-0 md:border-r border-white/10 bg-[#121212] relative flex flex-col min-h-0">
           <div className="bg-[#1a1a1a] text-gray-400 text-xs py-2 px-4 border-b border-white/10 font-mono flex justify-between items-center shrink-0">
             <span className="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                main.dooms
             </span>
             <span>Doomslang Playground</span>
           </div>
           <div className="relative flex-1 min-h-0 overflow-auto">
             <textarea 
               value={code}
               onChange={(e) => setCode(e.target.value)}
               onKeyDown={handleKeyDown}
               spellCheck={false}
               className="absolute inset-0 w-full h-full bg-transparent text-[#e6e6e6] font-mono p-6 resize-none focus:outline-none focus:ring-0 text-base leading-relaxed whitespace-pre"
               style={{ tabSize: 4 }}
             />
           </div>
        </div>

        {/* Terminal Pane */}
        <div className="flex-1 bg-[#0a0a0a] relative flex flex-col min-h-0">
          <div className="bg-[#1a1a1a] text-gray-400 text-xs py-2 px-4 border-b border-white/10 font-mono shrink-0 flex items-center gap-2">
             <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="4 17 10 11 4 5"></polyline><line x1="12" y1="19" x2="20" y2="19"></line></svg>
             Terminal Output
           </div>
           <div className="flex-1 p-6 overflow-y-auto">
             {output ? (
               <pre className="font-mono text-sm text-gray-300 whitespace-pre-wrap leading-relaxed">{output}</pre>
             ) : (
               <div className="text-gray-600 font-mono text-sm italic h-full flex items-center justify-center">
                 Click "Run Code" to see the output here...
               </div>
             )}
           </div>
        </div>
      </main>
    </div>
  );
}
