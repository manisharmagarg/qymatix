"""
get suggestions request responsible to get the suggestions for customer
as per their record
"""
# pylint: disable=import-error
# pylint: disable=relative-beyond-top-level
import json
import logging
import traceback

from django.http import HttpResponse

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.read.kam import KamFinder
from ...mysql.read.account_details_history import AccountDetailsData
from ...mysql.read.customers_suggestions import CustomerSuggestions
from ....domain.accounts.customers_details import CustomersDetails
from ....domain.suggestions.get_customer_suggestions import Suggestions

logger = logging.getLogger(__name__)


def request_get_suggestions(request):
    """
    Get suggestions request return the suggestion for customers
    """
    if request.method == 'GET':

        try:
            customer_id = request.GET['customer_id']
            group_name = request.user.groups.all()[0]

            kam = None
            # can_see_customer = True
            if request.user.configuration.account_type == 'basic':
                kam = get_kams(request)
                # customer_ids = [customer.id for k in kam for customer in k.customers]
                # can_see_customer = customer_id in customer_ids

            customers_history = AccountDetailsData(
                database=group_name,
                customer_id=customer_id,
                kam=kam
            )

            accounts_history = CustomersDetails(
                customers_history.results['customers_df'],
                customers_history.results['sales_df'],
                customers_history.results['customer_id']
            )

            customer = accounts_history.get_customers_details()

            get_insight = CustomerSuggestions(
                group_name, customer_id
            )

            get_insights = get_insight.results

            customer.update(get_insights)

            cust_suggestion = Suggestions(customer, customer_id)
            response = json.dumps(cust_suggestion.get_suggestions())
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
            response = {
                "status_code": 500,
                "message": "Internal Server Error"
            }
            status = 500
    else:
        response = ''
        status = 400
    return HttpResponse(
        response, content_type="application/json", status=status
    )


def get_kams(request):
    group_name = request.user.groups.all()[0]

    data_db = "data_{}".format(group_name)
    connection = MySqlConnection(data_db)
    session = connection.session()

    if request.user.configuration.account_type == 'basic':
        kam_finder = KamFinder(session)
        kam = kam_finder.get_kam_by_name(request.user.username)
        # group_finder = GroupFinder(session)
        # groups = group_finder.get_group_by_owner(kam.id)
        kam = [kam]

    return kam
