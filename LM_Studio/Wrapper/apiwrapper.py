from typing import Any
from abc import ABC, abstractmethod
from Starlight.LM_Studio import constants as cst
from Starlight.LM_Studio.Functions import function_calling as func
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller, FunctionItem

class APIWrapper(ABC):
    _function_list: list[FunctionCaller]

    def __init__(self):
        # Any common initialization code can go here
        pass

    CONTEXTS = [cst.CONTEXT_UNKNOWN, "Weather", "News", "DateTime"]
    def serialize_contexts(self, prompt:str):
        for context in self.CONTEXTS:
            prompt += context + ", "
        return prompt[:-2] #remove the last ', ' chars of the last context addition
    
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