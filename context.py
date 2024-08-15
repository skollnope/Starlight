from Starlight import constants as cst
from abc import ABC, abstractmethod
import json

DEFAULT_CTX_PROMPT = ("There is a list of Json object, you have to only answer a list, only, or none of those object which are relevant for the asked sentence. "
                    " Inside each Json Object, there is a 'value' key which is relevant to know the associated context of the object."
                    " If the 'description' key isn't empty, you can use it to have deeper information about the context."
                    " Also, the 'Type' key is relevant for the kind of action the context is associated for"
                    " If none of them stuck with the sentence, only answer with 'None'."
                    " If you find one or more, you must format you answer like: {\"choices\":[{\"type\":\"choice_type1\", \"value\":\"choice_value1\"}, ..., {\"type\":\"choice_typeN\", \"value\":\"choice_valueN\"}]}")


# below are the default values of a context's type
TYPE_FUNCTION_CALLING:str = "Function_Calling"
TYPE_EQUIPMENT_CONTROLLING:str = "Equipment_Controlling"

""" Contains information about a sentence's context

    type: the kind of context, usually "Function_Calling" but can have other values to add deeper context
    context: the name of the context to allow a model to identify one and choose it
    description: some additionnal information to help the model to correctly understand the purpose of the context

    you can use the serialize/deserialize method to manipulate them for/from a model
"""
class ContextObject(ABC):
    _type:str
    _ctx:str = TYPE_FUNCTION_CALLING
    _desc:str

    def __init__(self, context:str, type:str=TYPE_FUNCTION_CALLING, description:str=""):
        self._ctx = context
        self._type = type 
        self._desc = description
        pass

    def __eq__(self, value) -> bool:
        return self.type == value.type and self.context == value.context

    @property
    def type(self) -> str:
        return self._type
    
    @property
    def context(self) -> str:
        return self._ctx
    
    @property
    def description(self) -> str:
        return self._desc
    
    @staticmethod
    def deserialize(json_str:str):
        if json_str == "None": 
            return None
        
        obj = json.loads(json_str)
        lst = []
        for o in obj["choices"]:
            lst.append(ContextObject(o["value"], o["type"], o["description"]))
        return lst

    def __str__(self) -> str:
        json_obj = {'type':self.type, 'value':self.context, 'description':self.description}
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
            
    