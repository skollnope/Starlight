from Starlight import constants as cst

class Context():
    _contexts:list[str] = [cst.CONTEXT_UNKNOWN]

    @property
    def contexts(self) -> list[str]:
        return self._contexts
    
    def append(self, context:str) -> bool:
        if not self.contains(context):
            self._contexts.append(context)
            return True
        else:
            print("The following context already exists '" + context + "'")
            return False
    
    def serialize(self) -> str:
        string = ""
        for h in self.contexts:
            string += h + ", "
        return string [:-2]

    
    def contains(self, context:str):
        for c in self.contexts:
            if c == context:
                return True
        return False
            
    