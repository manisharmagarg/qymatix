# pylint: skip-file

import datetime
import json
import logging
import traceback

import numpy as np

from api.infrastructure.mysql import connection

logger = logging.getLogger(__name__)


class ChurnRiskHistory:

    def __init__(self, database_name, kam=None):
        super().__init__()

        self.results_db = "results_{}".format(database_name)
        self.data_db = "data_{}".format(database_name)

        self.mysql_connection = connection.MySQLConnection(self.results_db)
        self.con = self.mysql_connection.connect()
        self.cur = self.con.cursor()

        self.kam = kam
        self.results = self.read_history()

    def read_history(self):

        today = datetime.datetime.now()
        try:
            if self.kam is None:
                query = "SELECT ROUND(cr.risk, 2) as risk FROM {results_db}.critters AS cr " \
                        "LEFT JOIN {data_db}.customers AS c ON cr.name=c.id".format(
                            results_db=self.results_db,
                            data_db=self.data_db
                        )

            elif isinstance(self.kam, list):
                customer_ids = [customer.id for k in self.kam for customer in k.customers]

                query = "SELECT ROUND(cr.risk, 2) as risk FROM {results_db}.critters AS cr " \
                        "LEFT JOIN {data_db}.customers AS c ON cr.name=c.id " \
                        "WHERE c.id IN {customer_ids}" \
                    .format(
                        results_db=self.results_db,
                        data_db=self.data_db,
                        customer_ids=str(tuple(customer_ids))
                    )

            self.cur.execute(query)
            risk_data = np.asarray(self.cur.fetchall())
            risk_data_cols = [desc[0] for desc in self.cur.description]
            results = dict()

            for i in range(len(risk_data_cols)):
                values = np.ravel(risk_data[:, i])
                c = risk_data_cols[i]
                if c == 'risk':
                    results['rawRisk'] = values.tolist()

                values[values == -np.inf] = 0
                results[c] = values.tolist()

            return {
                'churn_risk': results,
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
