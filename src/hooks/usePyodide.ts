"use client";
import { useState, useEffect, useRef } from 'react';

export function usePyodide() {
  const [isReady, setIsReady] = useState(false);
  const [output, setOutput] = useState<string>('');
  const pyodideRef = useRef<any>(null);

  useEffect(() => {
    // Only load if it hasn't been loaded already
    if (document.querySelector('#pyodide-script')) return;

    const script = document.createElement('script');
    script.id = 'pyodide-script';
    script.src = 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js';
    script.async = true;
    
    script.onload = async () => {
      try {
        const pyodide = await (window as any).loadPyodide({
          stdout: (text: string) => {
            setOutput((prev) => prev + text + '\n');
          },
          stderr: (text: string) => {
            setOutput((prev) => prev + text + '\n');
          }
        });
        await pyodide.loadPackage('micropip');
        const micropip = pyodide.pyimport('micropip');
        await micropip.install('dooms');
        pyodideRef.current = pyodide;
        setIsReady(true);
      } catch (err) {
        console.error('Failed to load Pyodide or install dooms:', err);
        setOutput('Error initializing the environment. Please refresh the page.');
      }
    };
    document.body.appendChild(script);

    return () => {
      // We don't remove the script on unmount so returning to the page keeps it loaded
    };
  }, []);

  const executeCode = async (code: string) => {
    if (!pyodideRef.current) return;
    
    setOutput(''); // clear output before run
    
    // Set the code as a global variable to avoid string interpolation issues in python
    pyodideRef.current.globals.set("dooms_code", code);
    
    const pythonCode = `
from dooms.lexer.lexer import Lexer
from dooms.parser.parser import Parser
from dooms.interpreter.interpreter import Interpreter
from dooms.interpreter.errors import DoomsError
from dooms.cli import format_error
import sys

try:
    lexer = Lexer(dooms_code)
    parser = Parser(lexer)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)
except Exception as e:
    if isinstance(e, DoomsError):
        format_error(dooms_code, e)
    else:
        print(str(e), file=sys.stderr)
`;

    try {
      await pyodideRef.current.runPythonAsync(pythonCode);
    } catch (err: any) {
      setOutput(prev => prev + err.toString() + '\n');
    }
  };

  return { isReady, output, executeCode };
}
