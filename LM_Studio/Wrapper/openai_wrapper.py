from Starlight.LM_Studio.Wrapper.apiwrapper import APIWrapper
from Starlight.LM_Studio import constants as cst
from Starlight.LM_Studio import APIAccess as api
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller

import json
from typing import Any
from openai import OpenAI

class OpenAIWrapper(APIWrapper):
    MODEL:str = ""
    CLIENT:OpenAI = None
    _available_functions:list[FunctionCaller] = None
    _history:list[dict[str, str]] = []
    debug:bool = False

    def __init__(self, 
                 model:str=cst.MODEL_GPT35, 
                 functions:list[FunctionCaller]=None,
                 prompt:str=cst.SYSTEM_PROMPT):
        super().__init__()
        self.MODEL = model
        self._available_functions = functions
        self.CLIENT = OpenAI(api_key=api.get_openai_key())

        self._history.append({"role": "system", "content": prompt})

    def create_message_with_prompt(self, prompt:str, message:str):
        return [
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
    
    def create_user_message(self, message:str):
        return {"role": "user", "content": message}
    
    def create_assistant_message(self, message:str):
        return {"role": "assistant", "content": message}
    
    def create_toolcalling_message(self, message:str):
        return {"role": "tool_calling", "content": message}
    
    def parse_args(str_args:str) -> dict[str, str]:
        json_obj = json.loads(str_args)
        return json_obj
    
    def ask_for_context(self, sentence:str) -> str:
        # Implementation of method1 specific to this API
        prompt = self.serialize_contexts(cst.CONTEXT_PROMPT)
        message = self.create_message_with_prompt(prompt, sentence)

        completion = self.CLIENT.chat.completions.create(
            messages=message,
            model=cst.MODEL_DEFAULT,
            temperature=0)
        
        if self.debug:
            print("The kept context for this sentence \"" + 
                  sentence + "\" is: " + 
                  completion.choices[0].message.content)
            
        return completion.choices[0].message.content
    
    def parse_reply(self, choice:Any, function_caller:FunctionCaller=None):
        finish_reason = choice.finish_reason
        if self.debug:
            print("finish reason: " + finish_reason)

        if finish_reason == "tool_calls" and function_caller is not None:
            for call in choice.message.tool_calls:
                result = function_caller.get_function(call.function.name).invoke(self.parse_args(call.function.arguments))
                self._history.append(self.create_toolcalling_message(result))
                
            completion = self.CLIENT.chat.completions.create(
                messages=self._history,
                model=self.MODEL,
                temperature=0.7)

            self.parse_reply(completion.choices[0])

        elif finish_reason == "stop":
            return choice.message.content

        pass
    
    def ask_something(self, question:str) -> str:
        context = cst.CONTEXT_UNKNOWN
        if self._available_functions is not None:
            context = self.ask_for_context(question)

        function_description:list[dict[str, Any]] = None
        if context != cst.CONTEXT_UNKNOWN:
            for caller in self._available_functions:
                if caller._context == context:
                    print(str(caller.count))
                    function_description = caller.serialize()

        self._history.append(self.create_user_message(question))

        completion = self.CLIENT.chat.completions.create(
            messages=self._history,
            model=self.MODEL,
            temperature=0.7,
            tools=function_description)
        
        reply = self.parse_reply(completion.choices[0])
        
        answ = self.create_assistant_message(reply)
        self._history.append(answ)
        return reply



