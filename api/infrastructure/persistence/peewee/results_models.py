from peewee import *

database = MySQLDatabase('results_qymatix_com', **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost', 'user': 'root', 'password': 'dev'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Critters(BaseModel):
    ccbm = TextField(null=True)
    margin = TextField(null=True)
    name = TextField(null=True)
    ppb = TextField(null=True)
    risk = TextField(null=True)
    row_names = TextField(null=True)
    sales = TextField(null=True)
    size = TextField(null=True)

    class Meta:
        table_name = 'critters'
        primary_key = False

