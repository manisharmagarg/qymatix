import json
import logging
import traceback

import numpy as np
import pandas as pd

from api.infrastructure.mysql import connection

logger = logging.getLogger(__name__)


class CustomersHistory:

    def __init__(self, database_name, kam=None):
        super().__init__()
        self.data_db = "data_{}".format(database_name)
        self.results_db = "results_{}".format(database_name)

        self.kam = kam

        self.mysql_connection = connection.MySQLConnection(self.data_db)
        self.con = self.mysql_connection.connect()
        self.cur = self.con.cursor()

        self.results = self.read_history()

    def read_history(self):
        try:
            if self.kam is None:
                query = "SELECT c.*, u.name AS 'kam', cr.sales, cr.size, " \
                        "cr.risk, cr.margin, cr.ppb, cr.ccbm, " \
                        "cr.product_cross_selling, " \
                        "cr.product_type_cross_selling " \
                        "FROM {data_db}.customers AS c " \
                        "LEFT JOIN {data_db}.Users_Customers AS uc " \
                        "ON c.id = uc.customer_id " \
                        "LEFT JOIN {data_db}.users AS u ON uc.user_id = u.id " \
                        "LEFT JOIN {results_db}.critters AS cr " \
                        "ON cr.name = c.id;".format(
                            data_db=self.data_db, results_db=self.results_db
                        )

            elif isinstance(self.kam, list):
                customer_ids = [customer.id for k in self.kam for customer in k.customers]
                query = "SELECT c.*, u.name AS 'kam', cr.sales, cr.size, " \
                        "cr.risk, cr.margin, cr.ppb, cr.ccbm, " \
                        "cr.product_cross_selling, " \
                        "cr.product_type_cross_selling " \
                        "FROM {data_db}.customers AS c " \
                        "LEFT JOIN {data_db}.Users_Customers AS uc " \
                        "ON c.id = uc.customer_id " \
                        "LEFT JOIN {data_db}.users AS u ON uc.user_id = u.id " \
                        "LEFT JOIN {results_db}.critters AS cr " \
                        "ON cr.name = c.id " \
                        "WHERE c.id IN {customer_ids}" \
                        .format(
                            data_db=self.data_db,
                            results_db=self.results_db,
                            customer_ids=str(tuple(customer_ids))
                        )

            self.cur.execute(query)
            data = np.asarray(self.cur.fetchall())
            cols = [desc[0] for desc in self.cur.description]
            customers_df = pd.DataFrame(data, columns=cols)

            return {
                "customers_df": customers_df
            }
        except (TypeError, ValueError, NameError, KeyError) as exception:
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
