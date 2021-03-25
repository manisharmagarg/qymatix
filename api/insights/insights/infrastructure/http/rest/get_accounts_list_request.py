import json
import logging
import traceback

from django.http import HttpResponse

from api.insights.insights.domain.accounts.customers_details \
    import CustomersDetails
from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.read.account_details_history \
    import AccountDetailsData
from api.insights.insights.infrastructure.mysql.read.accounts_list_history \
    import AccountsListData
from api.insights.insights.infrastructure.mysql.read.kam import KamFinder

logger = logging.getLogger(__name__)


def request_get_accounts_list(request):
    if request.method == 'GET':
        try:
            customer_id = request.GET.get('customer_id')
            page_number = request.GET.get('page_number')

            group_name = request.user.groups.all()[0]

            kam = None
            can_see_customer = True
            if request.user.configuration.account_type == 'basic':
                kam = get_kams(request)
                customer_ids = [customer.id for k in kam for customer in k.customers]

                if customer_id is not None:
                    can_see_customer = int(customer_id) in customer_ids

            if (kam is not None and customer_id is not None and can_see_customer) and page_number is None:
                customers_history = AccountDetailsData(
                    database=group_name,
                    customer_id=customer_id,
                    page_number=page_number,
                    kam=kam
                )

                accounts_history = CustomersDetails(
                    customers_history.results['customers_df'],
                    customers_history.results['sales_df'],
                    customers_history.results.get('customer_id'),
                    customers_history.results.get('page_number'),
                )

                response = json.dumps(
                    accounts_history.get_customers_details()
                )

            elif kam is not None and customer_id is None and page_number is not None:
                customers_history = AccountDetailsData(
                    database=group_name,
                    customer_id=customer_id,
                    page_number=page_number,
                    kam=kam
                )

                accounts_history = CustomersDetails(
                    customers_history.results['customers_df'],
                    customers_history.results['sales_df'],
                    customers_history.results.get('customer_id'),
                    customers_history.results.get('page_number'),
                )

                response = json.dumps(
                    accounts_history.get_customers_details()
                )

            elif kam is None and page_number is not None:
                customers_history = AccountDetailsData(
                    database=group_name,
                    customer_id=customer_id,
                    page_number=page_number,
                    kam=kam
                )

                accounts_history = CustomersDetails(
                    customers_history.results['customers_df'],
                    customers_history.results['sales_df'],
                    customers_history.results.get('customer_id'),
                    customers_history.results.get('page_number'),
                )

                response = json.dumps(
                    accounts_history.get_customers_details()
                )

            elif kam is None and customer_id is not None:
                customers_history = AccountDetailsData(
                    database=group_name,
                    customer_id=customer_id,
                    page_number=page_number,
                    kam=kam
                )

                accounts_history = CustomersDetails(
                    customers_history.results['customers_df'],
                    customers_history.results['sales_df'],
                    customers_history.results.get('customer_id'),
                    customers_history.results.get('page_number'),
                )

                response = json.dumps(
                    accounts_history.get_customers_details()
                )

            else:
                accounts_history = AccountsListData(group_name, kam)
                response = accounts_history.as_json()

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

    kam_finder = KamFinder(session)
    kam = kam_finder.get_kam_by_name(request.user.username)
    # group_finder = GroupFinder(session)
    # groups = group_finder.get_group_by_owner(kam.id)
    kam = [kam]

    return kam
