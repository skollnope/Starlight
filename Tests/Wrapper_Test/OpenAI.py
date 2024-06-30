from Starlight.LM_Studio.Wrapper.openai_wrapper import OpenAIWrapper
import Starlight.LM_Studio.Functions.datetime as dt
import Starlight.LM_Studio.Functions.Equipments.LG.LGClient as lgc

wrapper = OpenAIWrapper(functions=[dt.datetime_functions, lgc.lg_general_functions])
wrapper.debug = False

while True:
    answer = wrapper.ask_something(question=input())
    print(answer)