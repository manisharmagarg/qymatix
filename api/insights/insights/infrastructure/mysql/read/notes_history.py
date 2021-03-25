"""
 Notes records by action and customer id
"""
import json
from ...mysql.mysql_connection import MySqlConnection
from ...mysql.orm.autogen_entities import Task, Customer


class NotesHistory(object):
    """
    NotesHistory used for get the notes data from db
    """
    def __init__(self, db_name, customer_id=None):
        super(NotesHistory, self).__init__()
        self.data_db = 'data_{}'.format(db_name)
        self.customer_id = customer_id
        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

        self.results = self.read_notes()

    def read_notes(self):
        """
        function: query to get the record on the bases of customer id
        and action type.
        return: notes data object
        """
        if not self.customer_id:
            notes = self.session.query(
                Task.id, Task.account, Task.title,
                Task.description, Task.action,
                Customer.name
            ).filter(
                Task.account == Customer.id,
            ).filter_by(action="Notes").all()
        else:
            notes = self.session.query(
                Task.id, Task.account, Task.title,
                Task.description, Task.action,
                Customer.name
            ).filter(
                Task.account == Customer.id,
            ).filter_by(action="Notes", account=self.customer_id).all()

        return notes

    def as_json(self):
        """
        function: convert the notes record into json format
        return: notes record in json format
        """
        tasks_not = list()
        for task_notes in self.results:
            tasks_note = dict()
            tasks_note['id'] = task_notes.id
            tasks_note['account_id'] = task_notes.account
            tasks_note['account'] = task_notes.name
            tasks_note['title'] = task_notes.title
            tasks_note['comment'] = task_notes.description
            tasks_note['action'] = task_notes.action
            tasks_not.append(tasks_note)
        return json.dumps(tasks_not)
