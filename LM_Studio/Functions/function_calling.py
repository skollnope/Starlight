from typing import Any
from Starlight.LM_Studio.Functions import hello_world as hw

def invoke(name:str, args:Any=None):
    function = FUNCTIONS.get(name)
    if(function is not None):     
            return function(args)
    else:
        print("No function named: \"" + name + "\" found")

def getFunctions() -> list[dict[str, Any]]:
    return [
            hw.hello_world_def,
            hw.hello_you_def,
        ]

FUNCTIONS: dict[str, Any] = {
    hw.hello_world_def["name"]: hw.hello_world,
    hw.hello_you_def["name"]: hw.hello_you,
    }