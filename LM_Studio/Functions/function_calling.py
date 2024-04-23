from typing import Any

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

class FunctionCaller():    
    context:str
    functions:list[dict[str, Any]]

    def __init__(self, context:str, functions:dict[str, Any]=None):
         self.context = context
         self.functions = functions
    
    def append_function(self, func:dict[str, Any]):
         if self.functions is not None:
            self.functions.append(func)
    
    def remove_function(self, name:str):
         func = self.get_function(name)
         if func is not None:
              self.functions.remove(func)

    def get_function(self, name:str) -> dict[str, Any]:
         if self.functions is None:
              return None
         
         for func in self.functions:
              if func["name"] == name:
                   return func
         return None