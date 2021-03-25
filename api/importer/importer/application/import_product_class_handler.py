from api.importer.importer.application.handler_interface import HandlerInterface
from api.importer.importer.domain.data.product_class_data_processor import ProductClassDataProcessor


class ImportProductClassHandler(HandlerInterface):

    def __init__(self, command):
        super().__init__()
        self.command = command

    def handle(self):
        processor = ProductClassDataProcessor(
            filename=self.command.filename,
            mappings=self.command.mappings
        )

        return processor.data