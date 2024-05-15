from Starlight.LM_Studio.Wrapper.apiwrapper import APIWrapper
from Starlight.LM_Studio import constants as cst
from Starlight.LM_Studio import APIAccess as api
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller

from openai import OpenAI

class OpenAIWrapper(APIWrapper):
    MODEL:str = ""
    CLIENT:OpenAI = None
    FUNCTION_LIST:list[FunctionCaller] = None
    HISTORY:list[dict[str, str]] = []
    debug:bool = False

    def __init__(self, 
                 model:str=cst.MODEL_GPT35, 
                 functions:list[FunctionCaller]=None,
                 prompt:str=cst.SYSTEM_PROMPT):
        super().__init__()
        self.MODEL = model
        self.FUNCTION_LIST = functions
        self.CLIENT = OpenAI(api_key=api.get_openai_key())

        self.HISTORY.append({"role": "system", "content": prompt})

    def create_message_with_prompt(self, prompt:str, message:str):
        return [
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
    
    def create_user_message(self, message:str):
        return {"role": "user", "content": message}
    
    def create_assistant_message(self, message:str):
        return {"role": "assistant", "content": message}
    
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
    
    def ask_something(self, question:str) -> str:
        context = cst.CONTEXT_UNKNOWN
        if self.FUNCTION_LIST is not None:
            context = self.ask_for_context(question)

        functions = None
        if context != cst.CONTEXT_UNKNOWN:
            for caller in self.FUNCTION_LIST:
                if caller.context == context:
                    functions = caller.functions

        self.HISTORY.append(self.create_user_message(question))

        completion = self.CLIENT.chat.completions.create(
            messages=self.HISTORY,
            model=self.MODEL,
            temperature=0.7,
            tools=functions)
        
        answ = self.create_assistant_message(completion.choices[0].message.content)
        self.HISTORY.append(answ)
        return completion.choices[0].message.content



