from api.importer.importer.application.handler_interface import HandlerInterface
from api.importer.importer.domain.data.kam_data_processor import KamDataProcessor


class ImportKamHandler(HandlerInterface):

    def __init__(self, command):
        super().__init__()
        self.command = command

    def handle(self):

        processor = KamDataProcessor(
            filename=self.command.filename,
            mappings=self.command.mappings
        )

        return processor.data
        

