import json
import traceback
from datetime import datetime
from .config import ERROR_LOG_FILE

def log_error(error_type, message, context=None):
    """Logs an error with context and traceback to a jsonl file."""
    error_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": error_type,
        "message": str(message),
        "traceback": traceback.format_exc(),
        "context": context or {}
    }
    
    try:
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(error_entry) + "\n")
        return True
    except Exception:
        return False
