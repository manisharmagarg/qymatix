from api.infrastructure.mysql.orm import autogen_entities
import pandas as pd
import os
from numpy import nan
import datetime
from api.importer.importer.infrastructure.write.mysql.mysql_connection import MySqlConncetion
from api.importer.importer.infrastructure.mappings.clarus_mappings import ClarusMappings
from api.importer.importer.application.assign_product_to_type_command import AssignProductToTypeCommand
from api.importer.importer.application.bus import Bus
from api.importer.importer.domain.customer import Customer



class AssignClarusProductToType():

    DATABASE = 'data_clarus___films_com'

    def __init__(self, filename):
        super().__init__()

        connection = MySqlConncetion(self.DATABASE)
        self.session = connection.session()

        self.filename = filename

        self.mappings = ClarusMappings()

        command = AssignProductToTypeCommand(
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
        
            child = row['product']
            parent = row['product type']

            if child is not nan and parent is not nan:

                parent_query = self.session.query(autogen_entities.ProductType)\
                                        .filter_by(name=parent)\
                                        .first()

                child_query = self.session.query(autogen_entities.Product)\
                                        .filter_by(name=child)\
                                        .first()
                
                if parent_query != None and child_query != None:
                    try:
                        # child_query.users.append(kam)
                        # session.add(customer)
                        # session.commit()
                        print(child_query.name)

                    except Exception as e:
                        print(e)


filename = '/Users/martin/Documents/cui/accounts/Clarus/ExcelExport_tblFaktStd_201909020919.xlsx'

uploader = AssignClarusProductToType(filename)
uploader.upload()