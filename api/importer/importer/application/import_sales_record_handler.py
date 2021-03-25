from api.importer.importer.application.handler_interface import HandlerInterface
from api.importer.importer.domain.data.sales_record_data_processor import SalesRecordDataProcessor 


class ImportSalesRecordHandler(HandlerInterface):

    def __init__(self, command):
        super().__init__()
        self.command = command

    def handle(self):

        processor = SalesRecordDataProcessor(
            filename=self.command.filename,
            mappings=self.command.mappings
        )

        return processor.data
        

