import json
import logging
import traceback

import numpy as np
import pandas as pd

from api.infrastructure.mysql import connection

logger = logging.getLogger(__name__)


class AccountDetailsData:

    PAGE_LIMIT = 100

    def __init__(self, database, customer_id=None, page_number=None, kam=None):
        super().__init__()
        self.kam = kam
        self.data_db = "data_{}".format(database)
        self.results_db = "results_{}".format(database)

        mysql_connection = connection.MySQLConnection(self.data_db)
        con = mysql_connection.connect()
        self.cur = con.cursor()

        self.page_number = page_number
        self.page_limit = self.PAGE_LIMIT

        self.results = self.read_account_details(customer_id)

    def read_account_details(self, customer_id=None):
        if self.page_number:
            off_set = (int(self.page_number)-1) * self.page_limit

        account_details = dict()
        try:
            if customer_id is not None:
                query = "SELECT c.*, u.name AS 'kam', cr.sales, cr.size, "\
                    "cr.risk, cr.margin, cr.ppb, cr.ccbm, "\
                    "cr.product_cross_selling, "\
                    "cr.product_type_cross_selling "\
                    "FROM {data_db}.customers AS c "\
                    "LEFT JOIN {data_db}.Users_Customers AS uc "\
                    "ON c.id = uc.customer_id "\
                    "LEFT JOIN {data_db}.users AS u ON uc.user_id = u.id "\
                    "LEFT JOIN {results_db}.critters AS cr "\
                    "ON cr.name = c.id where c.id = {customer_id};".format(
                        data_db=self.data_db, results_db=self.results_db,
                        customer_id=customer_id
                    )

                account_details["customer_id"] = customer_id

            elif customer_id is None and self.kam is not None and self.page_number is not None:
                customer_ids_string = str(tuple([customer.id for k in self.kam for customer in k.customers]))

                query = "SELECT c.*, u.name AS 'kam', cr.sales, cr.size, "\
                    "cr.risk, cr.margin, cr.ppb, cr.ccbm, "\
                    "cr.product_cross_selling, "\
                    "cr.product_type_cross_selling "\
                    "FROM {data_db}.customers AS c "\
                    "LEFT JOIN {data_db}.Users_Customers AS uc "\
                    "ON c.id = uc.customer_id "\
                    "LEFT JOIN {data_db}.users AS u ON uc.user_id = u.id "\
                    "LEFT JOIN {results_db}.critters AS cr "\
                    "ON cr.name = c.id " \
                    "WHERE c.id IN {kam_ids} " \
                    "LIMIT {page_limit} OFFSET {off_set} " \
                    .format(
                        data_db=self.data_db, results_db=self.results_db,
                        page_limit=self.page_limit, off_set=off_set,
                        kam_ids=customer_ids_string
                    )

                account_details["page_number"] = self.page_number

            elif customer_id is None and self.kam is None and self.page_number is not None:

                query = "SELECT c.*, u.name AS 'kam', cr.sales, cr.size, "\
                    "cr.risk, cr.margin, cr.ppb, cr.ccbm, "\
                    "cr.product_cross_selling, "\
                    "cr.product_type_cross_selling "\
                    "FROM {data_db}.customers AS c "\
                    "LEFT JOIN {data_db}.Users_Customers AS uc "\
                    "ON c.id = uc.customer_id "\
                    "LEFT JOIN {data_db}.users AS u ON uc.user_id = u.id "\
                    "LEFT JOIN {results_db}.critters AS cr "\
                    "ON cr.name = c.id " \
                    "LIMIT {page_limit} OFFSET {off_set} " \
                    .format(
                        data_db=self.data_db, results_db=self.results_db,
                        page_limit=self.page_limit, off_set=off_set
                    )
                account_details["page_number"] = self.page_number

            if self.kam is None:
                ssales_query = "SELECT cr.sales as sales, " \
                           "cr.margin as margin, " \
                           "cr.risk as risk, " \
                           "cr.ppb as ppb, " \
                           "cr.ccbm as ccbm " \
                           "FROM {results_db}.critters AS cr ;".format(
                               results_db=self.results_db
                           )

            if isinstance(self.kam, list):
                customer_ids = [customer.id for k in self.kam for customer in k.customers]
                ssales_query = "SELECT cr.sales as sales, " \
                               "cr.margin as margin, " \
                               "cr.risk as risk, " \
                               "cr.ppb as ppb, " \
                               "cr.ccbm as ccbm " \
                               "FROM {results_db}.critters AS cr " \
                               "WHERE cr.name IN {customer_ids}" \
                               .format(
                                   results_db=self.results_db,
                                   customer_ids=str(tuple(customer_ids))
                               )

            self.cur.execute(query)
            data = np.asarray(self.cur.fetchall())
            cols = [desc[0] for desc in self.cur.description]

            self.cur.execute(ssales_query)
            ssales_max_values_data = np.asarray(self.cur.fetchall())
            ssales_max_values_cols = [desc[0] for desc in self.cur.description]

            customer_details_df = pd.DataFrame(data, columns=cols)
            sales_df = pd.DataFrame(
                ssales_max_values_data, columns=ssales_max_values_cols
            )
            account_details["customers_df"] = customer_details_df
            account_details["sales_df"] = sales_df

            return account_details

        except (NameError, TypeError, KeyError, ValueError) as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )

    def as_json(self):
        return json.dumps(self.results)
