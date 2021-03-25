from api.importer.importer.application.handler_interface import HandlerInterface
from api.importer.importer.domain.data.product_line_data_processor import ProductLineDataProcessor


class ImportProductLineHandler(HandlerInterface):

    def __init__(self, command):
        super().__init__()
        self.command = command

    def handle(self):
        processor = ProductLineDataProcessor(
            filename=self.command.filename,
            mappings=self.command.mappings
        )

        return processor.data