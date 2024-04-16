from abc import ABC, abstractmethod
from Starlight.LM_Studio import constants as cst

class APIWrapper(ABC):
    def __init__(self):
        # Any common initialization code can go here
        pass

    CONTEXTS = [cst.CONTEXT_UNKNOWN, "Weather", "News", "Time"]
    def serialize_contexts(self, prompt:str):
        for context in self.CONTEXTS:
            prompt += context + ", "
        return prompt[:-2] #remove the last ', ' chars of the last context addition
    
    @abstractmethod #indicates that this method is overridable
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
    
    @abstractmethod
    def method2(self, params):
        pass