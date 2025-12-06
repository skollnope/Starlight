from typing import Any

hello_world_def: dict[str, Any] = {"name": "hello_world",
                                  "description": "Answers to the \"Hello World ?\" answers"}
def hello_world(args=None):
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