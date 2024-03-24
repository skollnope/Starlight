import re
from typing import Any

hello_world_def: dict[str, Any] = {"name": "hello_World",
                                  "description": "Answers to the \"Hello World ?\" answers"}
def hello_world():
    print("hello world !")

def invoke(name:str, args:any=None):
    function = locals()[name]
    if(function is not None):        
        function(args)

def getFunctions() -> list[dict[str, Any]]:
    return [
            hello_world_def,
        ]