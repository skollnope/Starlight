from typing import Any
import os
import json

class APIObject():
    _file:str = None
    _content:dict[str, Any] = None

    def __init__(self, 
                 group:list[str], 
                 name:str, 
                 api_key:str=None, 
                 additionnal_params:dict[str, Any]=None):

        # Create the file path
        group_path = os.path.join(*group)
        dir_path = os.path.join("c:/Starlight/APIs", group_path)
        file_path = os.path.join(dir_path, f"{name}.txt")

        # Ensure the directory exists
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        self._file = file_path
        
    def _read_file_content(self):
        if os.path.exists(self._file) and os.path.getsize(self._file) > 0:
            with open(self._file, 'r') as file:
                content = file.read()
                try:
                    self._content = json.loads(content)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file {self._file}")

    def save_content(self):
        with open(self._file, 'w') as file:
            json.dump(self._content, file, indent=4)