"""
 Modify Notes
"""
# pylint: disable=too-few-public-methods
from ...mysql.mysql_connection import MySqlConnection
from ...mysql.orm.autogen_entities import Task


class ModifyNotes(object):
    """
    ModifyNotes responsible to update the record in db
    """
    def __init__(self, db_name, notes_id, title=None, comment=None):
        super(ModifyNotes, self).__init__()
        self.data_db = 'data_{}'.format(db_name)
        self.notes_id = notes_id
        self.title = title
        self.comment = comment
        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

        self.results = self.modify_notes()

    def modify_notes(self):
        """
        function: query to update the notes record
        return: updated notes Id
        """
        notes_obj = self.session.query(Task). \
            filter_by(id=self.notes_id).first()
        notes_obj.title = self.title
        notes_obj.description = self.comment
        self.session.add(notes_obj)
        self.session.commit()
        return notes_obj.id
