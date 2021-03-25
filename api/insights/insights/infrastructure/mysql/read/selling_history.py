import json
import logging
import traceback

import numpy as np
import pandas as pd

from api.infrastructure.mysql import connection

logger = logging.getLogger(__name__)


class CrossSellingHistory:

    def __init__(self, database_name, kam):
        super().__init__()

        self.results_db = "results_{}".format(database_name)
        self.data_db = "data_{}".format(database_name)

        self.kam = kam

        self.mysql_connection = connection.MySQLConnection(self.results_db)
        self.con = self.mysql_connection.connect()
        self.cur = self.con.cursor()

        self.results = self.read_history()

    def read_history(self):
        try:
            if self.kam is None:
                query = "SELECT ROUND(AVG(ccbm), 2) AS ccbm, " \
                        "ROUND(AVG(ppb), 2) AS ppb, " \
                        "ROUND(AVG(risk), 2) AS risk " \
                        "FROM {results_db}.critters;".format(
                            results_db=self.results_db
                        )

            elif isinstance(self.kam, list):
                customer_ids = [customer.id for k in self.kam for customer in k.customers]
                query = "SELECT ROUND(AVG(ccbm), 2) AS ccbm, " \
                        "ROUND(AVG(ppb), 2) AS ppb, " \
                        "ROUND(AVG(risk), 2) AS risk " \
                        "FROM {results_db}.critters " \
                        "WHERE name in {customer_ids}" \
                    .format(
                        results_db=self.results_db,
                        customer_ids=str(tuple(customer_ids))
                    )

            self.cur.execute(query)
            selling_data = np.asarray(self.cur.fetchall())
            selling_data_cols = [desc[0] for desc in self.cur.description]
            selling_data_df = pd.DataFrame(
                selling_data,
                columns=selling_data_cols
            )
            selling_data_df = selling_data_df.astype(float)
            selling_data_df = selling_data_df.fillna(0)

            corss_selling = selling_data_df.to_dict('records')[0]

            return {
                'cross_selling': corss_selling
            }

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

    def as_json(self):
        return json.dumps(self.results)
