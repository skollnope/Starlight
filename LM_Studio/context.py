from Starlight.LM_Studio import constants as cst

class Context():
    _contexts:list[str] = [cst.CONTEXT_UNKNOWN, 
                           "Weather", 
                           "News", 
                           "DateTime"]

    @property
    def contexts(self) -> list[str]:
        return self._contexts
    
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
            
    