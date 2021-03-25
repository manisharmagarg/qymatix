import json
import logging
from datetime import datetime
from api.infrastructure.mysql.orm import database
from api.infrastructure.mysql.orm.autogen_entities import *
from api.infrastructure.mysql.orm.mapper_base import MapperBase
from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities import User
from tokenapi.views import token_
from ..models import Activity
from ..models import Configuration
from ..models import Contact
from django.contrib.auth.models import Group

logger = logging.getLogger('django.request')


class ConfigUser:
    user_id = None

    def __init__(self, user):
        self.user = user

        self.group_name = self.user.email.split("@")[1]
        self.group_name = self.group_name.replace('.', '_').replace("-", "___")

        self.database_name = None

        try:
            self.configuration = Configuration.objects.get(
                user_id=self.user.id)
        except Exception as e:
            self.configuration = Configuration.objects.create(
                user_id=self.user.id)
            self.configuration.save()

        try:
            self.activity = Activity.objects.get(user_id=self.user.id)
        except Exception as e:
            self.activity = Activity.objects.create(user_id=self.user.id)
            self.activity.save()

        try:
            self.contact = Contact.objects.get(user_id=self.user.id)
        except Exception as e:
            self.contact = Contact.objects.create(user_id=self.user.id)
            self.contact.save()

    def setup_user(self, plan='crm', account_type='admin'):

        logger.info("Setting up user: {}".format(self.user.username))

        self.create_databases()
        self.create_tables()

        # self.generate_token(password)

        self.user_plan_and_account(plan=plan, account_type=account_type)
        self.create_group()

        self.add_user()

    def create_tables(self):
        mapper_base = MapperBase('data_' + self.group_name)
        base = mapper_base.get_base()
        base.metadata.create_all(mapper_base.get_engine())

    def user_plan_and_account(self, plan='crm', account_type='admin'):
        self.configuration.plan = plan
        self.configuration.account_type = account_type
        self.configuration.save()

    def create_databases(self, name=None):
        if name is None:
            name = self.group_name
        for prefix in ['data_', 'results_']:
            fullname = prefix + name
            db = database.Database(fullname)
            try:
                db.create()
                logger.info("Database {} created".format(fullname))
            except Exception as e:
                print(e)
                logger.error("Error while creating DB {}".format(
                    fullname), extra={'dict': e})

        db.close()

    def generate_token(self, password):
        token = token_(self.user.username, password)
        token = token.content
        token = json.loads(token)

        self.configuration.token = token['token']
        self.configuration.save()

    def get_token(self):
        return self.configuration.token

    def create_group(self):

        try:
            industry_list = [
                'agriculture',
                'banking',
                'construction',
                'consulting',
                'education',
                'government',
                'industry_cl',
                'manufacturing',
                'medical',
                'retail',
                'services',
                'software',
                'transport',
                'other',
            ]

            seperator = ', '
            ins_lst = seperator.join("'{0}'".format(w) for w in industry_list)
            usergroup, created = Group.objects.get_or_create(
                name=self.group_name, industries_name=ins_lst)
            usergroup.user_set.add(self.user)
        except Exception as e:
            logger.error("Could not create group for user {}".format(
                self.user.username), extra={'Exception': e})

    def add_user(self):

        database_name = 'data_' + self.group_name
        connection = MySqlConnection(database_name)
        session = connection.session()

        result = session.query(User) \
            .filter_by(username=self.user.username) \
            .first()

        if result is not None:
            return

        new_user = User(
            name=self.user.first_name + " " + self.user.last_name,
            username=self.user.username,
            description='',
            created=datetime.now(),
            email=self.user.email,
            active=1,
            country='',
            phone=''
        )

        session.add(new_user)
        session.commit()

        return
