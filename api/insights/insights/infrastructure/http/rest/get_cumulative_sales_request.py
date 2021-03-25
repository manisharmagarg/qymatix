"""
API is responsible to get get cumulative sales
"""
# pylint: disable=import-error
import json
import logging
import traceback
from django.http import HttpResponse

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.read.kam import KamFinder
from ...mysql.read.cumulative_sales import CumulativeSales

logger = logging.getLogger(__name__)


def request_get_cumulative_sales(request):
    """
    function: request for get cumulative sales
    """
    if request.method == 'GET':

        try:
            kam = get_kams(request)

            group_name = request.user.groups.all()[0]
            sales_obj = CumulativeSales(group_name, _type="price", kam=kam)
            response = sales_obj.as_array()
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
            response = json.dumps({
                "status_code": 500,
                "message": "Internal Server Error"
            })
            status = 500

    else:
        response = ''
        status = 405

    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


def get_kams(request):
    group_name = request.user.groups.all()[0]

    data_db = "data_{}".format(group_name)
    connection = MySqlConnection(data_db)
    session = connection.session()

    kam = None
    if request.user.configuration.account_type == 'basic':
        limit_to_user = request.user.username
        kam_finder = KamFinder(session)
        kam = kam_finder.get_kam_by_name(limit_to_user)
        # group_finder = GroupFinder(session)
        # groups = group_finder.get_group_by_owner(kam.id)
        # kam = [user.id for user in group.users for group in groups]
        kam = [kam]

    return kam
