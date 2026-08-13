"use client";
import React, { useState, useEffect } from 'react';
import Link from 'next/link';

export default function Home() {
  const [copiedInstall, setCopiedInstall] = useState(false);
  const [copiedRun, setCopiedRun] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const copyInstall = () => {
    navigator.clipboard.writeText("pip install dooms");
    setCopiedInstall(true);
    setTimeout(() => setCopiedInstall(false), 2000);
  };

  const copyRun = () => {
    navigator.clipboard.writeText("dooms run main.dooms");
    setCopiedRun(true);
    setTimeout(() => setCopiedRun(false), 2000);
  };

  return (
    <main className="min-h-screen relative overflow-hidden flex flex-col items-center pt-24 px-6 text-center">
      {/* Background ambient glow */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-purple-900/20 blur-[120px] -z-10" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-indigo-900/20 blur-[120px] -z-10" />

      {/* Navigation */}
      <nav className={`fixed top-0 left-0 w-full z-50 transition-all duration-300 ${isScrolled ? 'bg-[#0a0a0a]/90 backdrop-blur-md border-b border-white/10 py-4 shadow-2xl' : 'bg-transparent py-6'}`}>
        <div className="max-w-5xl mx-auto flex justify-between items-center px-6 md:px-12 w-full">
          <div className="flex items-center gap-2 text-2xl font-bold tracking-tighter text-white">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
            DOOMS
          </div>
          <div className="flex gap-8 items-center">
            <Link href="/playground" className="text-white hover:text-accent font-semibold transition-colors bg-white/10 px-4 py-2 rounded-lg border border-white/20 hover:border-accent flex items-center gap-2 shadow-[0_0_15px_rgba(255,255,255,0.1)] hover:shadow-[0_0_20px_var(--accent)]">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="none"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
              Playground
            </Link>
            <Link href="/docs" className="text-gray-300 hover:text-white transition-colors">Documentation</Link>
            <Link href="https://github.com/Rohan-Shinde24/Dooms" target="_blank" className="text-gray-300 hover:text-white transition-colors">GitHub</Link>
            <Link href="https://pypi.org/project/dooms/" target="_blank" className="text-gray-300 hover:text-white transition-colors">PyPI</Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-4xl w-full mt-12 opacity-0 animate-fade-in animate-delay-1 flex flex-col items-center">
        <h1 className="flex items-center gap-4 text-6xl md:text-8xl font-extrabold tracking-tight mb-6 text-white">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="currentColor" stroke="none" className="md:w-20 md:h-20"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
          DOOMS
        </h1>
        
        <p className="text-xl text-gray-400 mb-8 max-w-2xl leading-relaxed">
          A custom, strictly-typed, dynamically evaluated scripting language. Built from scratch with a robust type-checker, OOP support, and expressive syntax.
        </p>

        {/* Commands Container */}
        <div className="flex flex-col md:flex-row gap-6 mb-10">
          {/* Install Command */}
          <div className="flex items-center bg-[#0d0d0d] border border-white/10 rounded-xl px-6 py-4 shadow-2xl relative group cursor-pointer transition-all hover:border-accent" onClick={copyInstall} title="Copy Install Command">
            <span className="text-gray-500 mr-4 font-mono">$</span>
            <code className="text-white font-mono text-lg mr-8">pip install dooms</code>
            <button className="text-gray-400 hover:text-white transition-colors">
              {copiedInstall ? (
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#27c93f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              )}
            </button>
          </div>

          {/* Run Command */}
          <div className="flex items-center bg-[#0d0d0d] border border-white/10 rounded-xl px-6 py-4 shadow-2xl relative group cursor-pointer transition-all hover:border-accent" onClick={copyRun} title="Copy Run Command">
            <span className="text-gray-500 mr-4 font-mono">$</span>
            <code className="text-white font-mono text-lg mr-8">dooms run main.dooms</code>
            <button className="text-gray-400 hover:text-white transition-colors">
              {copiedRun ? (
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#27c93f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              )}
            </button>
          </div>
        </div>
        
        <div className="mb-12">
          <Link href="/playground" className="btn-primary py-3! px-8! text-lg flex items-center gap-2 shadow-[0_0_30px_rgba(139,92,246,0.3)] hover:shadow-[0_0_40px_rgba(139,92,246,0.6)]">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" stroke="none"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            Try DOOMS in Browser
          </Link>
        </div>

        <p className="text-gray-500 text-sm mb-16">Note: You must have <span className="text-white font-semibold">Python 3.11+</span> installed to run DOOMS locally.</p>

        {/* Creator Info */}
        <div className="flex flex-col items-center gap-4 mb-16">
          <p className="text-gray-300 font-medium">Created by <span className="text-white font-bold">Rohan Shinde</span></p>
          <div className="flex gap-4">
            <Link href="https://www.linkedin.com/in/rohan-shinde024" target="_blank" className="btn-secondary py-2! px-4!">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
              LinkedIn
            </Link>
            <Link href="https://github.com/Rohan-Shinde24" target="_blank" className="btn-secondary py-2! px-4!">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              GitHub
            </Link>
          </div>
        </div>
      </section>

      {/* Code Snippet Section */}
      <section className="w-full max-w-5xl mx-auto opacity-0 animate-fade-in animate-delay-2 mb-24">
        <h2 className="text-3xl font-bold mb-8">Sample Code</h2>
        <div className="grid md:grid-cols-2 gap-8 text-left">
          <div className="code-window h-full">
            <div className="code-header">
              <div className="code-dot red"></div>
              <div className="code-dot yellow"></div>
              <div className="code-dot green"></div>
            </div>
            <div className="code-content whitespace-pre">
              <span className="comment">// Strict Typing & Arithmetic</span><br/>
              <span className="type">int</span> a = <span className="type">10</span>;<br/>
              <span className="type">int</span> b = <span className="type">5</span>;<br/>
              <span className="function">print</span>(<span className="string">"Sum:"</span>, a + b);<br/>
              <br/>
              <span className="comment">// Block Scoping & Loops</span><br/>
              <span className="type">int</span> count = <span className="type">0</span>;<br/>
              <span className="keyword">while</span> (count &lt; <span className="type">3</span>) {'{\n'}
              {'    '}<span className="function">print</span>(<span className="string">"Loop:"</span>, count);<br/>
              {'    '}count = count + <span className="type">1</span>;<br/>
              {'}'}
            </div>
          </div>
          
          <div className="code-window h-full">
            <div className="code-header">
              <div className="code-dot red"></div>
              <div className="code-dot yellow"></div>
              <div className="code-dot green"></div>
            </div>
            <div className="code-content whitespace-pre">
              <span className="comment">// Classes and Objects</span><br/>
              <span className="keyword">class</span> <span className="type">Person</span> {'{\n'}
              {'    '}<span className="keyword">func</span> <span className="function">init</span>(<span className="type">str</span> name, <span className="type">int</span> age) {'{\n'}
              {'        '}<span className="keyword">this</span>.name = name;<br/>
              {'        '}<span className="keyword">this</span>.age = age;<br/>
              {'    }'}<br/>
              <br/>
              {'    '}<span className="keyword">func</span> <span className="function">greet</span>() {'{\n'}
              {'        '}<span className="function">print</span>(<span className="string">"Hi, I'm"</span>, <span className="keyword">this</span>.name);<br/>
              {'    }'}<br/>
              {'}'}<br/>
              <br/>
              <span className="type">any</span> p = <span className="function">Person</span>(<span className="string">"Rohan"</span>, <span className="type">22</span>);<br/>
              p.<span className="function">greet</span>();
            </div>
          </div>
        </div>
        <div className="mt-8">
            <Link href="/docs" className="btn-primary">Read the full Documentation</Link>
        </div>
      </section>

      {/* Features Grid */}
      <section className="w-full max-w-6xl mx-auto px-6 pb-24 text-left">
        <h2 className="text-3xl font-bold mb-12 text-center">Why use DOOMS?</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="glass-card p-8">
            <h3 className="text-xl font-semibold mb-3 text-white">Strict Type Safety</h3>
            <p className="text-gray-400">Avoid runtime crashes by strictly defining variables with <code className="text-accent bg-accent/10 px-1 rounded">int</code>, <code className="text-accent bg-accent/10 px-1 rounded">str</code>, and <code className="text-accent bg-accent/10 px-1 rounded">boo</code>. Catch errors early.</p>
          </div>
          <div className="glass-card p-8">
            <h3 className="text-xl font-semibold mb-3 text-white">Fully Featured OOP</h3>
            <p className="text-gray-400">Class declarations, <code className="text-accent bg-accent/10 px-1 rounded">init()</code> constructors, and <code className="text-accent bg-accent/10 px-1 rounded">this</code> context binding natively supported for complex programs.</p>
          </div>
          <div className="glass-card p-8">
            <h3 className="text-xl font-semibold mb-3 text-white">Data Structures</h3>
            <p className="text-gray-400">Manipulate Arrays, fixed-size Tuple Types, and nested Dictionaries natively with helpful built-in string/array methods.</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="w-full border-t border-white/10 py-12 mt-12">
        <div className="max-w-6xl mx-auto px-6 text-gray-500 text-sm">
          <p>© {new Date().getFullYear()} DOOMS Language. Created by Rohan Shinde.</p>
        </div>
      </footer>
    </main>
  );
}
