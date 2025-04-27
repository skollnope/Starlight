from Starlight.Wrapper.apiwrapper import APIWrapper
from Starlight import constants as cst
from Starlight import APIAccess as api
from Functions.functions import FunctionCaller, serialize_all_functions
from Functions.API.equipment import getAllEquipments
from Starlight.context import *
from Starlight.Helpers.messagehelper import *
from Starlight.Helpers.sentencesniffer import OpenAISniffer
from Starlight.Functions.general import general_functions

import json
from typing import Any
from openai import OpenAI
from openai.types.chat.chat_completion import Choice, ChatCompletion

class OpenAIWrapper(APIWrapper):
    _model:str = ""
    _client:OpenAI = None

    def __init__(self, 
                 model:str=cst.MODEL_GPT35, 
                 functions:list[FunctionCaller]=None,
                 prompt:str=cst.SYSTEM_PROMPT):
        super().__init__(functions)
        self._sentenceSniffer = OpenAISniffer(model, self._contexts, getAllEquipments())

        self._model = model
        self._client = OpenAI(api_key=api.get_openai_key())

        prompt += ""
        self._history.append({"role": "system", "content": prompt})
    
    @staticmethod
    def parse_args(str_args:str) -> dict[str, str]:
        json_obj = json.loads(str_args)
        return json_obj
    
    def create_chat(self, 
                    messages:list[dict[str, str]],
                    temperature:float=0.7, 
                    tools:list[dict[str, Any]]=None) -> ChatCompletion:
        return self._client.chat.completions.create(messages=messages,
                                                    model=self._model,
                                                    temperature=temperature,
                                                    tools=tools)
    
    def parse_reply(self, choice:Choice, function_caller:list[FunctionCaller]=None) -> str:
        finish_reason = choice.finish_reason
        self.log("finish reason: " + finish_reason)

        if finish_reason == "tool_calls" and function_caller is not None:
            # First, store the answer inside the history
            self._history.append(create_assistant_toolcalls(choice.message.tool_calls))

            # Call each function requested, then add the answers to the history
            for call in choice.message.tool_calls:
                self.log("trying to invoke '" + call.function.name + "' method with \n" + call.function.arguments + " args")

                # Browse the list of functions to find the matching one
                matching_function = next((fc.get_function(call.function.name) for fc in function_caller if fc.get_function(call.function.name) is not None), None)
                if matching_function:
                    result = matching_function.invoke(self.parse_args(call.function.arguments))
                    self.log("result is: " + result)
                    self._history.append(create_toolcalling_message(result, call.id))
                else:
                    self.log(f"No matching function found for '{call.function.name}'")

            # Automatically send all function answers
            completion = self.create_chat(messages=self._history)

            # Return the final AI answer
            return self.parse_reply(completion.choices[0], function_caller)

        elif finish_reason == "stop":
            # Only text answer, just add it to the history then return the answer
            self._history.append(create_assistant_message(choice.message.content))
            return choice.message.content

        pass
    
    def ask_something(self, question:str) -> str:
        context: list[ContextObject] = None
        if self._function_list is not None:
            context = self._sentenceSniffer.request4contexts(question)

        fCaller:list[FunctionCaller] = [general_functions]
        function_description:list[dict[str, Any]] = None
        if context:
            fCaller.extend(self.get_functions_by_context(context))
            if len(fCaller) != 0:
                function_description = serialize_all_functions(fCaller)
                self.log("Function calling found for the '" + '|'.join(str(x) for x in context) + "' context")

        self._history.append(create_user_message(question))

        completion = self.create_chat(messages=self._history, 
                                      tools=function_description)
        
        # TODO: give the whole fCaller list instead of the 1st one
        return self.parse_reply(completion.choices[0], fCaller)



