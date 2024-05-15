from Starlight.LM_Studio.Wrapper.openai_wrapper import OpenAIWrapper

wrapper = OpenAIWrapper()
wrapper.debug = True

while True:
    answer = wrapper.ask_something(question=input())
    print(answer)