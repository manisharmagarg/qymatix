from api.infrastructure.mysql.orm import autogen_entities
import pandas as pd
import os
from numpy import nan
import datetime
from api.importer.importer.infrastructure.write.mysql.mysql_connection import MySqlConncetion
from api.importer.importer.infrastructure.mappings.clarus_mappings import ClarusMappings
from api.importer.importer.application.import_customer_command import ImportCustomerCommand
from api.importer.importer.application.bus import Bus
from api.importer.importer.domain.customer import Customer



class UploadClarusCustomers():

    DATABASE = 'data_clarus___films_com'

    def __init__(self, filename):
        super().__init__()

        connection = MySqlConncetion(self.DATABASE)
        self.session = connection.session()

        self.filename = filename

        self.mappings = ClarusMappings()

        command = ImportCustomerCommand(
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
            customer_name = row['account name']
            customer_industry = row['industry']

            if customer_name is not nan and customer_name is not None:

                customer = Customer(customer_name)

                if customer_industry is not nan and customer_industry != None:
                    customer.industry = customer_industry
                else:
                    customer.industry = ""

                try:
                    query = self.session.query(autogen_entities.Customer)\
                                            .filter_by(name=customer_name)\
                                            .first()

                    if query == None:
                        new = autogen_entities.Customer(
                                            name=customer_name,
                                            industry=customer.industry,
                                            address = '',
                                            postcode = '',
                                            city = '',
                                            country = '',
                                            revenue = 0,
                                            employees = 0,
                                            classification = '',
                                            website = '',
                                            comment = '',
                                            favorite = 0,
                                            telephone = '',
                                            customer_parent_id = '',
                                        )

                        self.session.add(new)
                        self.session.commit()
                        print(customer_name)

                except Exception as e:
                    print(e)


filename = '/Users/martin/Documents/cui/accounts/Clarus/ExcelExport_tblFaktStd_201909020919.xlsx'
filename = '/Users/martin/Documents/cui/accounts/Clarus/Auswertung Jan 2017 - Dez 2019.xlsx'

uploader = UploadClarusCustomers(filename)
uploader.upload()