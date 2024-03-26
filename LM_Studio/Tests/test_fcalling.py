from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

from Starlight.LM_Studio import constants as cst
from Starlight.LM_Studio.Functions import function_calling as funcs

# Point to the local server
client = OpenAI(base_url=cst.MODEL_URL, api_key=cst.API_KEY)

message = [
    {"role": "system", "content": "you have access to the following functions, use them."},
    {"role": "user", "content": "go to the next music"},
]

completion = client.chat.completions.create(
    messages=message,
    model=cst.DEFAULT_MODEL,
    temperature=0.7,
    tools=funcs.getFunctions(),
    tool_choice="hello_world")

if(completion.choices[0].finish_reason == "tool_calls"):
    calls = completion.choices[0].message.tool_calls
    for call in calls:
        name = call.function.name
        args = call.function.arguments
        funcs.invoke(name, args)

print(completion.choices[0].message.content)