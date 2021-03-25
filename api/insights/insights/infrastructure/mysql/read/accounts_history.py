"""
ActiveAccountsHistory class return the active accounts records
"""
import datetime

from sqlalchemy import func  # pylint: disable=import-error

from ...mysql.mysql_connection import MySqlConnection
from ...mysql.orm.autogen_entities import Sale, Customer
from ...mysql.read.time_utils import months_difference


class ActiveAccountsHistory:
    """
    return active accounts
    """

    def __init__(self, database, kam):
        super(ActiveAccountsHistory, self).__init__()
        self.kam = kam
        self.data_db = 'data_{}'.format(database)

        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

    def read_active_accounts_history(self):
        """
        return the last three months customers(active)
        """
        today = datetime.datetime.now()
        last_three_months = months_difference(today, -3)

        if isinstance(self.kam, list):
            customer_ids = [customer.id for k in self.kam for customer in k.customers]

            results = self.session.query(
                Customer.id.label("customer_id"),
                func.sum(Sale.price).label('sales')
            ) \
                .outerjoin(Customer, Sale.customer_id == Customer.id) \
                .filter(Sale.customer_id.in_(customer_ids)) \
                .filter(Sale.date.between(last_three_months, today)) \
                .group_by(Customer.id) \
                .all()

        else:
            results = self.session.query(
                Customer.id.label("customer_id"),
                func.sum(Sale.price).label('sales')
            ) \
                .outerjoin(Customer, Sale.customer_id == Customer.id) \
                .filter(Sale.date.between(last_three_months, today)) \
                .group_by(Customer.id) \
                .all()

        return results

    @staticmethod
    def as_json(results):
        """
        return the customers in json format
        """
        accounts_history = dict()
        for result in results:
            accounts_history[int(result.customer_id)] = result.sales
        return accounts_history

    def get_all_customer(self):
        """
        return all customers from databases
        """
        results = self.session.query(
            Customer.id.label("customer_id"),
            Customer.name.label("customer_name")
        ) \
            .all()

        return results

    @staticmethod
    def as_array(customers):
        """
        return all customers in list format
        """
        customer_history = list()
        for result in customers:
            customer_history.append(result.customer_id)
        return customer_history
