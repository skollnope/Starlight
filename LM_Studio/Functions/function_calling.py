from typing import Any, Callable
import Starlight.LM_Studio.constants as cst 

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

class FunctionItem():
     _description:dict[str, Any]=None
     _func:Callable[[dict[str, str]], str]=None

     def __init__(self, description:dict[str, Any], func:Callable[[dict[str, str]], str]):
        self._description = description
        self._func = func

     @property
     def name(self) -> str:
         return str(self._description["name"])
    
     @property
     def desc(self) -> dict[str, Any]:
          return self._description

     def invoke(self, args:dict[str, str]) -> str:
         print("invoking method: " + self.name)
         return self._func(args)

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
         lst = []
         for item in self.functions:
              lst.append(item.desc)
         return lst