from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

import logging

logger = logging.getLogger(__name__)


class Database:

    user = os.getenv("MYSQL_USER")
    key = os.getenv("MYSQL_KEY")
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT")

    print(host)

    url = 'mysql+mysqlconnector://{}:{}@{}:{}/'.format(user, key, host, port)
    logger.error(url)

    def __init__(self, name):
        self.name = name
        logger.info(self.url)
        engine = create_engine(self.url, connect_args={'use_pure': True})
        self.conn = engine.connect()
        self.conn.execute("commit")

    def create(self):
        self.conn.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.name))

    def drop(self):
        self.conn.execute("DROP DATABASE {}".format(self.name))

    def close(self):
        self.conn.close()
