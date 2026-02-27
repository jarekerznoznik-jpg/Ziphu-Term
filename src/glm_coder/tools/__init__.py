from .file_ops import read_file, write_file, edit_file
from .search import list_directory, search_files, glob_files
from .shell import run_command
from .base import get_tool_schema

TOOL_REGISTRY = {
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "list_directory": list_directory,
    "search_files": search_files,
    "glob_files": glob_files,
    "run_command": run_command,
}

def get_tools_schemas():
    return [get_tool_schema(func) for func in TOOL_REGISTRY.values()]
