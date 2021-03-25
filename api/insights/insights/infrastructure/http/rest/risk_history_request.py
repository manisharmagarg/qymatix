import json
import logging

from django.http import HttpResponse

from api.insights.insights.domain.risk.churn_risk import ChurnRisk
from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
# from api.insights.insights.infrastructure.mysql.read.group_finder import GroupFinder
from api.insights.insights.infrastructure.mysql.read.kam import KamFinder
from api.insights.insights.infrastructure.mysql.read.risk_history import ChurnRiskHistory
from api.insights.insights.infrastructure.mysql.read.sales_history import SalesHistory

logger = logging.getLogger(__name__)


def request_risk_history(request):
    if request.method == 'GET':

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

        churn_risk_history = ChurnRiskHistory(group_name, kam)
        sales_history = SalesHistory(group_name, kam)

        churn_risk = ChurnRisk(
            churn_risk_history.results['churn_risk'],
            sales_history.last_year_sale()
        )

        response = json.dumps(churn_risk.get_indicators())

        return HttpResponse(response, content_type="application/json")

    response = json.dumps({
        "status_code": 405,
        "message": "Method Not Allowed"
    })

    return HttpResponse(response, content_type="application/json", status=405)
