from sqlalchemy.orm import load_only

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import User


class KamFinder:

    def __init__(self, session=None):
        super().__init__()

        self.session = session

    @staticmethod
    def get_connection(database_name):
        data_db = "data_{}".format(database_name)
        connection = MySqlConnection(data_db)
        return connection.session()

    def get_kam_by_name(self, kam_name: str):
        if kam_name is None:
            return None

        fields = ['id', 'username']
        return self.session.query(User) \
            .options(load_only(*fields)) \
            .filter_by(username=kam_name) \
            .first()

    def get_kam_by_id(self, kam_id: int):
        if kam_id is None:
            return None

        fields = ['id', 'name']
        return self.session.query(User) \
            .options(load_only(*fields)) \
            .filter_by(id=kam_id) \
            .first()
