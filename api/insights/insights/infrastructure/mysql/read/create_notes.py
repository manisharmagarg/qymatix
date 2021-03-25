"""
Insert the notes in tasks
"""

import datetime
from ...mysql.mysql_connection import MySqlConnection
from ...mysql.orm.autogen_entities import Task, User


class CreateNotes:
    """
    CreateNotes used for create the new Notes.
    """
    def __init__(self, db_name):
        super(CreateNotes, self).__init__()
        self.data_db = 'data_{}'.format(db_name)

        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

    def get_owner(self, username):
        """
        Get User id(owner) on the bases of username
        """
        owner = self.session.query(User).filter_by(username=username).first()
        if owner:
            return owner.id
        return 0

    def create_notes(self, owner_id, customer_id, title, comment):
        """
        Query for Create new Note
        """
        created = datetime.datetime.now()
        task_obj = Task(
            account=customer_id,
            title=title,
            description=comment,
            owner_id=owner_id,
            group_id=1,
            action="Notes",
            created=created
        )
        self.session.add(task_obj)
        self.session.commit()
        return task_obj.id
