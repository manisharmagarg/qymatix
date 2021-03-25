from api.importer.importer.application.handler_interface import HandlerInterface
from api.importer.importer.domain.data.customer_data_processor import CustomerDataProcessor


class ImportCustomerHandler(HandlerInterface):

    def __init__(self, command):
        super().__init__()
        self.command = command

    def handle(self):

        processor = CustomerDataProcessor(
            filename=self.command.filename,
            mappings=self.command.mappings
        )

        return processor.data
        

