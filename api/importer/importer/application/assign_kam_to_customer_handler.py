from api.importer.importer.application.handler_interface import HandlerInterface
from api.importer.importer.domain.data.kam_to_customer_data_processor import KamToCustomerDataProcessor 


class ImportCustomerHandler(HandlerInterface):

    def __init__(self, command):
        super().__init__()
        self.command = command

    def handle(self):

        processor = KamToCustomerDataProcessor(
            filename=self.command.filename,
            mappings=self.command.mappings
        )

        return processor.data
        

