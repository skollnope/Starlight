from datetime import datetime
import pytz
from typing import Any
from Starlight.Functions.function_calling import FunctionCaller, FunctionItem
from Starlight.context import ContextObject

get_local_time_def: dict[str, Any] = {"name": "get_local_time",
                                      "description": "return a local date an time from an unknown location"}
def get_local_time(args:dict[str, str]=None) -> str:
    return datetime.now().isoformat()

get_timezone_local_time_def: dict[str, Any] = {"name": "get_timezone_local_time",
                                              "description": "return the date and the time from a specific timezone",
                                              "parameters": {
                                                  "type":"object",
                                                  "properties": {
                                                      "timezone": {
                                                          "type": "string",
                                                          "description": "the expected timezone",
                                                      },
                                                  },
                                                  "required": ["timezone"]}}
def get_timezone_local_time(args:dict[str, str]=None) -> str:
    current_time = datetime.now(pytz.timezone(args["timezone"]))
    return current_time.isoformat()

datetime_functions = FunctionCaller(ContextObject("DateTime"))
datetime_functions.append_function(FunctionItem(get_local_time_def, get_local_time))
datetime_functions.append_function(FunctionItem(get_timezone_local_time_def, get_timezone_local_time))