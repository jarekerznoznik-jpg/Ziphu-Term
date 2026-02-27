import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CONFIG_DIR = Path.home() / ".glm-coder"
CONFIG_FILE = CONFIG_DIR / "config.json"
SESSIONS_DIR = CONFIG_DIR / "sessions"

# Ensure config directory exists
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
ZHIPUAI_BASE_URL = os.getenv("ZHIPUAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
ZHIPUAI_MODEL = os.getenv("ZHIPUAI_MODEL", "glm-4.7-flash")

MODEL_CONTEXT_WINDOWS = {
    "glm-5": 200000,
    "glm-5-code": 200000,
    "glm-4.7": 200000,
    "glm-4.7-flash": 128000,
    "glm-4.6": 128000,
    "glm-4.5-flash": 128000,
}

def get_config():
    config = {
        "api_key": ZHIPUAI_API_KEY,
        "base_url": ZHIPUAI_BASE_URL,
        "model": ZHIPUAI_MODEL,
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception:
            pass
    return config

def save_config(new_config):
    config = get_config()
    config.update(new_config)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
