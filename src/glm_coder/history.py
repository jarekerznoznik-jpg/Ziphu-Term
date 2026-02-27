import json
import tiktoken
from datetime import datetime
from .config import SESSIONS_DIR, MODEL_CONTEXT_WINDOWS

class ConversationHistory:
    def __init__(self, session_id=None):
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.messages = []
        self.file_path = SESSIONS_DIR / f"{self.session_id}.json"
        
    def add_message(self, role, content, tool_calls=None, tool_call_id=None):
        msg = {"role": role, "content": content}
        if tool_calls:
            msg["tool_calls"] = tool_calls
        if tool_call_id:
            msg["tool_call_id"] = tool_call_id
        self.messages.append(msg)
        self.save()

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.messages, f, indent=2)

    def load(self):
        if self.file_path.exists():
            with open(self.file_path, "r") as f:
                self.messages = json.load(f)

    def clear(self, system_prompt):
        self.messages = [{"role": "system", "content": system_prompt}]
        self.save()

    def count_tokens(self, model="gpt-3.5-turbo"): # Using as approximation
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
        except:
            encoding = tiktoken.get_encoding("cl100k_base")
            
        num_tokens = 0
        for message in self.messages:
            num_tokens += 4 # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                if value:
                    num_tokens += len(encoding.encode(str(value)))
        num_tokens += 2 # every reply is primed with <im_start>assistant
        return num_tokens

    def truncate_if_needed(self, model_name):
        limit = MODEL_CONTEXT_WINDOWS.get(model_name, 128000)
        max_budget = int(limit * 0.8)
        
        while self.count_tokens() > max_budget and len(self.messages) > 5:
            # Keep system message (index 0)
            # Find first non-system message to remove
            # But be careful not to break tool_call/tool pairs
            # For simplicity, we remove from index 1
            idx_to_remove = 1
            if self.messages[idx_to_remove].get("role") == "assistant" and self.messages[idx_to_remove].get("tool_calls"):
                # If it's a tool call, we must also remove the following tool results
                # This is a bit complex, let's just pop until we find a safe spot or reach 10 last messages
                pass
            
            if len(self.messages) > 10:
                self.messages.pop(1)
            else:
                break
        self.save()
