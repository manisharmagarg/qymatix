import sqlalchemy


class MySqlConncetion():

    def __init__(self, db_name):
        super().__init__()
        self.db_name = db_name
    
    def session(self):
        url = "mysql+mysqlconnector://root:dev@0.0.0.0:3306/{}".format(self.db_name)

        engine = sqlalchemy.create_engine(
                        url,
                        connect_args={'use_pure': True}
                    )

        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=engine)
        session = Session()

        return session
