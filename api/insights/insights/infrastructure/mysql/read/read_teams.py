# pylint: skip-file

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import Group
from api.insights.insights.infrastructure.mysql.read.read_groups import ReadGroups


class Teams:

    def __init__(self, kam):
        super().__init__()

        self.kam = kam

    def get_teams(self):
        return self.kam.groups

    def get_own_teams(self):
        read_groups = ReadGroups()
        return self.kam.con
