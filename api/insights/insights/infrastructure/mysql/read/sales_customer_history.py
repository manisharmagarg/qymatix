"""
Query to get the sales customer history
"""
# pylint: disable=import-error
import json
from sqlalchemy import func
from sqlalchemy.orm import load_only
from ...mysql.mysql_connection import MySqlConnection
from ...mysql.orm.autogen_entities import Sale, Customer


class SalesCustomerHistory:
    """
    class is responsible to get the sale customer data from db
    """
    def __init__(self, database, customer_name, kam=None):
        super(SalesCustomerHistory, self).__init__()
        self.data_db = 'data_{}'.format(database)

        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

        self.kam = kam

        self.results = self.read_history(customer_name)

    def read_history(self, customer_name):
        """
        function: Query to get the sales data
        """
        fields = ['id', 'name']

        customer = self.session.query(Customer) \
            .options(load_only(*fields)) \
            .filter_by(name=customer_name) \
            .first()

        can_see_customer = True
        if isinstance(self.kam, list):
            customer_ids = [customer.id for k in self.kam for customer in k.customers]
            can_see_customer = customer.id in customer_ids

        results = None
        if can_see_customer:
            results = self.session.query(
                Sale.year,
                Sale.month,
                func.sum(Sale.price).label('total')
            ) \
                .filter_by(customer_id=customer.id) \
                .group_by(Sale.year, Sale.month) \
                .all()

        return results

    def as_array(self):
        """
        function: return sales data in list
        """
        sales_history = []
        for result in self.results:
            year = int(result.year)
            month = int(result.month)
            total = round(result.total, 2)

            sales_history.append([year, month, total])

        return sales_history

    def as_json(self):
        """
        function: return sales data in json format
        """
        sales_history = dict()
        modify_sales_history = dict()
        for result in self.results:
            year = int(result.year)
            month = int(result.month)
            total = round(result.total, 2)

            if year in sales_history:
                sales_history[year][month] = total
            else:
                sales_history[year] = {month: total}
        months_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for year_keys in sales_history:
            for list_months in months_list:
                months = sales_history.get(year_keys)
                if list_months in months.keys():
                    if year_keys in modify_sales_history:
                        modify_sales_history[year_keys][
                            list_months] = months.get(list_months)
                    else:
                        modify_sales_history[year_keys] = {
                            list_months: months.get(
                                list_months
                            )
                        }
                else:
                    if year_keys in modify_sales_history:
                        modify_sales_history[year_keys][list_months] = 0
                    else:
                        modify_sales_history[year_keys] = {list_months: 0}

        return json.dumps(modify_sales_history)
