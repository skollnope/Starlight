from pywebostv.connection import WebOSClient
from pywebostv.controls import TvControl
from Starlight.LM_Studio.Functions.Equipments.LG.LGClient import *

from typing import Any

get_timezone_local_time_def: dict[str, Any] = {"name": "register_new_equipment",
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
def register_new_equipment(args:dict[str, str]):
    register(args["name"], args["ip"])
    