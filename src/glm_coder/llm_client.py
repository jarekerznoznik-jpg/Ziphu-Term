from openai import OpenAI
from .config import get_config

def get_client(api_key=None, base_url=None):
    config = get_config()
    key = api_key or config.get("api_key")
    url = base_url or config.get("base_url")
    
    if not key:
        raise ValueError("ZHIPUAI_API_KEY is not set. Please set it in your environment or config file.")
    
    return OpenAI(
        api_key=key,
        base_url=url
    )
