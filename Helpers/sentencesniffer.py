from abc import ABC, abstractmethod
from typing import Any

from Starlight import APIAccess as api
from Starlight.Helpers.Helper_Functions import *
from Starlight.Helpers.messagehelper import *
from Starlight.context import *
from Functions.API.equipment import Equipment, DEFAULT_EQ_PROMPT

from openai import OpenAI

class SentenceSniffer(ABC):
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
        prompt = DEFAULT_EQ_PROMPT + Equipment.serialize(self._equipments)
        message = create_message_with_prompt(prompt, sentence)

        answ = self.__ask__(message)
        return Equipment.deserialize(answ)

class OpenAISniffer(SentenceSniffer):
    _client:OpenAI=None

    def __init__(self, model:str, contexts:Context, equipments:list[Equipment]):
        super.__init__(model, contexts, equipments)
        self._client = OpenAI(api_key=get_openai_key())

    def __ask__(self, messages, temperature=0) -> str:
        completion = self._client.chat.completions.create(messages=messages,
                                                    model=self._model,
                                                    temperature=temperature)
        return completion.choices[0].message.content
        