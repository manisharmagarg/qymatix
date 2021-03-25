import logging
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

logger = logging.getLogger('django.request')

env_path = Path('/var/www/qyapp') / '.env_core'
load_dotenv(dotenv_path=env_path, verbose=True)


class Databases:

    def __init__(self):
        self.connection = self.connect()

    @staticmethod
    def connect():
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            charset='latin1',
            use_unicode=True,
            use_pure=True
        )

        return connection

    def get_names(self, prefix='data_'):
        cursor = self.connection.cursor()

        command = 'show databases'

        cursor.execute(command)

        return [name[0] for name in cursor if prefix in name[0]]
