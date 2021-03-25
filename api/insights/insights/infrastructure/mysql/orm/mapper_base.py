import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base


class MapperBase():
    user = os.getenv("MYSQL_USER")
    key = os.getenv("MYSQL_KEY")
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT")

    def __init__(self, database):
        self.db = database
        if database == 'test':
            self.url = 'sqlite:///:memory:'
        else:
            self.url = \
                'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
                    self.user,
                    self.key,
                    self.host,
                    self.port,
                    self.db,
                )

        self.engine = create_engine(
            self.url,
            connect_args={'use_pure': True}
        )
        self.session = sessionmaker(bind=self.engine)
        self.base = Base

    def get_base(self):
        return self.base

    def get_engine(self):
        return self.engine

    def get_session(self):
        return self.session()
