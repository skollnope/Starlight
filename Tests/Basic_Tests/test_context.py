from openai import OpenAI

from Starlight import constants as cst
from Starlight import APIAccess as api

# Point to the local server
client = OpenAI(api_key=api.get_openai_key())

contexts=["Unknown", "Weather", "Greet"]
prompt="You are an assistant which is requested to find the context of the sentence. Just answer with the following keywords: "
prompt += contexts[0] + ", "
prompt += contexts[1] + ", "
prompt += contexts[2]

message = [
    {"role": "system", "content": prompt},
    {"role": "user", "content": "did you bought a car ?"}
]

completion = client.chat.completions.create(
    messages=message,
    model=cst.MODEL_DEFAULT,
    temperature=0)

print(completion.choices[0].message)