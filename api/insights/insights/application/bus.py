import importlib


class Bus():

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.handler = None

    def find_handler(self):
        module = importlib.import_module(self.command.get_path_and_class_name['module'])
        handler_class = getattr(module, self.command.get_path_and_class_name['handler_class'])
        self.handler = handler_class(self.command)

    def dispatch(self):
        self.find_handler()
        return self.handler.handle()
