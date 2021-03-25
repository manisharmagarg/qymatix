import json
import logging
import traceback

from django.http import HttpResponse

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.read.accounts_history import ActiveAccountsHistory
# from api.insights.insights.infrastructure.mysql.read.group_finder import GroupFinder
from api.insights.insights.infrastructure.mysql.read.kam import KamFinder

logger = logging.getLogger(__name__)


def request_account_history(request):
    if request.method == 'GET':

        try:
            group_name = request.user.groups.all()[0]

            kam = get_kams(request)

            customers_history = ActiveAccountsHistory(group_name, kam)
            data = customers_history.read_active_accounts_history()
            active_history = customers_history.as_json(data)

            all_customer = customers_history.get_all_customer()
            cust_data = customers_history.as_array(all_customer)

            data = {
                "active_accounts": active_history,
                "lost_accounts": [a for a in cust_data if a not in active_history.keys()]
            }
            response = json.dumps(data)
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

        return HttpResponse(response, content_type="application/json", status=status)

    response = json.dumps({
        "status_code": 405,
        "message": "Method Not Allowed"
    })

    return HttpResponse(response, content_type="application/json", status=405)


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
