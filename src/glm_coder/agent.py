import json
from rich.live import Live
from rich.markdown import Markdown
from .tools import TOOL_REGISTRY, get_tools_schemas
from .display import console, display_tool_call, confirm_action, display_tool_result, display_error
from .logger import log_error
from .config import ERROR_LOG_FILE

MAX_ITERATIONS = 25

SYSTEM_PROMPT = """
You are GLM Coder, an expert AI coding assistant running in the user's terminal. You have access to tools for reading files, writing files, editing code, searching codebases, and running shell commands.

Key principles:
- Always read relevant files before making changes to understand the existing code
- Use edit_file for targeted changes to existing files (preferred over write_file for modifications)
- Use write_file only for creating new files or complete rewrites
- After making changes, offer to run relevant tests or build commands
- Explain what you're doing and why
- If a tool call fails, read the error and try a different approach
- Be concise in explanations but thorough in code changes
"""

def agent_loop(user_input, history, client, model):
    if user_input:
        history.add_message("user", user_input)
    
    for iteration in range(MAX_ITERATIONS):
        history.truncate_if_needed(model)
        
        tools = get_tools_schemas()
        
        accumulated_text = ""
        tool_calls_buffer = {}
        finish_reason = None
        
        with Live(Markdown(""), console=console, refresh_per_second=8) as live:
            try:
                stream = client.chat.completions.create(
                    model=model,
                    messages=history.messages,
                    tools=tools,
                    tool_choice="auto",
                    stream=True,
                    # extra_body={"tool_stream": True} # Some models might need this
                )
                
                for chunk in stream:
                    delta = chunk.choices[0].delta
                    finish_reason = chunk.choices[0].finish_reason
                    
                    if delta.content:
                        accumulated_text += delta.content
                        live.update(Markdown(accumulated_text))
                    
                    if delta.tool_calls:
                        for tc in delta.tool_calls:
                            idx = tc.index
                            if idx not in tool_calls_buffer:
                                tool_calls_buffer[idx] = {
                                    "id": tc.id,
                                    "name": tc.function.name,
                                    "arguments": ""
                                }
                            if tc.function.arguments:
                                tool_calls_buffer[idx]["arguments"] += tc.function.arguments
            except Exception as e:
                live.stop()
                log_error("LLM_STREAM_ERROR", str(e), {"model": model})
                display_error(f"LLM Error: {str(e)}\\nDetails logged to {ERROR_LOG_FILE}")
                return

        # Reconstruction of assistant message
        tool_calls = []
        if tool_calls_buffer:
            for idx in sorted(tool_calls_buffer.keys()):
                tc = tool_calls_buffer[idx]
                tool_calls.append({
                    "id": tc["id"],
                    "type": "function",
                    "function": {
                        "name": tc["name"],
                        "arguments": tc["arguments"]
                    }
                })
        
        history.add_message("assistant", accumulated_text or None, tool_calls=tool_calls if tool_calls else None)

        if not tool_calls:
            break

        # Process tool calls
        for tc in tool_calls:
            name = tc["function"]["name"]
            try:
                args = json.loads(tc["function"]["arguments"])
            except:
                args = {"error": "Invalid JSON arguments"}
            
            display_tool_call(name, args)
            
            # Permission check
            if name in ["run_command", "write_file", "edit_file"]:
                if not confirm_action(name):
                    result = "User denied this operation."
                    history.add_message("tool", result, tool_call_id=tc["id"])
                    continue
            
            # Execute
            tool_func = TOOL_REGISTRY.get(name)
            if tool_func:
                try:
                    result = tool_func(**args)
                except Exception as e:
                    log_error("TOOL_EXECUTION_ERROR", str(e), {"tool": name, "args": args})
                    result = f"Error executing {name}: {str(e)}\\nDetails logged to {ERROR_LOG_FILE}"
            else:
                result = f"Error: Tool {name} not found."
            
            display_tool_result(str(result))
            history.add_message("tool", str(result), tool_call_id=tc["id"])

    else:
        console.print("[warning]Reached maximum iterations.[/warning]")
