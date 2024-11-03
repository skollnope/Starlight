from Starlight.Functions.functions import FunctionCaller, FunctionItem
from Starlight.Functions.API.equipment import getAllEquipments
from typing import Any

get_all_equipments_def: dict[str, Any] = {"name": "get_all_equipments",
                                        "description": "return all equipments you can remote"}
def get_all_equipments(args:dict[str, str]=None) -> str:
    return getAllEquipments()

general_functions = FunctionCaller("General")
general_functions.append_function(FunctionItem(get_all_equipments_def, get_all_equipments))