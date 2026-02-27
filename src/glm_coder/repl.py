import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from .config import CONFIG_DIR
from .display import console, display_welcome
from .agent import agent_loop, SYSTEM_PROMPT

def start_repl(history, client, model):
    session = PromptSession(
        history=FileHistory(str(CONFIG_DIR / "history")),
        auto_suggest=AutoSuggestFromHistory(),
    )
    
    display_welcome()
    
    if not history.messages:
        history.add_message("system", SYSTEM_PROMPT)

    while True:
        try:
            user_input = session.prompt(">>> ")
            
            if not user_input.strip():
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                break
                
            if user_input.startswith("/"):
                cmd = user_input.split()[0]
                if cmd in ["/exit", "/quit"]:
                    break
                elif cmd == "/help":
                    console.print("[info]Available commands:[/info]")
                    console.print("  /help    - Show this help")
                    console.print("  /clear   - Clear conversation history")
                    console.print("  /history - Show history summary")
                    console.print("  /model   - Change model")
                    console.print("  /exit    - Exit")
                    continue
                elif cmd == "/clear":
                    history.clear(SYSTEM_PROMPT)
                    console.print("[info]History cleared.[/info]")
                    continue
                elif cmd == "/history":
                    for msg in history.messages:
                        role = msg["role"]
                        content = msg.get("content", "")
                        if content:
                            console.print(f"[bold]{role}:[/bold] {content[:100]}...")
                    continue
                elif cmd == "/model":
                    parts = user_input.split()
                    if len(parts) > 1:
                        model = parts[1]
                        console.print(f"[info]Switched to model: {model}[/info]")
                    else:
                        console.print(f"[info]Current model: {model}[/info]")
                    continue
                elif cmd == "/key":
                    from rich.prompt import Prompt
                    from .config import save_config
                    new_key = Prompt.ask("Enter new Zhipu AI API Key", password=False)
                    if new_key:
                        save_config({"api_key": new_key})
                        client.api_key = new_key
                        console.print("[info]API Key updated.[/info]")
                    continue
            
            agent_loop(user_input, history, client, model)
            
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
            
    console.print("Goodbye!")
