import os
import shutil
from pathlib import Path

def read_file(path: str, start_line: int = None, end_line: int = None) -> str:
    """
    Read file contents. Use this to understand existing code before making changes.
    """
    try:
        file_path = Path(path)
        if not file_path.exists():
            return f"Error: File {path} does not exist."
        
        if file_path.stat().st_size > 1024 * 1024:
            return f"Error: File {path} is too large (> 1MB)."
        
        with open(file_path, 'rb') as f:
            chunk = f.read(8192)
            if b'\\x00' in chunk:
                return f"Error: File {path} appears to be binary."
        
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        start = (start_line - 1) if start_line else 0
        end = end_line if end_line else len(lines)
        
        subset = lines[start:end]
        output = []
        for i, line in enumerate(subset, start=start + 1):
            output.append(f"{i:4} | {line}")
        
        return "".join(output)
    except Exception as e:
        return f"Error reading file {path}: {str(e)}"

def write_file(path: str, content: str) -> str:
    """
    Write complete content to a file. Use for new files or complete rewrites. 
    For small changes to existing files, prefer edit_file.
    """
    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        temp_path = file_path.with_suffix('.tmp')
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        os.replace(temp_path, file_path)
        line_count = len(content.splitlines())
        return f"Successfully wrote {line_count} lines to {path}."
    except Exception as e:
        return f"Error writing file {path}: {str(e)}"

def edit_file(path: str, old_text: str, new_text: str) -> str:
    """
    Make a targeted edit by specifying exact text to find and replace. 
    The old_text must match exactly. Prefer this over write_file for modifying existing files.
    """
    try:
        file_path = Path(path)
        if not file_path.exists():
            return f"Error: File {path} does not exist."
            
        content = file_path.read_text(encoding='utf-8')
        
        if old_text in content:
            new_content = content.replace(old_text, new_text, 1)
        else:
            # Fuzzy match fallback
            lines = content.splitlines()
            old_lines = old_text.splitlines()
            
            # Simple fuzzy: strip trailing whitespace
            content_stripped = "\\n".join([l.rstrip() for l in lines])
            old_text_stripped = "\\n".join([l.rstrip() for l in old_lines])
            
            if old_text_stripped in content_stripped:
                return f"Error: Could not find exact match for old_text in {path}. Please ensure whitespace and indentation match exactly, or re-read the file."
            else:
                first_3_lines = "\\n".join(old_lines[:3])
                return f"Error: Could not find the text to replace in {path}.\\nFirst 3 lines of search text:\\n{first_3_lines}\\nPlease re-read the file to get the exact content."

        temp_path = file_path.with_suffix('.tmp')
        temp_path.write_text(new_content, encoding='utf-8')
        os.replace(temp_path, file_path)
        
        return f"Successfully edited {path}."
    except Exception as e:
        return f"Error editing file {path}: {str(e)}"
