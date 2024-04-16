from Starlight.LM_Studio.Wrapper.apiwrapper import APIWrapper
from Starlight.LM_Studio import constants as cst
from Starlight.LM_Studio import APIAccess as api

from openai import OpenAI

class OpenAIWrapper(APIWrapper):
    model:str = ""
    client:OpenAI = None

    def __init__(self, model:str=cst.MODEL_GPT35):
        super().__init__()
        self.model = model
        self.client = OpenAI(api.get_openai_key())

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
        return completion.choices[0].message


