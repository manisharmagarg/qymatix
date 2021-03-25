import os

from dotenv import load_dotenv
from peewee import MySQLDatabase

env_path = Path('/var/www/qyapp') / '.env_core'
load_dotenv(dotenv_path=env_path, verbose=True)


class Database:

    def __init__(self, database_name):
        self.database_name = database_name

    def database(self):
        database = MySQLDatabase(
            self.database_name,
            **{
                'charset': 'utf8',
                'use_unicode': True,
                'host': os.getenv("MYSQL_HOST"),
                'user': os.getenv("MYSQL_USER"),
                'password': os.getenv("MYSQL_ROOT_PASSWORD")
            }
        )

        return database
