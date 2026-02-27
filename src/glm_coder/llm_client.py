from openai import OpenAI
from rich.prompt import Prompt
from .config import get_config, save_config
from .display import console

def get_client(api_key=None, base_url=None):
    config = get_config()
    key = api_key or config.get("api_key")
    url = base_url or config.get("base_url")
    
    if not key:
        console.print("[warning]ZHIPUAI_API_KEY is not set.[/warning]")
        console.print("You can find your API key at: [bold blue]https://open.bigmodel.cn/usercenter/apikeys[/bold blue]")
        key = Prompt.ask("Please enter your Zhipu AI API Key", password=True)
        if key:
            save_config({"api_key": key})
            console.print("[info]API Key saved to config.[/info]")
        else:
            raise ValueError("API Key is required to run GLM Coder.")
    
    return OpenAI(
        api_key=key,
        base_url=url
    )
