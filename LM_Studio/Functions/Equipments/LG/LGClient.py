from pywebostv.connection import WebOSClient
from pywebostv.controls import SystemControl, MediaControl

from Starlight.LM_Studio.Functions.API.APIObject import APIObject
from Starlight.LM_Studio.Functions.function_calling import FunctionCaller, FunctionItem
from typing import Any

# start a register request to the specified equipment
def register(name:str, ip:str=""):
    api:APIObject = APIObject(name, ip)
    if ip != "":
        client = WebOSClient(ip, secure=True)
    else:
        client = WebOSClient().discover()[0] # take first, sould improve it to get a list of equipment, then choose the right one
    
    store = {}
    client.connect() # start the connection

    for status in client.register(store):
        if status == WebOSClient.PROMPTED: # requested to valid the connection on the equipment
            print(f"Please accept the connection on the '{name}' equipment")
        elif status == WebOSClient.REGISTERED: # registered
            api.api_key = store["client_key"]
            print(f"New equipment '{name}' just registered")

def connect(api_obj:APIObject) -> WebOSClient:
    if api_obj is None or not api_obj.registered:
        return None # unable to connect to the equipment
    
    client:WebOSClient = None
    try:
        client = WebOSClient(api_obj.ip, secure=True)
        client.connect()
        client.register({"client_key": api_obj.api_key})
    except:
        print("Can't connect to the equipment")
        print({"client_key": api_obj.api_key})
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

pause_equipment_def: dict[str, Any] = {"name": "pause_equipment",
                                              "description": "pause the equipment",
                                              "parameters": {
                                                  "type":"object",
                                                  "properties": {
                                                      "name": {
                                                          "type": "string",
                                                          "description": "The name of the new equipment to identify it among all others",
                                                      }
                                                  },
                                                  "required": ["name"]}}
def pause_equipment(args:dict[str, str]) -> str:
    client = connect(APIObject(args["name"]))
    if client is None:
        return "Error while trying to connect to " + args["name"]
    try:
        media = MediaControl(client)
        media.pause(block=False)
    except Exception as e:
        return "Error while trying to pause the " + args["name"] + ". Error message: " + repr(e)
    
    return "Done"

notify_on_equipment_def: dict[str, Any] = {"name": "notify_on_equipment",
                                              "description": "send a notification message on a selected equipment",
                                              "parameters": {
                                                  "type":"object",
                                                  "properties": {
                                                      "name": {
                                                          "type": "string",
                                                          "description": "The name of the new equipment to identify it among all others",
                                                      },
                                                      "message": {
                                                          "type": "string",
                                                          "description": "The message to be shown",
                                                      }
                                                  },
                                                  "required": ["name", "message"]}}
def notify_on_equipment(args:dict[str, str]) -> str:
    client = connect(APIObject(args["name"]))
    if client is None:
        return "Error while trying to connect to " + args["name"]
    
    try:
        system = SystemControl(client)
        system.notify(args["message"])
    except Exception as e:
        return "Error while trying to send a notification message on the " + args["name"] + ". Error message: " + repr(e)

    return "Done"

lg_general_functions:FunctionCaller = FunctionCaller("Equipment_LG")
lg_general_functions.append_function(FunctionItem(register_new_equipment_def, register_new_equipment))
lg_general_functions.append_function(FunctionItem(pause_equipment_def, pause_equipment))
lg_general_functions.append_function(FunctionItem(notify_on_equipment_def, notify_on_equipment))