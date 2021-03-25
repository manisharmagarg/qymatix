from api.importer.importer.application.command_interface import CommandInterface
from pathlib import Path


class AssignKamToCustomerCommand(CommandInterface):

    def __init__(self, filename: str, mappings):
        super().__init__()
        path = Path(filename)
        if path.is_file():
            self._filename = filename
        else:
            raise ValueError("File does not exists")

        self._mappings = mappings
    
    @property
    def filename(self):
        return Path(self._filename)
    
    @property
    def mappings(self):
        return self._mappings

    @property
    def fqdn(self):
        module = "api.importer.importer.application.assign_kam_to_customer_handler"
        handler_class = "AssignKamToCustomerHandler"

        return {'module': module, 'handler_class': handler_class}
