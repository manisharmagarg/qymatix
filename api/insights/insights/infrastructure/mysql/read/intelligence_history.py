import json
import logging
import traceback

import numpy as np

from api.infrastructure.mysql import connection

logger = logging.getLogger(__name__)


class PriceIntelligenceHistory:

    def __init__(self, database_name, kam=None):
        super().__init__()

        self.results_db = "results_{}".format(database_name)
        self.data_db = "data_{}".format(database_name)

        self.kam = kam

        mysql_connection = connection.MySQLConnection(self.results_db)
        con = mysql_connection.connect()
        self.cur = con.cursor()

        self.results = self.read_history()

    def read_history(self):

        try:
            if self.kam is None:
                script = \
                    "SELECT cr.ppb as ppb FROM {results_db}.critters AS cr " \
                    "LEFT JOIN {data_db}.customers AS c " \
                    "ON cr.name=c.id".format(
                        results_db=self.results_db,
                        data_db=self.data_db
                    )
            elif isinstance(self.kam, list):
                customer_ids = [customer.id for k in self.kam for customer in k.customers]
                script = \
                    "SELECT cr.ppb as ppb FROM {results_db}.critters AS cr " \
                    "LEFT JOIN {data_db}.customers AS c " \
                    "ON cr.name=c.id " \
                    "WHERE c.id IN {customer_ids}" \
                    .format(
                        results_db=self.results_db,
                        data_db=self.data_db,
                        customer_ids=str(tuple(customer_ids))
                    )

            self.cur.execute(script)
            intelligence_data = np.asarray(self.cur.fetchall())
            intelligence_cols = [desc[0] for desc in self.cur.description]
            results = dict()

            for i, cols in enumerate(intelligence_cols):
                values = np.ravel(intelligence_data[:, i])
                if cols == 'ppb':
                    results['ppb'] = values.tolist()

                values[values == -np.inf] = 0
                results[cols] = values.tolist()

            return {
                'price_intelligence': results,
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
