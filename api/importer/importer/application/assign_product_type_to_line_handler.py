from api.importer.importer.application.handler_interface import HandlerInterface
from api.importer.importer.domain.data.product_type_to_line_data_processor import ProductTypeToLineDataProcessor


class AssignProductTypeToLineHandler(HandlerInterface):

    def __init__(self, command):
        super().__init__()
        self.command = command

    def handle(self):

        processor = ProductTypeToLineDataProcessor(
            filename=self.command.filename,
            mappings=self.command.mappings
        )

        return processor.data
        

