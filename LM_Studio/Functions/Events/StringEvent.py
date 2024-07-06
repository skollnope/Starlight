class StringEvent:
    def __init__(self):
        self.handlers = []

    def link(self, handler):
        self.handlers.append(handler)

    def unlink(self, handler):
        self.handlers.remove(handler)

    def emit(self, arg:str):
        for handler in self.handlers:
            handler(arg)