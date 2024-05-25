from Starlight.LM_Studio.Wrapper.openai_wrapper import OpenAIWrapper
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller, FunctionItem
import Starlight.LM_Studio.Functions.datetime as dt

wrapper = OpenAIWrapper(functions=[dt.datetime_functions])
wrapper.debug = True

while True:
    answer = wrapper.ask_something(question=input())
    print(answer)