from api.importer.importer.application.handler_interface import HandlerInterface
from api.importer.importer.domain.data.product_type_data_processor import ProductTypeDataProcessor


class ImportProductTypeHandler(HandlerInterface):

    def __init__(self, command):
        super().__init__()
        self.command = command

    def handle(self):
        processor = ProductTypeDataProcessor(
            filename=self.command.filename,
            mappings=self.command.mappings
        )

        return processor.data