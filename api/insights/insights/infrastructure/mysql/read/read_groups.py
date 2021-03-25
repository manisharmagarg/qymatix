from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import Group


class ReadGroups:

    def __init__(self, database, kam=None):
        super().__init__()
        self.data_db = 'data_{}'.format(database)

        self.session = self.create_session()

        self.results = self.get_groups(kam)

    def create_session(self):
        connection = MySqlConnection(self.data_db)
        return connection.session()

    def get_groups(self, kam):

        if kam is None:
            return self.session \
                .query(Group) \
                .all()

        if isinstance(kam, str):
            return self.session \
                .query(Group) \
                .filter_by(name=kam) \
                .all()

        if isinstance(kam, int):
            return self.session \
                .query(Group) \
                .filter_by(id=kam) \
                .all()

        if isinstance(kam, list):
            return self.session \
                .query(Group) \
                .filter(Group.id.in_(kam)) \
                .all()

        return None
