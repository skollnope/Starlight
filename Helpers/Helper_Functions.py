from typing import Any, Generator, Callable, get_type_hints, get_args
import openai

from Starlight.APIAccess import get_openai_key

# This function MUST be called when the whole generator has been browsed, otherwise, the result isn't the return one
def get_generator_result(gen: Generator[Any, Any, str]) -> str:
    try:
        next(gen) # as the generator is done, it will blow up
    except StopIteration as e:
        return str(e.value)  # Output: the result of the generators
    return None # is not ended, return None

def isOpenAIModel(model:str) -> bool:
    if(model.startswith("gpt")):
        return True
    return False
