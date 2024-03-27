from typing import Any
from Starlight.LM_Studio.Functions import hello_world as hw

def invoke(name:str, args:Any=None):
    function = FUNCTIONS.get(name)
    if(function is not None):     
            return function(args)
    else:
        print("No function named: \"" + name + "\" found")
        
def serialize_function(func_def: dict[str, Any]) -> dict[str, Any]:
     return {"type": "function",
             "function": func_def}

def getFunctions() -> list[dict[str, Any]]:
    return [
            serialize_function(hw.hello_world_def),
            serialize_function(hw.string_answer_def),
        ]

FUNCTIONS: dict[str, Any] = {
    hw.hello_world_def["name"]: hw.hello_world,
    hw.string_answer_def["name"]: hw.string_answer,
    }