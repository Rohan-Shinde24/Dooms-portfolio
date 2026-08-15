import sys
import os
from dooms.lexer.lexer import Lexer
from dooms.parser.parser import Parser
from dooms.interpreter.interpreter import Interpreter

def run_file(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
        
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    try:
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(program)
    except Exception as e:
        from dooms.interpreter.errors import DoomsError
        if isinstance(e, DoomsError):
            format_error(source, e)
        else:
            print(str(e), file=sys.stderr)
        sys.exit(1)

def format_error(source, error):
    error_type = error.__class__.__name__
    message = error.message
    
    print(f"\n\033[91m{error_type}\033[0m: {message}", file=sys.stderr)
    
    if error.line is not None and error.column is not None:
        print(f"  \033[94m-->\033[0m line {error.line}, column {error.column}", file=sys.stderr)
        
        lines = source.splitlines()
        if 0 < error.line <= len(lines):
            line_content = lines[error.line - 1]
            print(f"\n    | {line_content}", file=sys.stderr)
            caret_padding = " " * (error.column - 1)
            print(f"    | {caret_padding}\033[91m^\033[0m", file=sys.stderr)
            
    if error.hint:
        print(f"\n\033[93mHint:\033[0m {error.hint}", file=sys.stderr)
    
    print("", file=sys.stderr)

def main():
    if len(sys.argv) < 3 or sys.argv[1] != 'run':
        print("Usage: python -m src.cli.cli run <filename.dooms>")
        sys.exit(1)
        
    filepath = sys.argv[2]
    run_file(filepath)

if __name__ == "__main__":
    main()
