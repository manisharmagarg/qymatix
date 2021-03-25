import datetime
import json

from sqlalchemy import func

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import Sale, User


class SalesHistory:

    def __init__(self, database, kam=None):
        super().__init__()
        self.data_db = 'data_{}'.format(database)

        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

        self.kam = kam

        self.results = self.read_history()

    def read_history(self):

        # if self.kam is not None:
        if isinstance(self.kam, User):
            results = self.session.query(
                Sale.year,
                Sale.month,
                func.sum(Sale.price).label('total')
            ) \
                .filter_by(kam=self.kam.id) \
                .group_by(Sale.year, Sale.month) \
                .all()
        elif isinstance(self.kam, list):
            customer_ids = [customer.id for k in self.kam for customer in k.customers]
            results = self.session.query(
                Sale.year,
                Sale.month,
                func.sum(Sale.price).label('total')
            ) \
                .filter(Sale.customer_id.in_(customer_ids)) \
                .group_by(Sale.year, Sale.month) \
                .all()
        else:
            results = self.session.query(
                Sale.year,
                Sale.month,
                func.sum(Sale.price).label('total')
            ) \
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

    def last_year_sale(self):
        today = datetime.datetime.now()
        last_year = today.year - 1
        sales_history = json.loads(self.as_json())
        last_year_sales_dict = sales_history[str(last_year)]
        last_year_sales_values = last_year_sales_dict.values()
        last_year_sale_sum = sum(last_year_sales_values)
        return {
            'last_year_sale': round(last_year_sale_sum)
        }
