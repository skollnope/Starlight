from typing import Any
from abc import ABC, abstractmethod
from Starlight import constants as cst
from Functions import functions as func
from Functions.functions import FunctionCaller, FunctionItem
from Starlight.context import *
from Starlight.Helpers.sentencesniffer import SentenceSniffer
from Starlight.Functions.general import general_context

class APIWrapper(ABC):
    _function_list: dict[ContextObject, FunctionCaller] = {}
    _history:list[dict[str, str]] = []
    debug:bool = False
    _contexts:Context = Context()
    _sentenceSniffer:SentenceSniffer=None 

    def __init__(self, functions:list[FunctionCaller]):
        if functions is None:
            pass    

        self._contexts.append(general_context)
        for f in functions:
            self._contexts.append(f.context)
            self._function_list[f.context] = f

    def __del__(self):
        if self.debug:
            self.print_history()
    
    def print_history(self):
        for h in self._history:
            print(h["role"] + ": " + h["content"])
    
    def append_function_caller(self, function:FunctionCaller):
        if self._contexts.append(function.context):
            self._function_list.append(function)

    def get_functions_by_context(self, context: list[ContextObject]) -> list[FunctionCaller]:
        funcs = []
        for ctx in context:
            for func in self._function_list.values():
                if(func.context == ctx):                    
                    funcs.append(func) 
                    break
        return funcs

    @abstractmethod
    def parse_reply(answer:Any):
        pass

    def log(self, log_message:str):
        if self.debug:
            print(log_message)

    def log_debug(self, log_message:str):
        if self.debug:
            print("\033[94mDEBUG: " + log_message + "" "\033[0m")

    def log_error(self, log_message:str):
        if self.debug:
            print("\033[91mERROR: " + log_message + "" "\033[0m")
            
    def log_info(self, log_message:str):
        if self.debug:
            print("\033[92mINFO: " + log_message + "" "\033[0m")
            
    def log_warning(self, log_message:str):
        if self.debug:
            print("\033[93mWARNING: " + log_message + "" "\033[0m")