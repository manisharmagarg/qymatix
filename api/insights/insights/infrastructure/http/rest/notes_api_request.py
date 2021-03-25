"""
Notes Api request responsible to handle create notes, get notes, and
update the notes functionality.
"""

import json
import logging
import traceback

from django.http import HttpResponse
from django.views import View

from ...mysql.read.create_notes import CreateNotes
from ...mysql.read.modify_notes import ModifyNotes
from ...mysql.read.notes_history import NotesHistory

logger = logging.getLogger(__name__)


class NotesAPI(View):
    """
    NotesAPI class responsible to create, get and update records
    """

    @staticmethod
    def post(request):
        """
        function: crete the new notes
        return: new notes id
        """
        try:
            group_name = request.user.groups.all()[0]
            customer_id = request.GET.get('account_id')
            title = request.GET.get('title')
            comment = request.GET.get('comment')
            username = request.user.username
            notes_obj = CreateNotes(group_name)
            owner_id = notes_obj.get_owner(username)
            new_notes_id = notes_obj.create_notes(
                owner_id,
                customer_id,
                title,
                comment
            )
            response = json.dumps(
                {
                    "notes_id": new_notes_id,
                    "success": 200
                }
            )
            status = 200
        except (
                NameError,
                TypeError,
                KeyError,
                ValueError,
                AttributeError,
                IndexError
        ) as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )
            response = json.dumps(
                {
                    "status_code": 500,
                    "message": "Internal Server Error"
                }
            )
            status = 500
        return HttpResponse(
            response,
            content_type="application/json",
            status=status
        )

    @staticmethod
    def get(request):
        """
        function: fetching the notes data from the databases on the bases of
        customer id and action type
        return: notes records
        """
        try:
            group_name = request.user.groups.all()[0]
            customer_id = request.GET.get('customer_id')
            task_note_obj = NotesHistory(group_name, customer_id)
            response = task_note_obj.as_json()
            status = 200
        except (
                NameError,
                TypeError,
                KeyError,
                ValueError,
                AttributeError,
                IndexError
        ) as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )
            response = json.dumps(
                {
                    "status_code": 500,
                    "message": "Internal Server Error"
                }
            )
            status = 500
        return HttpResponse(
            response,
            content_type="application/json",
            status=status
        )

    @staticmethod
    def put(request):
        """
        function: update the notes record according to given filters
        """
        try:
            group_name = request.user.groups.all()[0]
            note_id = request.GET.get('id')
            title = request.GET.get('title')
            comment = request.GET.get('comment')
            notes_obj = ModifyNotes(group_name, note_id, title, comment)
            notes_obj.modify_notes()
            response = json.dumps(
                {
                    "mess": "Notes updated Successfully"
                }
            )
            status = 200
        except (
                NameError,
                TypeError,
                KeyError,
                ValueError,
                AttributeError,
                IndexError
        ) as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )
            response = json.dumps(
                {
                    "status_code": 500,
                    "message": "Internal Server Error"
                }
            )
            status = 500
        return HttpResponse(
            response,
            content_type="application/json",
            status=status
        )
