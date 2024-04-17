from openai import OpenAI
from Starlight.LM_Studio import constants as cst
from LM_Studio.Functions import function_calling as funcs

# Point to the local server
client = OpenAI(base_url=cst.MODEL_URL, api_key=cst.API_KEY)

message = [
    {"role": "system", "content": "Only answer to the question"},
    {"role": "user", "content": input("> ")},
]

completion = client.chat.completions.create(
    messages=message,
    model=cst.MODEL_DEFAULT,
    temperature=0.7)

print(completion.choices[0].message)