import json
import datetime

from api.infrastructure.mysql import connection
from api.qymatix.analytics.performance_analytics import kam
from api.qymatix import insights

import numpy as np
import pandas as pd
import traceback
import logging

logger = logging.getLogger(__name__)


class CustomerSuggestions:

    def __init__(self, database_name, customer_id):
        super().__init__()
        self.database_name = database_name

        self.data_db = "data_{}".format(database_name)
        self.results_db = "results_{}".format(database_name)

        self.mysql_connection = connection.MySQLConnection(self.data_db)
        self.con = self.mysql_connection.connect()
        self.cur = self.con.cursor()
        self.customer_id = customer_id
        self.results = self.read_customer_suggestions()

    def read_customer_suggestions(self):
    	username = 'admin'
    	
    	actions_per_account = kam.actionsPerAccount(self.cur, username=username)
    	actions_YTD = kam.actionsYTD(self.cur, username=username)
    	active_accounts = kam.activeAccounts(self.cur, username=username)
    	try:
    		actions_active_accounts_ratio = round(float(actions_YTD) / len(active_accounts.keys()), 2)
    	except:
    		actions_active_accounts_ratio = 0.0
    	insight = insights.get_insights(
    		self.database_name, 
    		account=self.customer_id, 
    		raw=False, local=False, 
    		dbusername='', passwd='', username='', user=''
    	)

    	
    	return {
    		"actions_per_account": actions_per_account,
    		"actions_active_accounts_ratio": actions_active_accounts_ratio,
    		"insights": insight
    	}

    def as_json(self):
        return json.dumps(self.results)

