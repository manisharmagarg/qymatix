from os import getenv
from pathlib import Path

import sqlalchemy
from dotenv import load_dotenv


# env_path = Path('/var/www/importer') / '.env_core'
# env_path = Path('../../../../../.env_core')
env_path = Path('.env_core')
load_dotenv(dotenv_path=env_path, verbose=True)
load_dotenv()


class MySqlConnection:

    def __init__(self, db_name):
        super().__init__()
        self.db_name = db_name

        self.username = getenv("MYSQL_USER")
        self.password = getenv("MYSQL_PASSWORD")
        self.host = getenv("MYSQL_HOST")
        self.port = getenv("MYSQL_PORT")

    def session(self):
        url = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(
            self.username,
            self.password,
            self.host,
            self.port,
            self.db_name
        )

        engine = sqlalchemy.create_engine(
            url,
            connect_args={'use_pure': True}
        )

        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=engine, autoflush=False, expire_on_commit=False)
        session = Session()

        return session
