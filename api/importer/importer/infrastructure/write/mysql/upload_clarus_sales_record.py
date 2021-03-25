from api.infrastructure.mysql.orm import autogen_entities
import pandas as pd
import os
from numpy import nan
import datetime
from api.importer.importer.infrastructure.write.mysql.mysql_connection import MySqlConncetion
from api.importer.importer.infrastructure.mappings.clarus_mappings import ClarusMappings
from api.importer.importer.application.import_sales_record_command import ImportSalesRecordCommand
from api.importer.importer.application.bus import Bus
from api.importer.importer.domain.sales_record import SalesRecord



class UploadClarusSalesRecord():

    DATABASE = 'data_clarus___films_com'

    def __init__(self, filename):
        super().__init__()

        connection = MySqlConncetion(self.DATABASE)
        self.session = connection.session()

        self.filename = filename

        self.mappings = ClarusMappings()

        command = ImportSalesRecordCommand(
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
            invoice = row['invoice']
            price = row['price']
            margin = row['margin']
            customer_name = row['account name']
            product_name = row['product']
            kam = '' #row['kam']
            date = row['Date']
            quantity = row['quantity']

            if customer_name is not nan:

                try:
                    record = SalesRecord()
                    record.invoice = invoice
                    record.price = price
                    record.margin = margin
                    record.date = date
                    record.quantity = quantity 

                    product_query = self.session.query(autogen_entities.Product)\
                                            .filter_by(name=product_name)\
                                            .first()
                    
                    if product_query != None:
                        record.product_id = product_query.id

                    customer_query = self.session.query(autogen_entities.Customer)\
                                            .filter_by(name=customer_name)\
                                            .first()
                    
                    if customer_query != None:
                        record.customer_id = customer_query.id

                    user_query = self.session.query(autogen_entities.User)\
                                            .filter_by(name=kam)\
                                            .first()
                    
                    if user_query != None:
                        record.kam_id = user_query.id
                    else:
                        record.kam_id = 0


                    query = self.session.query(autogen_entities.Sale)\
                                            .filter_by(invoice=record.invoice)\
                                            .filter_by(price=record.price)\
                                            .first()
                                            # .filter_by(product_id=record.product_id)\
                    

                    if query == None:
                        new_customer = autogen_entities.Sale(
                                                invoice=record.invoice,
                                                price=record.price,
                                                margin=record.margin,
                                                cost=record.cost,
                                                product_id=record.product_id,
                                                customer_id=record.customer_id,
                                                quantity=record.quantity,
                                                kam=record.kam_id,
                                                date=record.date.strftime("%Y-%m-%d"),
                                                year=record.date.year,
                                                month=record.date.month,
                                    )

                        self.session.add(new_customer)
                        self.session.commit()
                        print("New sales record inserted: {}".format(record.invoice))
                    else:
                        print("Record exisits: {}".format(query.invoice))

                except Exception as e:
                    print(e)
                    raise


filename = '/Users/martin/Documents/cui/accounts/Clarus/ExcelExport_tblFaktStd_201909020919.xlsx'
filename = '/Users/martin/Documents/cui/accounts/Clarus/Auswertung Jan 2017 - Dez 2019.xlsx'

uploader = UploadClarusSalesRecord(filename)
uploader.upload()