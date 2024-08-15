
from typing import Any

def create_user_message(message:str):
    return {"role": "user", "content": message}

def create_assistant_message(message:str):
    return {"role": "assistant", "content": message}

def create_assistant_toolcalls(tool_calls:list[dict[str, Any]]=None):
    return {"role": "assistant", "tool_calls": tool_calls}

def create_toolcalling_message(message:str, id:str):
    return {"role": "tool", "content": message, "tool_call_id": id}
    
def create_message_with_prompt(prompt:str, message:str):
    return [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ]