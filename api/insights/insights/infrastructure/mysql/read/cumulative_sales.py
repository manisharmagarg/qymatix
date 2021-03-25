"""
Query for retrive the cumulative sum of sales
"""
import datetime
import json

from sqlalchemy import text

from ...mysql.mysql_connection import MySqlConnection


class CumulativeSales:
    """
    Query for retrive the cumulative sum of sales
    """

    def __init__(self, db_name, _type, kam=None):
        super(CumulativeSales, self).__init__()
        self.kam = kam
        self.data_db = 'data_{}'.format(db_name)
        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

        self._type = _type

        self.results = self.get_cumulative_sales()

    def get_cumulative_sales(self):
        """
        Query to get sales
        """
        current_time = datetime.datetime.now()
        last_two_year = current_time.year - 2

        if self.kam is None:
            query = text("SELECT customer_id, sum({_type}) as "
                         "last_two_year_{_type}, "
                         "@running_{_type}:=@running_{_type} + sum({_type}) as "
                         "cumulative_{_type} "
                         "FROM sales JOIN (SELECT @running_{_type}:=0) r "
                         "WHERE year>={year} group by "
                         "customer_id;".format(year=last_two_year,
                                               _type=self._type))

        elif isinstance(self.kam, list):
            kam_ids = '(' + ','.join([str(k.id) for k in self.kam]) + ')'
            query = text(
                "SELECT customer_id, sum({_type}) as "
                "last_two_year_{_type}, "
                "@running_{_type}:=@running_{_type} + sum({_type}) as "
                "cumulative_{_type} "
                "FROM sales JOIN (SELECT @running_{_type}:=0) r "
                "WHERE year>={year} AND kam IN {kam_ids} "
                "GROUP BY customer_id;"
                .format(
                    year=last_two_year,
                    _type=self._type,
                    kam_ids=kam_ids
                )
            )

        return self.session.execute(query)

    def as_array(self):
        """
        function: get the list of cumulative sale and margin
        """
        cumulative_sales_list = []
        for result in self.results:
            if self._type == "price":
                cumulative_sales_list.append(
                    round(result.cumulative_price, 2)
                )
            else:
                cumulative_sales_list.append(
                    round(result.cumulative_margin, 2)
                )
        cumulative_sales_list.sort(reverse=True)
        return json.dumps(cumulative_sales_list)

    def as_json(self):
        """
        function: get the json response of cumulative sale and margin
        """
        cumulative_sales = list()
        for result in self.results:
            data = dict()
            if self._type == "price":
                data["customer_id"] = result.customer_id
                data["last_two_year_sale"] = round(
                    result.last_two_year_price, 2
                )
                data["cumulative_sale"] = round(
                    result.cumulative_price, 2
                )
            else:
                data["customer_id"] = result.customer_id
                data["last_two_year_margin"] = round(
                    result.last_two_year_margin, 2
                )
                data["cumulative_margin"] = round(
                    result.cumulative_margin, 2
                )
            cumulative_sales.append(data)
        return json.dumps(cumulative_sales)
