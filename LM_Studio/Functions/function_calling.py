from typing import Any

hello_world_def: dict[str, Any] = {"name": "hello_world",
                                  "description": "Answers to the \"Hello World ?\" answers"}
def hello_world():
    message = "hello world !"
    print(message)
    return message

hello_you_def: dict[str, Any] = {"name": "hello_you",
                                 "description": "greet someone",
                                 "parameters": {"type": "string",
                                                "description": "the name of the person"}}
def hello_you(args):
    message = "Hello " + args["name"] + " !"
    print(message)
    return message

#--------- General Definitions ----------

def invoke(name:str, args:any=None):
    function = FUNCTIONS.get(name)
    if(function is not None):  
        if(args is not None):      
            return function(args)
        else:
            return function()
    else:
        print("No function named: \"" + name + "\" found")

def getFunctions() -> list[dict[str, Any]]:
    return [
            hello_world_def,
            hello_you_def,
        ]

FUNCTIONS: dict[str, Any] = {
    hello_world_def["name"]: hello_world,
    hello_you_def["name"]: hello_you,
    }