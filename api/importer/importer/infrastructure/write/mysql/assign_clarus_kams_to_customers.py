from api.infrastructure.mysql.orm import autogen_entities
import pandas as pd
import os
from numpy import nan
import datetime
from api.importer.importer.infrastructure.write.mysql.mysql_connection import MySqlConncetion
from api.importer.importer.infrastructure.mappings.clarus_mappings import ClarusMappings
from api.importer.importer.application.assign_kam_to_customer_command import AssignKamToCustomerCommand
from api.importer.importer.application.bus import Bus
from api.importer.importer.domain.customer import Customer



class AssignClarusKamsToCustomers():

    DATABASE = 'data_clarus___films_com'

    def __init__(self, filename):
        super().__init__()

        connection = MySqlConncetion(self.DATABASE)
        self.session = connection.session()

        self.filename = filename

        self.mappings = ClarusMappings()

        command = AssignKamToCustomerCommand(
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
        
            account_name = row['account name']
            kam_name = row['kam']

            if account_name is not nan and kam_name is not nan:

                kam = self.session.query(autogen_entities.User)\
                                        .filter_by(name=kam_name)\
                                        .first()

                customer = self.session.query(autogen_entities.Customer)\
                                        .filter_by(name=account_name)\
                                        .first()
                
                if customer != None and kam != None:
                    try:
                        # customer.users.append(kam)
                        # session.add(customer)
                        # session.commit()
                        print(customer.name)

                    except Exception as e:
                        print(e)


filename = '/Users/martin/Documents/cui/accounts/Clarus/ExcelExport_tblFaktStd_201909020919.xlsx'

uploader = AssignClarusKamsToCustomers(filename)
uploader.upload()