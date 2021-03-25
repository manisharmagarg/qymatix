import unittest
from src.core.views.orm.base import Base
from src.core.views.orm.user import User
from src.core.views.orm.address import Address
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class TestUserMapper(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_user(self):
        user = User("Pedro", "Pedro Picapiedra", "Peter")

        address_main = Address("J. B. Justo", "10", user)
        address_secondary = Address("J. B. Justo", "10", user)
        addresses = [address_main, address_secondary]

        user.addresses = addresses

        self.assertEqual(user.name, 'Pedro')
        self.assertEqual(user.fullname, 'Pedro Picapiedra')
        self.assertEqual(user.nickname, 'Peter')
        self.assertEqual(user.addresses, addresses)
