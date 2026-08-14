import React from 'react';
import Link from 'next/link';

export default function Docs() {
  return (
    <div className="min-h-screen text-[#ededed] flex flex-col md:flex-row relative">
      {/* Sidebar Navigation */}
      <aside className="md:w-72 md:fixed md:left-0 md:top-0 md:h-screen overflow-y-auto border-r border-white/10 glass-panel rounded-none! border-y-0! border-l-0! z-10">
        <div className="p-8">
          <Link href="/" className="flex items-center gap-2 text-2xl font-bold tracking-tighter text-white mb-8">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
            Doomslang
          </Link>
          <nav className="flex flex-col gap-4 text-sm font-medium text-gray-400">
            <h4 className="text-xs uppercase text-gray-600 font-bold tracking-wider mt-4 mb-2">Getting Started</h4>
            <a href="#install" className="hover:text-white transition-colors">Installation</a>
            
            <h4 className="text-xs uppercase text-gray-600 font-bold tracking-wider mt-4 mb-2">Language Guide</h4>
            <a href="#variables" className="hover:text-white transition-colors">Variables & Types</a>
            <a href="#functions" className="hover:text-white transition-colors">Functions</a>
            <a href="#arrays" className="hover:text-white transition-colors">Arrays & Tuples</a>
            <a href="#dictionaries" className="hover:text-white transition-colors">Dictionaries</a>
            <a href="#classes" className="hover:text-white transition-colors">Classes (OOP)</a>
            <a href="#modules" className="hover:text-white transition-colors">Modules System</a>
          </nav>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 md:ml-72 py-12 px-6 lg:px-16">
        <div className="max-w-4xl">
          <h1 className="text-5xl font-bold mb-4">Documentation</h1>
          <p className="text-xl text-gray-400 mb-16">Learn how to build software with Doomslang, a strictly-typed scripting language.</p>

          <div className="space-y-24">
            
            {/* Install Section */}
            <section id="install" className="scroll-mt-24">
              <h2 className="text-3xl font-semibold mb-6 border-b border-white/10 pb-4">Installation</h2>
              <p className="text-gray-400 mb-4">Doomslang runs on Python. You must have Python 3.11+ installed. Once Python is ready, you can install Doomslang globally via pip.</p>
              <div className="code-window mb-6">
                <div className="code-content whitespace-pre text-gray-300">
                  <span className="comment"># Install via pip</span><br/>
                  pip install dooms<br/>
                  <br/>
                  <span className="comment"># Run a Doomslang script</span><br/>
                  dooms run my_script.dooms
                </div>
              </div>
            </section>

            {/* Variables Section */}
            <section id="variables" className="scroll-mt-24">
              <h2 className="text-3xl font-semibold mb-6 border-b border-white/10 pb-4">Variables and Data Types</h2>
              <p className="text-gray-400 mb-4">Doomslang is strictly typed. You must declare the type of every variable. Supported types are <code className="text-accent bg-accent/10 px-1 rounded">int</code>, <code className="text-accent bg-accent/10 px-1 rounded">str</code>, <code className="text-accent bg-accent/10 px-1 rounded">boo</code>, and <code className="text-accent bg-accent/10 px-1 rounded">any</code>.</p>
              <div className="code-window">
                <div className="code-content whitespace-pre">
                  <span className="type">int</span> age = <span className="type">25</span>; <span className="comment">// Integers</span><br/>
                  <span className="type">str</span> name = <span className="string">"Doomslang"</span>; <span className="comment">// Strings</span><br/>
                  <span className="type">boo</span> isAwesome = <span className="type">true</span>; <span className="comment">// Booleans</span><br/>
                  <span className="type">any</span> generic = <span className="type">100</span>; <span className="comment">// Dynamic fallback</span>
                </div>
              </div>
            </section>

            {/* Functions Section */}
            <section id="functions" className="scroll-mt-24">
              <h2 className="text-3xl font-semibold mb-6 border-b border-white/10 pb-4">Functions</h2>
              <p className="text-gray-400 mb-4">Define functions using the <code className="text-accent bg-accent/10 px-1 rounded">func</code> keyword. Parameters must be explicitly typed.</p>
              <div className="code-window">
                <div className="code-content whitespace-pre">
                  <span className="keyword">func</span> <span className="function">add</span>(<span className="type">int</span> a, <span className="type">int</span> b) {'{\n'}
                  {'    '}<span className="keyword">return</span> a + b;<br/>
                  {'}'}<br/>
                  <br/>
                  <span className="type">int</span> result = <span className="function">add</span>(<span className="type">10</span>, <span className="type">20</span>);
                </div>
              </div>
            </section>

            {/* Arrays Section */}
            <section id="arrays" className="scroll-mt-24">
              <h2 className="text-3xl font-semibold mb-6 border-b border-white/10 pb-4">Arrays and Tuples</h2>
              <p className="text-gray-400 mb-4">Doomslang supports dynamic arrays (with built-in methods) and strictly typed fixed-size Tuples.</p>
              <div className="code-window">
                <div className="code-content whitespace-pre">
                  <span className="comment">// Dynamic Arrays (using 'any' wrapper array type)</span><br/>
                  <span className="type">any</span> arr = [<span className="type">1</span>, <span className="type">2</span>, <span className="type">3</span>];<br/>
                  arr.<span className="function">push</span>(<span className="type">4</span>);<br/>
                  arr.<span className="function">pop</span>();<br/>
                  <br/>
                  <span className="comment">// Strictly Typed Tuples</span><br/>
                  [<span className="type">int</span>, <span className="type">str</span>] my_tuple = [<span className="type">404</span>, <span className="string">"Not Found"</span>];
                </div>
              </div>
            </section>

            {/* Dictionaries Section */}
            <section id="dictionaries" className="scroll-mt-24">
              <h2 className="text-3xl font-semibold mb-6 border-b border-white/10 pb-4">Dictionaries</h2>
              <p className="text-gray-400 mb-4">Store key-value pairs using string keys. Dictionaries come with <code className="text-accent bg-accent/10 px-1 rounded">.keys()</code> and <code className="text-accent bg-accent/10 px-1 rounded">.get()</code> methods.</p>
              <div className="code-window">
                <div className="code-content whitespace-pre">
                  <span className="type">any</span> user = {'{\n'}
                  {'    '}<span className="string">"name"</span>: <span className="string">"Alice"</span>,<br/>
                  {'    '}<span className="string">"age"</span>: <span className="type">30</span><br/>
                  {'}'};<br/>
                  <br/>
                  <span className="function">print</span>(user[<span className="string">"name"</span>]);<br/>
                  <span className="function">print</span>(user.<span className="function">keys</span>());
                </div>
              </div>
            </section>

            {/* Classes Section */}
            <section id="classes" className="scroll-mt-24">
              <h2 className="text-3xl font-semibold mb-6 border-b border-white/10 pb-4">Object-Oriented Programming</h2>
              <p className="text-gray-400 mb-4">Doomslang natively supports Classes. The <code className="text-accent bg-accent/10 px-1 rounded">init</code> method acts as the constructor. State is managed via <code className="text-accent bg-accent/10 px-1 rounded">this</code>.</p>
              <div className="code-window">
                <div className="code-content whitespace-pre">
                  <span className="keyword">class</span> <span className="type">Robot</span> {'{\n'}
                  {'    '}<span className="keyword">func</span> <span className="function">init</span>(<span className="type">str</span> name) {'{\n'}
                  {'        '}<span className="keyword">this</span>.name = name;<br/>
                  {'    }'}<br/>
                  <br/>
                  {'    '}<span className="keyword">func</span> <span className="function">activate</span>() {'{\n'}
                  {'        '}<span className="function">print</span>(<span className="keyword">this</span>.name, <span className="string">"is now active!"</span>);<br/>
                  {'    }'}<br/>
                  {'}'}<br/>
                  <br/>
                  <span className="comment">// Instantiate simply by calling the class name</span><br/>
                  <span className="type">any</span> bot = <span className="function">Robot</span>(<span className="string">"T-800"</span>);<br/>
                  bot.<span className="function">activate</span>();
                </div>
              </div>
            </section>

            {/* Modules Section */}
            <section id="modules" className="scroll-mt-24">
              <h2 className="text-3xl font-semibold mb-6 border-b border-white/10 pb-4">Modules System</h2>
              <p className="text-gray-400 mb-4">Import variables and functions from other Doomslang files to keep your codebase organized.</p>
              <div className="code-window">
                <div className="code-content whitespace-pre">
                  <span className="comment">// main.dooms</span><br/>
                  <span className="keyword">import</span> <span className="string">"math.dooms"</span> <span className="keyword">as</span> math;<br/>
                  <span className="function">print</span>(math.<span className="function">add</span>(<span className="type">5</span>, <span className="type">5</span>));
                </div>
              </div>
            </section>
            
          </div>
        </div>
      </main>
    </div>
  );
}
