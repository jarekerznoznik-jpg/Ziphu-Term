from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Confirm
from rich.theme import Theme

custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "tool": "bold blue",
})

console = Console(theme=custom_theme)

def display_welcome():
    console.print(Panel.fit(
        """[bold blue]GLM Coder[/bold blue] - Agentic AI Coding Assistant
Powered by Zhipu AI GLM Models""",
        title="Welcome",
        border_style="blue"
    ))
    console.print("Type your request or use [bold]/help[/bold] for commands.")

def display_tool_call(name, args):
    console.print(Panel(
        Syntax(str(args), "json", theme="monokai", background_color="default"),
        title=f"Tool Call: [bold blue]{name}[/bold blue]",
        border_style="blue"
    ))

def confirm_action(name):
    return Confirm.ask(f"Allow [bold blue]{name}[/bold blue] to proceed?")

def display_tool_result(result):
    # Truncate for display
    display_text = result[:500] + "..." if len(result) > 500 else result
    console.print(f"[dim]Result: {display_text}[/dim]")

def display_error(msg):
    console.print(Panel(msg, title="Error", border_style="red"))
