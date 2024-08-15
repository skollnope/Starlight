from typing import Any, Callable

import Starlight.constants as cst 
from Starlight.Functions import hello_world as hw
from Starlight.Functions.Events.StringEvent import StringEvent
from Starlight.Helpers.Helper_Functions import *
from Starlight.context import ContextObject

class FunctionItem():
    _description:dict[str, Any]=None
    _func:Callable[[dict[str, str]], Any]=None
    _yield_event:StringEvent = None

    def __init__(self, description:dict[str, Any], func:Callable[[dict[str, str]], Any]):
        self._description = description
        self._func = func
        self._yield_event = StringEvent()

    @property
    def name(self) -> str:
        return str(self._description["name"])
    
    @property
    def desc(self) -> dict[str, Any]:
        return self._description

    def invoke(self, args:dict[str, str]) -> str:
        result = self._func(args)
        if isinstance(result, str):
            return result
        elif isinstance(result, Generator):
            for step in result:
                self._yield_event.emit(step)
            return get_generator_result(result)
        raise TypeError(f"Unknown return type for the following function: {self.name}")

class FunctionCaller():    
    _context:ContextObject
    _function_list:list[FunctionItem]=[]
    _yield_event:StringEvent = None

    def __init__(self, context:ContextObject, functions:list[FunctionItem]=[]):
        self._context = context
        for f in functions:
            self.append_function(f)
        self._yield_event = StringEvent()
    
    def append_function(self, func:FunctionItem):
        if func is not None:
            self._function_list.append(func)
            func._yield_event.link(self._yield_event.emit)
    
    def remove_function(self, name:str):
        func = self.get_function(name)
        if func is not None:
            func._yield_event.unlink(self._yield_event.emit)
            self._function_list.remove(func)

    @property
    def count(self) -> int:
        return self.functions.count

    @property
    def context(self) -> ContextObject:
        return self._context
    
    @property
    def functions(self) -> list[FunctionItem]:
        return self._function_list

    def get_function(self, name:str) -> FunctionItem:
        if self.functions is None:
            return None
         
        for func in self.functions:
            if func.name == name:
                return func
        return None
    
    def serialize(self) -> list[dict[str, Any]]:
        functions = []
        for item in self.functions:
              functions.append({"type": "function",
                                 "function": item.desc})
        
        return functions