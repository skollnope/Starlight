from openai import OpenAI
import json
import re

from Starlight.LM_Studio import constants as cst
from Starlight.LM_Studio.Functions import function_calling as funcs

# Point to the local server
client = OpenAI(base_url=cst.MODEL_URL, api_key=cst.API_KEY)

messages = [
    {"role": "system", "content": f"You are a helpful assistant with access to the following functions. Use them if required- {json.dumps(funcs.getFunctions())}"},
    {"role": "user", "content": "what's your name ?"},
]

completion = client.chat.completions.create(
    messages=messages,
    model=cst.DEFAULT_MODEL,
    temperature=0.3)

message = completion.choices[0].message.content
print(message)

messages.append({"role": "assistant", "content": message})
match = re.search(r"<functioncall>(.*?)<", message, re.DOTALL)
if not match:
    print("No function needed")
else:
    print("function needed")