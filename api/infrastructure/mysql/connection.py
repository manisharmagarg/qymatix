import logging
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

logger = logging.getLogger('django.request')

env_path = Path('/var/www/qyapp') / '.env_core'
load_dotenv(dotenv_path=env_path, verbose=True)


class MySQLConnection:

    def __init__(self, database=""):
        self.database = database

    def connect(self):

        try:

            con = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=self.database,
                charset='latin1',
                use_unicode=True,
                use_pure=True
            )

            return con

        except Exception as e:

            logger.error("{}".format(e), extra={'type': 'MySQL connection'})

            return e
