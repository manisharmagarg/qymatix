from api.infrastructure.mysql.orm import autogen_entities
import pandas as pd
import os
from numpy import nan
import datetime
from api.importer.importer.infrastructure.write.mysql.mysql_connection import MySqlConncetion
from api.importer.importer.infrastructure.mappings.clarus_mappings import ClarusMappings
from api.importer.importer.application.import_product_command import ImportProductCommand
from api.importer.importer.application.bus import Bus
from api.importer.importer.domain.product import Product


class UploadClarusProduct():

    DATABASE = 'data_clarus___films_com'

    def __init__(self, filename):
        super().__init__()

        connection = MySqlConncetion(self.DATABASE)
        self.session = connection.session()

        self.filename = filename

        self.mappings = ClarusMappings()

        command = ImportProductCommand(
            filename=self.filename,
            mappings=self.mappings.mappings()
        )

        self.bus = Bus(command)

        # This could be replaced by an event
        self.data = self.bus.dispatch()


    def upload(self):
        '''
        '''
        for index, row in self.data.iterrows():
            product_name = row['product']

            if product_name is not nan:

                product = Product(product_name)

                query = self.session.query(autogen_entities.Product)\
                                        .filter_by(name=product_name)\
                                        .first()

                if query == None:
                    new = autogen_entities.Product(
                                        name=product.name,
                                        description='',
                                        product_type_id=1,
                                        number='',
                                        serial='',
                                        active=1,
                                        created=datetime.datetime.now()
                                     )

                    self.session.add(new)
                    self.session.commit()
                    print(product.name)


filename = '/Users/martin/Documents/cui/accounts/Clarus/ExcelExport_tblFaktStd_201909020919.xlsx'
filename = '/Users/martin/Documents/cui/accounts/Clarus/Auswertung Jan 2017 - Dez 2019.xlsx'

uploader = UploadClarusProduct(filename)
uploader.upload()