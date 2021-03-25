from peewee import *

# database = MySQLDatabase('data_test',
#                          **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost', 'user': 'root',
#                             'password': 'dev'})

database = MySQLDatabase(None)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Users(BaseModel):
    active = IntegerField()
    country = TextField()
    created = DateTimeField()
    description = TextField()
    email = TextField()
    name = CharField(unique=True)
    phone = TextField()
    username = TextField()

    class Meta:
        table_name = 'users'


class Groups(BaseModel):
    created = DateTimeField()
    description = TextField()
    name = CharField(unique=True)
    owner = ForeignKeyField(column_name='owner_id', field='id', model=Users)

    class Meta:
        table_name = 'groups'


class Plans(BaseModel):
    account = TextField()
    action = TextField()
    calls = DecimalField()
    chances = FloatField()
    created = DateTimeField()
    description = TextField()
    due = DateTimeField()
    goal = FloatField()
    group = ForeignKeyField(column_name='group_id', field='id', model=Groups)
    hot = IntegerField()
    name = CharField()
    offers = DecimalField()
    owner = ForeignKeyField(column_name='owner_id', field='id', model=Users)
    status = TextField()
    visits = DecimalField()

    class Meta:
        table_name = 'plans'


class Tasks(BaseModel):
    account = TextField()
    action = TextField()
    allday = IntegerField()
    contact_id = IntegerField()
    created = DateTimeField()
    description = TextField()
    due = DateTimeField()
    end = DateTimeField()
    group = ForeignKeyField(column_name='group_id', field='id', model=Groups)
    owner = ForeignKeyField(column_name='owner_id', field='id', model=Users)
    plan = TextField()
    status = TextField()
    title = TextField()

    class Meta:
        table_name = 'tasks'


class PlansActions(BaseModel):
    plan = ForeignKeyField(column_name='plan_id', field='id', model=Plans)
    task = ForeignKeyField(column_name='task_id', field='id', model=Tasks)

    class Meta:
        table_name = 'Plans_Actions'
        indexes = (
            (('plan', 'task'), True),
        )
        primary_key = CompositeKey('plan', 'task')


class UsersActions(BaseModel):
    task = ForeignKeyField(column_name='task_id', field='id', model=Tasks)
    user = ForeignKeyField(column_name='user_id', field='id', model=Users)

    class Meta:
        table_name = 'Users_Actions'
        indexes = (
            (('user', 'task'), True),
        )
        primary_key = CompositeKey('task', 'user')


class Customers(BaseModel):
    address = CharField()
    city = CharField()
    classification = CharField()
    comment = TextField()
    country = CharField()
    employees = IntegerField()
    favorite = IntegerField()
    industry = CharField()
    name = CharField(unique=True)
    postcode = CharField()
    revenue = FloatField()
    website = CharField()
    telephone = CharField()

    # def __init__(self, db_path):
    #     database.init(db_path, **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost', 'user': 'root', 'password': 'dev'})

    class Meta:
        table_name = 'customers'


class UsersCustomers(BaseModel):
    customer = ForeignKeyField(column_name='customer_id', field='id', model=Customers)
    user = ForeignKeyField(column_name='user_id', field='id', model=Users)

    class Meta:
        table_name = 'Users_Customers'
        indexes = (
            (('user', 'customer'), True),
        )
        primary_key = CompositeKey('customer', 'user')


class UsersGroups(BaseModel):
    group = ForeignKeyField(column_name='group_id', field='id', model=Groups)
    user = ForeignKeyField(column_name='user_id', field='id', model=Users)

    class Meta:
        table_name = 'Users_Groups'
        indexes = (
            (('user', 'group'), True),
        )
        primary_key = CompositeKey('group', 'user')


class UsersPlans(BaseModel):
    plan = ForeignKeyField(column_name='plan_id', field='id', model=Plans)
    user = ForeignKeyField(column_name='user_id', field='id', model=Users)

    class Meta:
        table_name = 'Users_Plans'
        indexes = (
            (('user', 'plan'), True),
        )
        primary_key = CompositeKey('plan', 'user')


class Contacts(BaseModel):
    created = DateTimeField()
    customer = ForeignKeyField(column_name='customer_id', field='id', model=Customers)
    description = TextField()
    email = TextField()
    function = TextField()
    linkedin = TextField()
    name = CharField(unique=True)
    phone = TextField()
    title = TextField()
    xing = TextField()

    class Meta:
        table_name = 'contacts'


class Goals(BaseModel):
    april = FloatField()
    august = FloatField()
    country = TextField()
    created = DateTimeField()
    december = FloatField()
    description = TextField()
    february = FloatField()
    january = FloatField()
    july = FloatField()
    june = FloatField()
    march = FloatField()
    may = FloatField()
    name = CharField()
    november = FloatField()
    october = FloatField()
    september = FloatField()
    user = ForeignKeyField(column_name='user_id', field='id', model=Users)
    year = IntegerField()

    class Meta:
        table_name = 'goals'


class ProductClass(BaseModel):
    active = IntegerField()
    created = DateTimeField()
    description = TextField()
    name = CharField(unique=True)
    number = CharField()

    class Meta:
        table_name = 'product_class'


class ProductLine(BaseModel):
    active = IntegerField()
    created = DateTimeField()
    description = TextField()
    name = CharField(unique=True)
    number = CharField()
    product_class = ForeignKeyField(column_name='product_class_id', field='id', model=ProductClass)

    class Meta:
        table_name = 'product_line'


class ProductType(BaseModel):
    active = IntegerField()
    created = DateTimeField()
    description = TextField()
    name = CharField(unique=True)
    number = CharField()
    product_line = ForeignKeyField(column_name='product_line_id', field='id', model=ProductLine)

    class Meta:
        table_name = 'product_type'


class Products(BaseModel):
    active = IntegerField()
    created = DateTimeField()
    description = TextField()
    name = CharField(unique=True)
    number = CharField()
    product_type = ForeignKeyField(column_name='product_type_id', field='id', model=ProductType)
    serial = CharField()

    class Meta:
        table_name = 'products'


class Sales(BaseModel):
    cost = FloatField()
    customer = ForeignKeyField(column_name='customer_id', field='id', model=Customers)
    date = DateTimeField()
    invoice = CharField()
    kam = CharField()
    margin = FloatField()
    month = DecimalField()
    price = FloatField()
    product = ForeignKeyField(column_name='product_id', field='id', model=Products)
    quantity = IntegerField()
    year = DecimalField()

    class Meta:
        table_name = 'sales'
