from pywebostv.connection import WebOSClient
from Starlight.LM_Studio.Functions.API.APIObject import APIObject
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller, FunctionItem
from typing import Any

# start a register request to the specified equipment
def register(name:str, ip:str=""):
    api:APIObject = APIObject(name, ip)
    if ip != "":
        client = WebOSClient(ip)
    else:
        client = WebOSClient().discover()[0] # take first, sould improve it to get a list of equipment, then choose the right one
    
    store = {}
    client.connect() # start the connection

    for status in client.register(store):
        if status == WebOSClient.PROMPTED: # requested to valid the connection on the equipment
            print(f"Please accept the connection on the '{name}' equipment")
        elif status == WebOSClient.REGISTERED: # registered
            api.api_key = store[0]
            print(f"New equipment '{name}' just registered")

def connect(api_obj:APIObject) -> WebOSClient:
    if api_obj is None or not api_obj.registered:
        return None # unable to connect to the equipment
    
    client = WebOSClient(api_obj.ip)
    if client.register({"client-key": api_obj.api_key}) != WebOSClient.REGISTERED:
        return None # the current api key isn't valid (anymore ?)
    client.connect()
    return client

register_new_equipment_def: dict[str, Any] = {"name": "register_new_equipment",
                                              "description": "Register a new equipment to allow API accesses",
                                              "parameters": {
                                                  "type":"object",
                                                  "properties": {
                                                      "name": {
                                                          "type": "string",
                                                          "description": "The name of the new equipment to identify it among all others",
                                                      },
                                                      "ip": {
                                                          "type": "string",
                                                          "description": "The ip address where the equipment is located, must be in the IPV4 format",
                                                      },
                                                  },
                                                  "required": ["name", "ip"]}}
def register_new_equipment(args:dict[str, str]) -> str:
    register(args["name"], args["ip"])
    return "Finalized"

funcCaller:FunctionCaller = FunctionCaller("Equipment_LG")
funcCaller.append_function(FunctionItem(register_new_equipment_def, register_new_equipment))