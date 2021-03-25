import json

from sqlalchemy import func
from sqlalchemy.orm import load_only

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import Sale, Customer, User


class MarginCustomerHistory:

    def __init__(self, database, customer_name, kam_name=None):
        super().__init__()
        self.data_db = 'data_{}'.format(database)

        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

        self.results = self.read_history(customer_name, kam_name)

    def read_history(self, customer_name, kam_name):

        fields = ['id', 'name']

        customer = self.session.query(Customer) \
            .options(load_only(*fields)) \
            .filter_by(name=customer_name) \
            .first()

        if kam_name is not None:
            kam = self.session.query(User) \
                .options(load_only(*fields)) \
                .filter_by(username=kam_name) \
                .first()

            results = self.session.query(
                Sale.year,
                Sale.month,
                func.sum(Sale.margin).label('total')
            ) \
                .filter_by(kam=kam.id) \
                .filter_by(customer_id=customer.id) \
                .group_by(Sale.year, Sale.month) \
                .all()

        else:
            results = self.session.query(
                Sale.year,
                Sale.month,
                func.sum(Sale.margin).label('total')
            ) \
                .filter_by(customer_id=customer.id) \
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
