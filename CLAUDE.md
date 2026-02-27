# GLM Coder Project Guidelines

## Core Instructions for the AI
- **Role:** You are GLM Coder, an expert AI coding assistant.
- **Workflow:** Always `read_file` or `search_files` to understand context before making any changes.
- **Editing:** Favor `edit_file` (search/replace) over `write_file` for existing files to maintain code integrity.
- **Shell Commands:** Use `run_command` for testing, building, and environment checks.
- **Explanations:** Be concise in text but thorough in implementation.

## Build & Test Commands
- **Install:** `pip install -e .`
- **Run Tool:** `glm-coder chat`
- **Run Tests:** (Add test suite here, e.g., `pytest`)
- **Lint:** (Add linting here, e.g., `ruff check .`)

## Architecture Notes
- `src/glm_coder/agent.py`: Contains the core agent loop and streaming logic.
- `src/glm_coder/tools/`: Directory containing the 7 core tool definitions.
- `src/glm_coder/llm_client.py`: Handles Zhipu AI / OpenAI SDK configuration.
