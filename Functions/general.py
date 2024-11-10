from Starlight.Functions.functions import FunctionCaller, FunctionItem
from Starlight.Functions.API.equipment import getAllEquipments
from Starlight.context import ContextObject
from typing import Any

get_all_equipments_def: dict[str, Any] = {"name": "get_all_equipments",
                                        "description": "return all equipments you can remote"}
def get_all_equipments(args:dict[str, str]=None) -> str:
    return getAllEquipments()

general_context = ContextObject("General", description="General functions usable when you need to have deeper information about your accesses/rights")

general_functions = FunctionCaller("General")
general_functions.append_function(FunctionItem(get_all_equipments_def, get_all_equipments))