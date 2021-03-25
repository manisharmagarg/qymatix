"""
API is responsible to get cross-selling, Churn-Risk and Price-Intelligence
bubble chart data
"""
# pylint: disable=import-error
# pylint: disable=relative-beyond-top-level
import json
import logging
import traceback
from django.http import HttpResponse
from ...mysql.read.get_chart_data import CustomerChartData
from ....domain.accounts.customers_details import CustomersDetails

logger = logging.getLogger(__name__)


def request_customers_chart_data(request):
    """
    function: request for get cross-selling, Churn-Risk and
    Price-Intelligence bubble chart data
    """
    if request.method == 'GET':

        try:
            group_name = request.user.groups.all()[0]
            customers_graph_history = CustomerChartData(group_name)
            accounts_graph_history = CustomersDetails(
                customers_graph_history.results['customers_df']
            )
            response = json.dumps(
                accounts_graph_history.get_customers_details()
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
            response = json.dumps({
                "status_code": 500,
                "message": "Internal Server Error",
                "err": str(traceback.format_exc())
            })
            status = 500

    else:
        response = ''
        status = 400

    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )
