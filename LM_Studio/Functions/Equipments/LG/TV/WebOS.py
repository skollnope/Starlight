from pywebostv.connection import WebOSClient
from pywebostv.controls import TvControl
from Starlight.LM_Studio.Functions.Equipments.LG.LGClient import *

def register_new_equipment(args:dict[str, str]):
    register(args["name"], args["ip"])
    