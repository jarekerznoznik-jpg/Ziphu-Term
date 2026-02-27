# GLM Coder

An agentic CLI tool powered by Zhipu AI's GLM models. Similar to Claude Code or Aider, it can read your codebase, edit files, and run commands to help you build software.

## Features

- **Agentic Workflow**: The AI uses tools to explore and modify your project.
- **Zhipu AI Integration**: Optimized for GLM-5, GLM-4.7, and GLM-4.7-flash.
- **Interactive REPL**: Rich terminal interface with syntax highlighting and streaming Markdown.
- **Smart Tools**: Read, write, edit files, search, glob, and run shell commands.
- **Safety First**: Asks for confirmation before writing files or running shell commands.

## Installation

```bash
cd glm-coder
pip install -e .
```

## Configuration

Set your Zhipu AI API key as an environment variable:

```bash
export ZHIPUAI_API_KEY="your-api-key-here"
```

Optional environment variables:
- `ZHIPUAI_BASE_URL`: Override the default API endpoint.
- `ZHIPUAI_MODEL`: Set the default model (default is `glm-4.7-flash`).

## Usage

### Interactive Chat

Start an interactive session in your terminal:

```bash
glm-coder chat
```

### One-shot Command

Run a single prompt and exit:

```bash
glm-coder run "Fix the bug in main.py"
```

## Available Tools

1. `read_file`: Read content and line numbers of a file.
2. `write_file`: Create or overwrite a file.
3. `edit_file`: Search and replace text in a file.
4. `list_directory`: List files in a directory.
5. `search_files`: Regex search through the codebase.
6. `glob_files`: Find files by name pattern.
7. `run_command`: Execute shell commands (requires confirmation).

## Slash Commands

In the REPL, you can use:
- `/help`: Show help.
- `/clear`: Clear conversation history.
- `/model <name>`: Switch the model.
- `/exit`: Exit the tool.
