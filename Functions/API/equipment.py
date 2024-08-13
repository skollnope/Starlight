from typing import Any
import os
import json

api_default_directory:str = "c:/Starlight/APIs"
api_extension_file:str = ".txt"


if not os.path.exists(api_default_directory):
    os.makedirs(api_default_directory)

# APIObjet content:
#   - Name, the name you want to give to the object (TV, HIFI, other)
#   - Room, the room the object is located (can be null) !!!!!!!!!!! TODO: add it to the file and store the files less flat
#   - ip, the ip to reach the object
#   - api_key = key to identify the requester (eq. to SSH)

# TODO: allow to "serialize" the object to allow the assisant to know them all

class Equipment():
    _file:str = None
    _content:dict[str, Any] = {}

    def __init__(self, 
                 name:str,
                 room:str = "",
                 ip:str=""):

        # define the file location
        if room:
            self.file = os.path.join(api_default_directory, room)
        else:
            self.file = api_default_directory
        self._file = os.path.join(self.file, f"{name}{api_extension_file}")
            
        # fill the api object content
        if not self.read_file_content():
            self._content["name"] = name
            self._content["ip"] = ip
            self._content["room"] = room
            self._content["api_key"] = ""
            self.save_content()
        elif ip != "" and ip != self.ip:
            self.ip = ip

    @property
    def name(self) -> str:
        return self._content["name"]
    
    @property
    def ip(self) -> str:
        return self._content["ip"]
    
    @ip.setter
    def ip(self, ip:str):
        self._content["ip"] = ip
        self.save_content()
    
    @property
    def api_key(self) -> str:
        return self._content["api_key"]

    @api_key.setter
    def api_key(self, api_key:str):
        self._content["api_key"] = api_key
        self.save_content()

    @property
    def registered(self) -> bool:
        return self.api_key != ""
    
    # returns a json object as string
    @property
    def serialize(self) -> str:
        return json.dump(self._content)
        
    def read_file_content(self) -> bool:
        if os.path.exists(self._file) and os.path.getsize(self._file) > 0:
            with open(self._file, 'r') as file:
                content = file.read()
                try:
                    self._content = json.loads(content)
                    return True
                except json.JSONDecodeError:
                    print("Error while reading the \"" + self._file + "\" file name")
                    return False
        else:
            return False


    def save_content(self):
        with open(self._file, 'w') as file:
            json.dump(self._content, file, indent=4)