from pywebostv.connection import WebOSClient
from Starlight.LM_Studio.Functions.API.APIObject import APIObject

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
