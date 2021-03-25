import json

from django.http import HttpResponse

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.read.kam import KamFinder
from api.insights.insights.infrastructure.mysql.read.sales_customer_history import SalesCustomerHistory
from api.insights.insights.infrastructure.mysql.read.sales_history import SalesHistory
from api.insights.insights.infrastructure.mysql.read.sales_kam_history import SalesKamHistory
from api.insights.insights.infrastructure.mysql.read.sales_product_history import SalesProductHistory


def request_sales_history(request):
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
            kam = [kam]

        if 'customer_name' in request.GET.keys():
            sales_history = SalesCustomerHistory(
                group_name,
                request.GET['customer_name'],
                kam
            )
        elif 'kam_name' in request.GET.keys():
            sales_history = SalesKamHistory(group_name, request.GET['kam_name'])
        elif 'product_name' in request.GET.keys():
            sales_history = SalesProductHistory(group_name, request.GET['product_name'])
        else:
            sales_history = SalesHistory(group_name, kam)

        response = sales_history.as_json()

        return HttpResponse(response, content_type="application/json")

    response = json.dumps({
        "status_code": 405,
        "message": "Method Not Allowed"
    })

    return HttpResponse(response, content_type="application/json", status=405)
