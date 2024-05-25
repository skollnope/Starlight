from datetime import datetime
from typing import Any
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller, FunctionItem

get_local_time_def: dict[str, Any] = {"name": "get_local_time",
                                      "description": "return a local date an time from an unknown location"}
def get_local_time(args:dict[str, str]=None) -> str:
    return datetime.now().isoformat()

get_country_local_time_def: dict[str, Any] = {"name": "get_country_local_time",
                                              "description": "return the date and the time from a specific country",
                                              "parameters": {
                                                  "type":"object",
                                                  "properties": {
                                                      "country": {
                                                          "type": "string",
                                                          "description": "the country",
                                                      },
                                                  },
                                                  "required": ["country"],
                                              }}
def get_country_local_time(args:dict[str, str]=None) -> str:
    return "I don't know what time is it in " + args["country"]

datetime_functions = FunctionCaller("DateTime")
datetime_functions.append_function(FunctionItem(get_local_time_def, get_local_time))
datetime_functions.append_function(FunctionItem(get_country_local_time_def, get_country_local_time))


    #  {"name": "get_current_weather",
    #   "description": "Get the current weather in a given location",
    #   "parameters": {
    #     "type": "object",
    #     "properties": {
    #       "location": {
    #         "type": "string",
    #         "description": "The city and state, e.g. San Francisco, CA",
    #       },
    #       "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
    #     },
    #     "required": ["location"],
    #   }}