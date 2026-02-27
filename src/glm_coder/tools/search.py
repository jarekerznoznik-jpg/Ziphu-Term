import os
import re
from pathlib import Path

def list_directory(path: str = ".") -> str:
    """
    List directory contents sorted: directories first (with / suffix), then files.
    """
    try:
        p = Path(path)
        if not p.is_dir():
            return f"Error: {path} is not a directory."
        
        items = []
        # Common skip list
        skip = {'__pycache__', 'node_modules', '.git', '.venv', 'venv'}
        
        for item in sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            if item.name.startswith('.') and not path.startswith('.'):
                continue
            if item.name in skip:
                continue
            
            suffix = "/" if item.is_dir() else ""
            items.append(f"{item.name}{suffix}")
            
            if len(items) >= 200:
                items.append("... (truncated)")
                break
                
        return "
".join(items) if items else "(empty directory)"
    except Exception as e:
        return f"Error listing directory {path}: {str(e)}"

def search_files(pattern: str, path: str = ".", file_pattern: str = None) -> str:
    """
    Regex search across files recursively. Use this for content search.
    """
    try:
        p = Path(path)
        regex = re.compile(pattern)
        matches = []
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}
        
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in skip_dirs]
            
            for file in files:
                if file_pattern and not Path(file).match(file_pattern):
                    continue
                    
                file_path = Path(root) / file
                try:
                    # Check if binary
                    with open(file_path, 'rb') as f:
                        if b'\x00' in f.read(1024):
                            continue
                            
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        for i, line in enumerate(f, start=1):
                            if regex.search(line):
                                matches.append(f"{file_path}:{i}: {line.strip()}")
                                if len(matches) >= 100:
                                    matches.append("... (truncated)")
                                    return "
".join(matches)
                except Exception:
                    continue
                    
        return "
".join(matches) if matches else "No matches found."
    except Exception as e:
        return f"Error searching files: {str(e)}"

def glob_files(pattern: str) -> str:
    """
    Find files matching glob patterns. Use this for finding files by name pattern.
    """
    try:
        # Use recursive glob if ** is in pattern
        p = Path('.')
        matches = list(p.glob(pattern))
        
        results = []
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}
        
        for m in matches:
            # Check if any part of the path is in skip_dirs
            if any(part in skip_dirs or part.startswith('.') for part in m.parts[:-1]):
                continue
            results.append(str(m))
            if len(results) >= 200:
                results.append("... (truncated)")
                break
                
        return "
".join(results) if results else "No matches found."
    except Exception as e:
        return f"Error globbing files: {str(e)}"
