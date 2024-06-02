class StringEvent:
    def __init__(self):
        self.handlers = []

    def register(self, handler):
        self.handlers.append(handler)

    def unregister(self, handler):
        self.handlers.remove(handler)

    def trigger(self, arg:str):
        for handler in self.handlers:
            handler(arg)