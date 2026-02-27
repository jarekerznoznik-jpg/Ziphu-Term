import subprocess
import os

def run_command(command: str, timeout: int = 120) -> str:
    """
    Execute a shell command. Use for running tests, builds, git operations, installing packages, or any CLI tool.
    THIS TOOL ALWAYS REQUIRES USER CONFIRMATION.
    """
    try:
        # We handle confirmation in the agent loop/display layer,
        # but the docstring here is critical for the LLM's understanding.
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        output = f"Exit Code: {result.returncode}
"
        if result.stdout:
            output += f"STDOUT:
{result.stdout}
"
        if result.stderr:
            output += f"STDERR:
{result.stderr}
"
            
        if len(output) > 10000:
            output = output[:10000] + "... (output truncated)"
            
        return output
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"
