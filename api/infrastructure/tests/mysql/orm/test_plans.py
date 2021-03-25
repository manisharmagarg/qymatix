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

    def test_plan_set_kam(self):

        kam = Kam("Peter")
#        action = Action("Title", kam)

        plan = Plan("Title", kam=kam)

        self.assertEqual(plan.name, 'Title')
        self.assertEqual(plan.kam, kam)

    def test_plan_set_action(self):

        kam = Kam("Peter")
        action = Action("Title", kam)
        action2 = Action("Title 2", kam)

        plan = Plan("Title", kam=kam, action=[action])

        plan.action.append(action2)

        self.assertEqual(plan.name, 'Title')
        self.assertEqual(plan.kam, kam)
        self.assertEqual(plan.action, [action, action2])
