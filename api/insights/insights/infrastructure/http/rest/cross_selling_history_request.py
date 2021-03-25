import json
import logging
import traceback

from django.http import HttpResponse

from api.insights.insights.domain.ccbm.cross_selling \
    import CrossSelling
from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.read.kam import KamFinder
from api.insights.insights.infrastructure.mysql.read.sales_history \
    import SalesHistory
from api.insights.insights.infrastructure.mysql.read.selling_history \
    import CrossSellingHistory

logger = logging.getLogger(__name__)


def request_selling_history(request):
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
                kam = [kam]

            selling_history = CrossSellingHistory(group_name, kam)
            sales_history = SalesHistory(group_name, kam)

            cross_selling = CrossSelling(
                selling_history.results['cross_selling'],
                sales_history.last_year_sale()
            )
            response = json.dumps(cross_selling.get_indicators())
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


    response = json.dumps({
        "status_code": 405,
        "message": "Method Not Allowed"
    })

    return HttpResponse(response, content_type="application/json", status=405)
