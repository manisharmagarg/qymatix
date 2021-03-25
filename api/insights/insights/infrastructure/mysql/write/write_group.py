import datetime

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import Group, User


class WriteGroup:

    def __init__(self, domain, username):
        super().__init__()
        self.data_db = 'data_{}'.format(domain)

        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

        self.user = self.session.query(User).filter_by(username=username).first()

    def add_group(self, group_name, description=''):

        new_group = self.session.query(Group) \
            .filter_by(name=group_name) \
            .first()

        if new_group:
            return new_group

        new_group = Group(
            name=group_name,
            description=description,
            owner_id=self.user.id,
            created=datetime.datetime.now()
        )

        self.session.add(new_group)
        self.session.commit()
        return new_group

    def modify_group(self, group_id, fields_to_modify):
        selected_group = self.session.query(Group) \
            .filter_by(id=group_id) \
            .first()

        for field in fields_to_modify:
            setattr(selected_group, field, fields_to_modify[field])

        self.session.add(selected_group)
        self.session.commit()
        return selected_group


group = WriteGroup('clarus___films_com', 'test__clarus___films_com')

group1 = group.add_group('Group 1')
group1 = group.add_group('Group 2')

print(group1.description)

fields = {
    'description': '',
}

modified_group1 = group.modify_group(1, fields)

print(modified_group1.description)
