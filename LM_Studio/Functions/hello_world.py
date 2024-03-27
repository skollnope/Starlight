from typing import Any

hello_world_def: dict[str, Any] = {"name": "hello_world",
                                  "description": "Answers to the \"Hello World ?\" question"}
def hello_world(args=None):
    message = "hello world !2"
    print(message)
    return message

string_answer_def: dict[str, Any] = {"name": "string_answer",
                                    "description": "this function is only made to you, to answer to the user",
                                    "parameters":{  "type": "object",
                                                    "properties": {"text": {"type": "string",
                                                                            "description": "the text you want to say"
                                                                            }},
                                                    "required": ["text"]}}
def string_answer(args):
    message = args["text"]
    print(message)