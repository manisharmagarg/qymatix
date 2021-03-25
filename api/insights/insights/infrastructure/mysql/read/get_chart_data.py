"""
Query for get the cross-selling, Churn-Risk and Price-Intelligence
bubble graph data
"""
# pylint: disable=import-error
# pylint: disable=relative-beyond-top-level
import json
import traceback
import logging
import numpy as np
import pandas as pd
from ......infrastructure.mysql import connection

logger = logging.getLogger(__name__)


class CustomerChartData(object):
    """
    class responsible query for get the cross-selling, Churn-Risk and
    Price-Intelligence bubble graph data
    """

    def __init__(self, db_name):
        super(CustomerChartData, self).__init__()
        self.data_db = "data_{}".format(db_name)
        self.results_db = "results_{}".format(db_name)
        self.mysql_connection = connection.MySQLConnection(self.data_db)
        self.con = self.mysql_connection.connect()
        self.cur = self.con.cursor()
        self.results = self.read_chart_data()

    def read_chart_data(self):
        """
        Query to read customers chart data
        """
        try:
            graph_details = dict()
            query = "SELECT cr.sales , cr.margin, " \
                    "cr.risk, cr.ppb, cr.ccbm, " \
                    "c.name, c.id " \
                    "FROM {results_db}.critters AS cr " \
                    "LEFT JOIN {data_db}.customers as c on " \
                    "c.id = cr.name;".format(data_db=self.data_db,
                                             results_db=self.results_db)
            self.cur.execute(query)
            data = np.asarray(self.cur.fetchall())
            cols = [desc[0] for desc in self.cur.description]
            customer_details_df = pd.DataFrame(data, columns=cols)
            graph_details["customers_df"] = customer_details_df
            return graph_details
        except (NameError, TypeError, KeyError, ValueError) as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )
            return str(traceback.format_exc())

    def as_json(self):
        """
        return: customer data in json format
        """
        return json.dumps(self.results)
