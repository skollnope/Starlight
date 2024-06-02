from typing import Any, Generator, Callable, get_type_hints, get_args


# This function MUST be called when the whole generator has been browsed, otherwise, the result isn't the return one
def get_generator_result(gen: Generator[str, None, str]) -> str:
    try:
        next(gen) # as the generator is done, it will blow up
    except StopIteration as e:
        return e.value  # Output: the result of the generators
    return None # is not ended, return None

def get_return_type(callback:Callable) -> Any:
        type_hint = get_type_hints(callback)["arg"]
        arg_types, return_type = get_args(type_hint)
        return return_type