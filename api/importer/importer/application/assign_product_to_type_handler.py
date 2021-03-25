from api.importer.importer.application.handler_interface import HandlerInterface
from api.importer.importer.domain.data.product_to_type_data_processor import ProductToTypeDataProcessor


class AssignProductToTypeHandler(HandlerInterface):

    def __init__(self, command):
        super().__init__()
        self.command = command

    def handle(self):

        processor = ProductToTypeDataProcessor(
            filename=self.command.filename,
            mappings=self.command.mappings
        )

        return processor.data
        

