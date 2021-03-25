from api.importer.importer.application.handler_interface import HandlerInterface
from api.importer.importer.domain.data.product_line_to_class_data_processor import ProductLineToClassDataProcessor 


class AssignProductLineToClassHandler(HandlerInterface):

    def __init__(self, command):
        super().__init__()
        self.command = command

    def handle(self):

        processor = ProductLineToClassDataProcessor(
            filename=self.command.filename,
            mappings=self.command.mappings
        )

        return processor.data
        

