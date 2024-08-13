from abc import ABC, abstractmethod
from typing import Any

from Starlight import APIAccess as api
from Starlight.Helpers.Helper_Functions import *
from Starlight.Helpers.messagehelper import *
from Starlight.context import *
from Starlight.Functions.API.APIObject import APIObject

class ContextSniffer(ABC):
    _client:Any=None
    _model:str=None    
    _contexts:Context = Context()
    
    def __init__(self, model:str, contexts:Context):
        self._contexts = contexts
        self._model=model

    @abstractmethod
    def request4context(self, sentence:str) -> str:
        pass

    def request4Equipment(self, sentence:str) -> APIObject:
        pass

class OpenAIContextSniffer(ContextSniffer):
    def __init__(self, model:str):
        super. __init__(model)
        self._client = openai.OpenAI(api_key=get_openai_key())

    def request4context(self, sentence: str) -> str:
        prompt = DEFAULT_CTX_PROMPT + self._contexts.serialize()
        message = create_message_with_prompt(prompt, sentence)

        completion = self._client.chat.completions.create(messages=message,
                                                    model=self._model,
                                                    temperature=0)
            
        contexts = ContextObject.deserialize(completion.choices[0].message.content)
        return contexts
        