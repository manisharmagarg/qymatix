from sqlalchemy.orm import load_only

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import Product


class ProductFinder:

    def __init__(self, session=None):
        super().__init__()

        self.session = session

    @staticmethod
    def get_connection(database_name):
        data_db = "data_{}".format(database_name)
        connection = MySqlConnection(data_db)
        return connection.session()

    def by_name(self, name: str) -> Product:
        if name is None:
            return None

        fields = ['id', 'name']
        return self.session.query(Product) \
            .options(load_only(*fields)) \
            .filter_by(name=name) \
            .first()

    def by_id(self, entity_id: int):
        if entity_id is None:
            return None

        fields = ['id', 'name']
        return self.session.query(Product) \
            .options(load_only(*fields)) \
            .filter_by(id=entity_id) \
            .first()
