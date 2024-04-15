import os

def getKey(file_path:str = "./OpenAI_Key.txt"):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else: 
        return None