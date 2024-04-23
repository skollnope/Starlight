from Starlight.LM_Studio.Wrapper.apiwrapper import APIWrapper
from Starlight.LM_Studio import constants as cst
from Starlight.LM_Studio import APIAccess as api
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller

from openai import OpenAI

class OpenAIWrapper(APIWrapper):
    model:str = ""
    client:OpenAI = None
    functions:list[FunctionCaller] = None

    def __init__(self, 
                 model:str=cst.MODEL_GPT35, 
                 functions:list[FunctionCaller]=None):
        super().__init__()
        self.model = model
        self.functions = functions
        self.client = OpenAI(api_key=api.get_openai_key())

    def create_message(self, prompt:str, user_sentence:str):
        return [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_sentence}
        ]
    
    def ask_for_context(self, sentence:str) -> str:
        # Implementation of method1 specific to this API
        prompt = self.serialize_contexts(cst.CONTEXT_PROMPT)
        message = self.create_message(prompt, sentence)

        completion = self.client.chat.completions.create(
            messages=message,
            model=cst.MODEL_DEFAULT,
            temperature=0)
        return completion.choices[0].message.content
    
    def ask_something(self, question:str) -> str:
        context = self.ask_for_context(question)

        functions = None
        if context != cst.CONTEXT_UNKNOWN:
            for caller in self.functions:
                if caller.context == context:
                    functions = caller.functions

        completion = self.client.chat.completions.create(
            messages=question,
            model=cst.MODEL_DEFAULT,
            temperature=0.7,
            tools=functions)
        return completion.choices[0].message.content



