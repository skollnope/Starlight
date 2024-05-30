from typing import Any
import os
import json

api_default_directory:str = "c:/Starlight/APIs"
api_extension_file:str = ".txt"


if not os.path.exists(api_default_directory):
    os.makedirs(api_default_directory)

class APIObject():
    _file:str = None
    _content:dict[str, Any] = None

    def __init__(self, 
                 name:str,
                 ip:str=""):

        self._file = os.path.join(api_default_directory, f"{name}{api_extension_file}")
        if not self.read_file_content():
            self._content["name"] = name
            self._content["ip"] = ip
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
        
    def read_file_content(self) -> bool:
        if os.path.exists(self._file) and os.path.getsize(self._file) > 0:
            with open(self._file, 'r') as file:
                content = file.read()
                try:
                    self._content = json.loads(content)
                    return True
                except json.JSONDecodeError:
                    return False
        else:
            return False


    def save_content(self):
        with open(self._file, 'w') as file:
            json.dump(self._content, file, indent=4)