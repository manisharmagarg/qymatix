from sqlalchemy.orm import load_only

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import Customer


class CustomerFinder:

    def __init__(self, session=None):
        super().__init__()

        self.session = session

    @staticmethod
    def get_connection(database_name):
        data_db = "data_{}".format(database_name)
        connection = MySqlConnection(data_db)
        return connection.session()

    def get_customer_by_name(self, customer_name: str) -> Customer:
        if customer_name is None:
            return None

        fields = ['id', 'name']
        return self.session.query(Customer) \
            .options(load_only(*fields)) \
            .filter_by(name=customer_name) \
            .first()

    def get_customer_by_id(self, customer_id: int):
        if customer_id is None:
            return None

        fields = ['id', 'name']
        return self.session.query(Customer) \
            .options(load_only(*fields)) \
            .filter_by(id=customer_id) \
            .first()
