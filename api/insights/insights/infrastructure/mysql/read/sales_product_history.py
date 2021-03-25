import json

from sqlalchemy import func
from sqlalchemy.orm import load_only

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import Sale, Product


class SalesProductHistory:

    def __init__(self, database, product_name):
        super().__init__()
        self.data_db = 'data_{}'.format(database)

        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

        self.results = self.read_history(product_name)

    def read_history(self, product_name):

        fields = ['id', 'name']

        product = self.session.query(Product) \
            .options(load_only(*fields)) \
            .filter_by(name=product_name) \
            .first()

        results = self.session.query(
            Sale.year,
            Sale.month,
            func.sum(Sale.price).label('total')
        ) \
            .filter_by(product_id=product.id) \
            .group_by(Sale.year, Sale.month) \
            .all()

        return results

    def as_array(self):
        sales_history = []
        for result in self.results:
            year = int(result.year)
            month = int(result.month)
            total = round(result.total, 2)

            sales_history.append([year, month, total])

        return sales_history

    def as_json(self):
        sales_history = dict()
        for result in self.results:
            year = int(result.year)
            month = int(result.month)
            total = round(result.total, 2)

            if year in sales_history:
                sales_history[year][month] = total
            else:
                sales_history[year] = {month: total}

        return json.dumps(sales_history)
