import json
import logging
import traceback

from django.http import HttpResponse

from api.insights.insights.domain.accounts.customers_details import CustomersDetails
from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.read.customers_history import CustomersHistory
# from api.insights.insights.infrastructure.mysql.read.group_finder import GroupFinder
from api.insights.insights.infrastructure.mysql.read.kam import KamFinder

logger = logging.getLogger(__name__)


def request_get_customers(request):
    if request.method == 'GET':

        try:
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

            customers_history = CustomersHistory(group_name, kam)
            customers_detail = CustomersDetails(
                customers_history.results['customers_df']
            )
            response = json.dumps(customers_detail.get_customers_details())
            return HttpResponse(
                response, content_type="application/json"
            )
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

    response = json.dumps({
        "status_code": 405,
        "message": "Method Not Allowed"
    })

    return HttpResponse(response, content_type="application/json", status=405)
