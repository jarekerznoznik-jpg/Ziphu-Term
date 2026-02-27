import inspect
from typing import get_type_hints, Any

def get_tool_schema(func):
    """Generates an OpenAI-compatible JSON schema for a function."""
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    
    properties = {}
    required = []
    
    for name, param in signature.parameters.items():
        if name == "return":
            continue
            
        param_type = type_hints.get(name, Any)
        
        # Simple type mapping
        json_type = "string"
        if param_type == int:
            json_type = "integer"
        elif param_type == bool:
            json_type = "boolean"
        elif param_type == float:
            json_type = "number"
        elif param_type == list:
            json_type = "array"
        elif param_type == dict:
            json_type = "object"
            
        properties[name] = {
            "type": json_type,
            "description": f"Parameter {name}" # Basic description if docstring parsing isn't implemented
        }
        
        if param.default is inspect.Parameter.empty:
            required.append(name)

    # Try to extract descriptions from docstring
    doc = inspect.getdoc(func) or ""
    
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": doc.split("\\n\\n")[0] if doc else "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }
