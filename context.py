from Starlight import constants as cst
from abc import ABC, abstractmethod
import json

DEFAULT_CTX_PROMPT = ("There is a list of Json object, you have to only answer a list, only, or none of those object which are relevant for the asked sentence. "
                    " Inside each Json Object, there is a 'value' key which is relevant to know the associated context of the object."
                    " If none of them stuck with the sentence, only answer with 'None'."
                    " If you find one or more, you must format you answer like: [{'choice1'}, {'choice2'}, ..., {'choiceN'}]")


TYPE_FUNCTION_CALLING:str = "Function_Calling"

class ContextObject(ABC):
    _type:str
    _ctx:str = TYPE_FUNCTION_CALLING

    def __init__(self, context:str, type:str=TYPE_FUNCTION_CALLING):
        self._ctx = context
        self._type = type 
        pass

    def __eq__(self, value) -> bool:
        return self.type == value.type and self.context == value.context

    @property
    def type(self) -> str:
        return self._type
    
    @property
    def context(self) -> str:
        return self._ctx
    
    @staticmethod
    def deserialize(json_str:str):
        if json_str == "None": 
            return None
        
        obj = json.loads(json_str)
        return ContextObject(obj["value"], obj["type"])

    def __str__(self) -> str:
        json_obj = {'type': self.type, 'value':self.context}
        return json.dumps(json_obj)

class Context():
    _contexts:list[ContextObject] = []

    @property
    def contexts(self) -> list[ContextObject]:
        return self._contexts
    
    def append(self, context:ContextObject) -> bool:
        if not self.contains(context):
            self._contexts.append(context)
            return True
        else:
            print("The following context already exists '" + str(context) + "'")
            return False
    
    def serialize(self) -> str:
        string = ""
        for h in self.contexts:
            string += str(h) + ","
        return string [:-1]

    
    def contains(self, context:ContextObject):
        for c in self.contexts:
            if c == context:
                return True
        return False
            
    