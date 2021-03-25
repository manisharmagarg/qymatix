import json

from api.insights.insights.infrastructure.mysql.mysql_connection \
    import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities \
    import Customer


class AccountsListData:

    def __init__(self, database_name, kam=None):
        super().__init__()
        self.kam = kam
        self.data_db = 'data_{}'.format(database_name)

        connection = MySqlConnection(self.data_db)
        self.session = connection.session()

        self.results = self.read_accounts()

    def read_accounts(self):

        if isinstance(self.kam, list):
            customer_ids = [customer.id for k in self.kam for customer in k.customers]
            customers_result = self.session.query(
                Customer
            ) \
                .filter(Customer.id.in_(customer_ids)) \
                .all()
        else:
            customers_result = self.session.query(
                Customer
            ) \
                .all()

        return customers_result

    def as_json(self):
        response = dict()
        for customer in self.results:
            customer_as_dict = customer.__dict__
            for user in customer.users:
                customer_as_dict['kam'] = user.name
            customer_as_dict.pop('_sa_instance_state')
            customer_as_dict.pop('users')
            response[customer.id] = customer_as_dict
        return json.dumps(response)
