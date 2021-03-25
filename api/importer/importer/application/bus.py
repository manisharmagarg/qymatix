import importlib


class Bus():

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.handler = None

    def find_handler(self):
        module = importlib.import_module(self.command.fqdn['module'])
        handler_class = getattr(module, self.command.fqdn['handler_class'])
        self.handler = handler_class(self.command)

    def dispatch(self):
        self.find_handler()
        return self.handler.handle()
