from sqlalchemy.orm import load_only

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import Group


class GroupFinder:

    def __init__(self, session=None, database_name=None):
        super().__init__()

        if session is None:
            self.session = self.get_connection(database_name)
        else:
            self.session = session

    @staticmethod
    def get_connection(database_name):
        data_db = "data_{}".format(database_name)
        connection = MySqlConnection(data_db)
        return connection.session()

    def get_group_by_name(self, group_name: str):
        if group_name is None:
            return None

        fields = ['id', 'name']
        return self.session.query(Group) \
            .options(load_only(*fields)) \
            .filter_by(name=group_name) \
            .first()

    def get_group_by_owner(self, owner_id: str):
        if owner_id is None:
            return None

        fields = ['id', 'owner_id']
        return self.session.query(Group) \
            .options(load_only(*fields)) \
            .filter_by(owner_id=owner_id) \
            .all()
