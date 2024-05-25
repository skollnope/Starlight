from typing import Any
from abc import ABC, abstractmethod
from Starlight.LM_Studio import constants as cst
from Starlight.LM_Studio.Functions import function_calling as func
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller, FunctionItem
from Starlight.LM_Studio.context import Context

class APIWrapper(ABC):
    _function_list: list[FunctionCaller]
    _history:list[dict[str, str]] = []
    debug:bool = False
    _contexts:Context = Context()

    def __init__(self):
        # Any common initialization code can go here
        pass

    def __del__(self):
        if self.debug:
            self.print_history()
    
    def print_history(self):
        for h in self._history:
            print(h["role"] + ": " + h["content"])
    
    def create_user_message(self, message:str):
        return {"role": "user", "content": message}
    
    def create_assistant_message(self, message:str):
        return {"role": "assistant", "content": message}
    
    def create_toolcalling_message(self, message:str):
        return {"role": "tool_calling", "content": message}

    def serialize_contexts(self, prompt:str):
        return prompt + self._contexts.serialize()
    
    @abstractmethod
    def ask_for_context(self, sentence:str) -> str:
        """
        summary:
            ask to an API model to return the global context of the sentence

        args:
        sentence: the sentence wanted to be asked

        returns:
            the keyword context
        """
        pass

    def get_methods_by_context(self, context: str) -> FunctionCaller:
        for func in self._function_list:
            if(func.context == context):
                return func
        return None

    @abstractmethod
    def parse_reply(answer:Any):
        pass

    def log(self, log_message:str):
        if self.debug:
            print(log_message)