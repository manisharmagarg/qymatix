# pylint: skip-file

import pandas as pd

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.read.product_finder import ProductFinder

group_name = 'hartl___online_de'

data_db = "data_{}".format(group_name)

connection = MySqlConnection(data_db)

session = connection.session()

product_finder = ProductFinder(session)

mapping = pd.read_excel('ARNR_Artikelbezeichnung.xlsx')

mapping = mapping.dropna()

mapping['ARNR'] = mapping['ARNR'].astype('str')
mapping['ARBE'] = mapping['ARBE'].astype('str')

products = []
total_number_of_rows = len(mapping.index)
for index, row in mapping.iterrows():

    product = product_finder.by_name(row['ARNR'])

    if product is None:
        print(str(row['ARNR']) + ' not found')
        continue

    product.description = row['ARBE']
    product.number = row['ARNR']

    products.append(product)

    if index % 2000 == 0:
        session.bulk_save_objects(products)
        session.commit()
        customers = []

session.bulk_save_objects(products)
session.commit()
