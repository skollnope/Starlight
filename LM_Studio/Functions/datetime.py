from datetime import datetime
from typing import Any
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller, FunctionItem

get_local_time_def: dict[str, Any] = {"name": "get_local_time",
                                      "description": "return the date and the time"}
def get_local_time(args:dict[str, str]=None) -> str:
    return datetime.now().isoformat()

get_country_local_time_def: dict[str, Any] = {"name": "get_country_local_time",
                                            "description": "return the date time of the corresponding country"}
def get_country_local_time(args:dict[str, str]=None) -> str:
    return "I don't know what time is it in " + args["country"]

datetime_functions = FunctionCaller("DateTime")
datetime_functions.append_function(FunctionItem(get_local_time_def, get_local_time))