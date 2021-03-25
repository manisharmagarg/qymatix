import json

from sqlalchemy import func

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import Sale


class MarginHistory:

    def __init__(self, database, kam=None):
        super().__init__()
        self.kam = kam
        self.data_db = 'data_{}'.format(database)

        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

        self.results = self.read_history()

    def read_history(self):

        if isinstance(self.kam, list):
            customer_ids = [customer.id for k in self.kam for customer in k.customers]

            results = self.session.query(
                Sale.year,
                Sale.month,
                func.sum(Sale.margin).label('total')
            ) \
                .filter(Sale.customer_id.in_(customer_ids)) \
                .group_by(Sale.year, Sale.month) \
                .all()
        else:
            results = self.session.query(
                Sale.year,
                Sale.month,
                func.sum(Sale.margin).label('total')
            ) \
                .group_by(Sale.year, Sale.month) \
                .all()

        return results

    def as_array(self):
        margin_history = []
        for result in self.results:
            year = int(result.year)
            month = int(result.month)
            total = round(result.total, 2)

            margin_history.append([year, month, total])

        return margin_history

    def as_json(self):
        margin_history = dict()
        for result in self.results:
            year = int(result.year)
            month = int(result.month)
            total = round(result.total, 2)

            if year in margin_history:
                margin_history[year][month] = total
            else:
                margin_history[year] = {month: total}

        return json.dumps(margin_history)
