from Starlight.LM_Studio.Wrapper.openai_wrapper import OpenAIWrapper

wrapper = OpenAIWrapper()
context = wrapper.ask_for_context("is it raining ?")
print(context)