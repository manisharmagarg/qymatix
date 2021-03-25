# pylint: skip-file
from sys import stdout

import pandas as pd

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.read.customer_finder import CustomerFinder
from api.insights.insights.infrastructure.mysql.read.kam import KamFinder

group_name = 'hartl___online_de'

data_db = "data_{}".format(group_name)

connection = MySqlConnection(data_db)

session = connection.session()

customer_finder = CustomerFinder(session)
kam_finder = KamFinder(session)

mapping = pd.read_excel('KDNR_KDNAME.xlsx')

mapping = mapping.dropna()

customers = []
total_number_of_rows = len(mapping.index)
for index, row in mapping.iterrows():

    customer = customer_finder.get_customer_by_name(row['ADRN'])

    if customer is None:
        print(str(row['ADRN']) + ' not found')
        continue

    customer.name = str(row['NAME']) + ' - ' + str(row['ADRN'])
    customer.customer_number = row['ADRN']

    customers.append(customer)

    if index % 2000 == 0:
        session.bulk_save_objects(customers)
        session.commit()
        customers = []

        stdout.write("Processed {} form {}\r".format(index, total_number_of_rows))
        stdout.flush()

session.bulk_save_objects(customers)
session.commit()
