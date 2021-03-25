import unittest
from src.core.views.orm.base import Base
from src.core.views.orm.plan import Plan
from src.core.views.orm.action import Action
from src.core.views.orm.kam import Kam
#from src.core.views.orm.plan import Plan
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class TestAction(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_action(self):

        kam = Kam("Peter")

        action = Action("Title", kam)

        self.assertEqual(kam.name, 'Peter')
        self.assertEqual(action.name, 'Title')
        self.assertEqual(action.kam, kam)

