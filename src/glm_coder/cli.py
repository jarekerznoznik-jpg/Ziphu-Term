import typer
from typing import Optional
from .llm_client import get_client
from .history import ConversationHistory
from .repl import start_repl
from .agent import agent_loop, SYSTEM_PROMPT
from .config import ZHIPUAI_MODEL, ZHIPUAI_BASE_URL, get_config

app = typer.Typer(help="GLM Coder - AI coding assistant powered by Zhipu AI")

@app.command()
def chat(
    model: str = typer.Option(ZHIPUAI_MODEL, help="Model to use"),
    base_url: str = typer.Option(ZHIPUAI_BASE_URL, help="API base URL override"),
    resume: bool = typer.Option(False, help="Resume last session"),
):
    """Start interactive coding session."""
    try:
        client = get_client(base_url=base_url)
        history = ConversationHistory()
        if resume:
            # Simple logic to find latest session
            history.load() # This would need more robust logic to find the LATEST
            
        start_repl(history, client, model)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

@app.command()
def run(
    prompt: str = typer.Argument(..., help="One-shot prompt to execute"),
    model: str = typer.Option(ZHIPUAI_MODEL, help="Model to use"),
):
    """Execute a single prompt and exit."""
    try:
        client = get_client()
        history = ConversationHistory()
        history.add_message("system", SYSTEM_PROMPT)
        agent_loop(prompt, history, client, model)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
