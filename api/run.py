from http.server import BaseHTTPRequestHandler
import json
import sys
import tempfile
import os
import subprocess

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            code = data.get('code', '')
            
            with tempfile.NamedTemporaryFile(suffix=".dooms", delete=False, mode='w', encoding='utf-8') as f:
                f.write(code)
                temp_path = f.name
                
            try:
                # Add the project root to PYTHONPATH so python can find the local 'dooms' folder
                env = os.environ.copy()
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")
                
                result = subprocess.run(
                    [sys.executable, "-m", "dooms.cli", "run", temp_path],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    env=env
                )
                output = result.stdout + result.stderr
            except subprocess.TimeoutExpired:
                output = "Execution timed out after 5 seconds.\n"
            except Exception as e:
                output = str(e)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        except Exception as e:
            output = f"Internal Server Error: {str(e)}"
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'output': output}).encode('utf-8'))
