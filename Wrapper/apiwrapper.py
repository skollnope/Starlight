from typing import Any
from abc import ABC, abstractmethod
from Starlight import constants as cst
from Starlight.Functions import function_calling as func
from Starlight.Functions.function_calling import FunctionCaller, FunctionItem
from Starlight.context import *
from Starlight.Helpers.sentencesniffer import SentenceSniffer

class APIWrapper(ABC):
    _function_list: list[FunctionCaller] = None
    _history:list[dict[str, str]] = []
    debug:bool = False
    _contexts:Context = Context()
    _sentenceSniffer:SentenceSniffer=None 

    def __init__(self, functions:list[FunctionCaller]):
        if functions is None:
            pass

        for f in functions:
            self._contexts.append(f.context)
        self._function_list = functions

    def __del__(self):
        if self.debug:
            self.print_history()
    
    def print_history(self):
        for h in self._history:
            print(h["role"] + ": " + h["content"])

    def serialize_contexts(self, prompt:str):
        return prompt + self._contexts.serialize()
    
    def append_function_caller(self, function:FunctionCaller):
        if self._contexts.append(function.context):
            self._function_list.append(function)
    
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

    def get_functions_by_context(self, context: list[ContextObject]) -> FunctionCaller:
        funcs = []
        remaining_funcs = self._function_list.copy() # create a copy to don't modify the reference
        for ctx in context:
            for func in remaining_funcs:
                if(func.context == ctx):                    
                    remaining_funcs.remove(func) # already found, no need to re-browse it
                    funcs.append(func) 
                    break
        return funcs

    @abstractmethod
    def parse_reply(answer:Any):
        pass

    def log(self, log_message:str):
        if self.debug:
            print(log_message)