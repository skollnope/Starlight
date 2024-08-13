from abc import ABC, abstractmethod
from typing import Any

from Starlight import APIAccess as api
from Starlight.Helpers.Helper_Functions import *
from Starlight.Helpers.messagehelper import *
from Starlight.context import *
from Functions.API.equipments import Equipment

class SentenceSniffer(ABC):
    _client:Any=None
    _model:str=None    
    _contexts:Context = Context()
    _equipments:list[Equipment] = []
    
    def __init__(self, model:str, contexts:Context, equipments:list[Equipment]):
        self._equipments = equipments
        self._contexts = contexts
        self._model=model

    @abstractmethod
    def __ask__(self, messages, model, temperature=0) -> str:
        pass

    def request4contexts(self, sentence:str) -> list[ContextObject]:
        prompt = DEFAULT_CTX_PROMPT + self._contexts.serialize()
        message = create_message_with_prompt(prompt, sentence)

        answ = self.__ask__(message)
        return ContextObject.deserialize(answ)

    def request4Equipments(self, sentence:str) -> list[Equipment]:
        prompt = "Prompt for the Equipment" + "" #TODO: Need to serialize all equipments
        message = create_message_with_prompt(prompt, sentence)

        answ = self.__ask__(message)
        return None

class OpenAISniffer(SentenceSniffer):
    def __init__(self, model:str):
        super.__init__(model)
        self._client = openai.OpenAI(api_key=get_openai_key())

    def __ask__(self, messages, temperature=0) -> str:
        completion = self._client.chat.completions.create(messages=messages,
                                                    model=self._model,
                                                    temperature=0)
        return completion.choices[0].message.content
        