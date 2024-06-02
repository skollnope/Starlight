from typing import Any, Callable
import Starlight.LM_Studio.constants as cst 

from Starlight.LM_Studio.Functions import hello_world as hw
from Starlight.LM_Studio.Helpers.Helper_Functions import *

class FunctionItem():
     _description:dict[str, Any]=None
     _func:Callable[[dict[str, str]], Any]=None

     def __init__(self, description:dict[str, Any], func:Callable[[dict[str, str]], Any]):
        self._description = description
        self._func = func

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
                print(step) # Need to create an Event to allow step explanation by the model maybe
            return get_generator_result(result)
        raise TypeError(f"Unknown return type for the following function: {self.name}")

class FunctionCaller():    
     _context:str=""
     _function_list:list[FunctionItem]=[]

     def __init__(self, context:str, functions:list[FunctionItem]=[]):
         self._context = context
         self._function_list = functions
    
     def append_function(self, func:FunctionItem):
         if func is not None:
            self._function_list.append(func)
    
     def remove_function(self, name:str):
         func = self.get_function(name)
         if func is not None:
              self._function_list.remove(func)

     @property
     def count(self) -> int:
         return self.functions.count

     @property
     def context(self) -> str:
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