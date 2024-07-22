from Starlight.Wrapper.openai_wrapper import OpenAIWrapper
import Starlight.Functions.datetime as dt
import Starlight.Functions.Equipments.LG.LGClient as lgc
from Starlight.context import DEFAULT_CTX_PROMPT

wrapper = OpenAIWrapper(functions=[dt.datetime_functions, lgc.lg_general_functions])
wrapper.debug = True

while True:
    answer = wrapper.ask_something(question=input())
    print(answer)