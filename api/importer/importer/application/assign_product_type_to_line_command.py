from api.importer.importer.application.command_interface import CommandInterface
from pathlib import Path


class AssignProductTypeToLineCommand(CommandInterface):

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
        module = "api.importer.importer.application.assign_product_type_to_line_handler"
        handler_class = "AssignProductTypeToLineHandler"

        return {'module': module, 'handler_class': handler_class}
