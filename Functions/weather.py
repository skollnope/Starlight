from typing import Any
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller

get_weather_def: dict[str, Any] = {"name": "get_weather",
                                  "description": "return the weather of an unknown location"}
def get_weather(args=None):
    message = "it's raining"
    return message

weather_functions = FunctionCaller("Weather")
weather_functions.append_function(get_weather)