import { NextResponse } from 'next/server';
import { execFile } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const execFileAsync = promisify(execFile);

export async function POST(request: Request) {
  try {
    const { code } = await request.json();

    if (typeof code !== 'string') {
      return NextResponse.json({ error: 'Invalid code provided' }, { status: 400 });
    }

    // Create a temporary file
    const tempFileName = `dooms_script_${Date.now()}_${Math.random().toString(36).substring(7)}.dooms`;
    const tempFilePath = path.join(os.tmpdir(), tempFileName);

    // Write code to the file
    fs.writeFileSync(tempFilePath, code, 'utf8');

    try {
      // Execute the dooms code by pointing directly to the python module
      // This assumes the Next.js app is next to the Dooms language directory
      const doomsDir = path.resolve(process.cwd(), '../Dooms');
      const { stdout, stderr } = await execFileAsync('python', ['-m', 'dooms.cli', 'run', tempFilePath], { 
        timeout: 5000,
        cwd: doomsDir,
        shell: process.platform === 'win32' ? 'cmd.exe' : true
      });
      
      // Clean up temp file
      fs.unlinkSync(tempFilePath);

      return NextResponse.json({ output: stdout + (stderr || '') });
    } catch (execError: any) {
      // Clean up temp file on error
      if (fs.existsSync(tempFilePath)) {
        fs.unlinkSync(tempFilePath);
      }

      // If it's a timeout error
      if (execError.killed) {
        return NextResponse.json({ output: 'Execution timed out after 5 seconds.\n' });
      }

      // dooms cli might return non-zero exit code on syntax errors, etc.
      // In that case, we still want to show the error message.
      const errorOutput = execError.stdout || execError.stderr || execError.message;
      return NextResponse.json({ output: errorOutput });
    }

  } catch (error: any) {
    return NextResponse.json({ output: 'Failed to process request: ' + error.message + '\n' }, { status: 500 });
  }
}
