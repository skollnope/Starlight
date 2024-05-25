from Starlight.LM_Studio.Wrapper.openai_wrapper import OpenAIWrapper
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller, FunctionItem
import Starlight.LM_Studio.Functions.datetime as dt

#datetime_functions = FunctionCaller("DateTime")
#datetime_functions.append_function(FunctionItem(dt.get_local_time_def, dt.get_local_time))
wrapper = OpenAIWrapper(functions=[dt.datetime_functions])
wrapper.debug = True

while True:
    answer = wrapper.ask_something(question=input())
    print(answer)