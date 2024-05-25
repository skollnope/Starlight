from Starlight.LM_Studio.Wrapper.apiwrapper import APIWrapper
from Starlight.LM_Studio import constants as cst
from Starlight.LM_Studio import APIAccess as api
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller

import json
from typing import Any
from openai import OpenAI
from openai.types.chat.chat_completion import Choice

class OpenAIWrapper(APIWrapper):
    _model:str = ""
    _client:OpenAI = None

    def __init__(self, 
                 model:str=cst.MODEL_GPT35, 
                 functions:list[FunctionCaller]=None,
                 prompt:str=cst.SYSTEM_PROMPT):
        super().__init__()
        self._model = model
        self._function_list = functions
        self._client = OpenAI(api_key=api.get_openai_key())

        self._history.append({"role": "system", "content": prompt})

    def create_message_with_prompt(self, prompt:str, message:str):
        return [
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
    
    @staticmethod
    def parse_args(str_args:str) -> dict[str, str]:
        json_obj = json.loads(str_args)
        return json_obj
    
    def ask_for_context(self, sentence:str) -> str:
        prompt = self.serialize_contexts(cst.CONTEXT_PROMPT)
        message = self.create_message_with_prompt(prompt, sentence)

        completion = self._client.chat.completions.create(
            messages=message,
            model=cst.MODEL_DEFAULT,
            temperature=0)
        
        self.log("The kept context for this sentence \"" + 
                  sentence + "\" is: " + 
                  completion.choices[0].message.content)
            
        return completion.choices[0].message.content
    
    def parse_reply(self, choice:Choice, function_caller:FunctionCaller=None) -> str:
        finish_reason = choice.finish_reason
        self.log("finish reason: " + finish_reason)

        if finish_reason == "tool_calls" and function_caller is not None:
            #first, store the answer inside the history
            self._history.append(self.create_assistant_toolcalls(choice.message.tool_calls))

            #call each function requested, then add the answers to the history
            for call in choice.message.tool_calls:
                self.log("trying to invoke '" + call.function.name + "' method with \n" + call.function.arguments + " args")
                result = function_caller.get_function(call.function.name).invoke(self.parse_args(call.function.arguments))
                self._history.append(self.create_toolcalling_message(result, call.id))
                
            #automatically send all function answers
            completion = self._client.chat.completions.create(
                messages=self._history,
                model=self._model,
                temperature=0.7)

            #return the final AI answer
            return self.parse_reply(completion.choices[0])

        elif finish_reason == "stop":
            #only text answer, just add it to the history then return the answer
            self._history.append(self.create_assistant_message(choice.message.content))
            return choice.message.content

        pass
    
    def ask_something(self, question:str) -> str:
        context = cst.CONTEXT_UNKNOWN
        if self._function_list is not None:
            context = self.ask_for_context(question)

        function_description:list[dict[str, Any]] = None
        if context != cst.CONTEXT_UNKNOWN:
            fCaller = self.get_methods_by_context(context)
            if fCaller is not None:
                function_description = fCaller.serialize()
                self.log("Function calling found for the '" + context + "' context")

        self.log(function_description)

        self._history.append(self.create_user_message(question))

        completion = self._client.chat.completions.create(
            messages=self._history,
            model=self._model,
            temperature=0.7,
            tools=function_description)
        
        return self.parse_reply(completion.choices[0], fCaller)



