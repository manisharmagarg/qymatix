from api.infrastructure.mysql.orm import autogen_entities
import pandas as pd
import os
from numpy import nan
import datetime
from api.importer.importer.infrastructure.write.mysql.mysql_connection import MySqlConncetion
from api.importer.importer.infrastructure.mappings.clarus_mappings import ClarusMappings
from api.importer.importer.application.import_kam_command import ImportKamCommand
from api.importer.importer.application.bus import Bus



class UploadClarusKams():

    DATABASE = 'data_clarus___films_com'

    def __init__(self, filename):
        super().__init__()

        connection = MySqlConncetion(self.DATABASE)
        self.session = connection.session()

        self.filename = filename

        self.mappings = ClarusMappings()

        command = ImportKamCommand(
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
            kam_name = row['kam']

            if kam_name is not nan:

                query = self.session.query(autogen_entities.User)\
                                        .filter_by(name=kam_name)\
                                        .first()
                
                if query == None:

                    new_user = autogen_entities.User(
                                        name=kam_name,
                                        username='',
                                        description='',
                                        country='',
                                        phone='',
                                        email='',
                                        active=False,
                                        created=datetime.datetime.now()
                                    )

                    self.session.add(new_user)
                    self.session.commit()
                    print(kam_name)


filename = '/Users/martin/Documents/cui/accounts/Clarus/ExcelExport_tblFaktStd_201909020919.xlsx'
filename = '/Users/martin/Documents/cui/accounts/Clarus/Auswertung Jan 2017 - Dez 2019.xlsx'

uploader = UploadClarusKams(filename)
uploader.upload()