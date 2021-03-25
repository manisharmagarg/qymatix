# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, Float, ForeignKey, String, Table, Text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TINYINT
from sqlalchemy.orm import relationship

from api.infrastructure.mysql.orm.base import Base

metadata = Base.metadata


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    postcode = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    revenue = Column(Float, nullable=False)
    employees = Column(INTEGER(11), nullable=False)
    industry = Column(String(255), nullable=False)
    classification = Column(String(255), nullable=False)
    website = Column(Text, nullable=False)
    comment = Column(LONGTEXT, nullable=False)
    favorite = Column(TINYINT(1), nullable=False)
    telephone = Column(Text, nullable=False)
    customer_parent_id = Column(Text, nullable=False)
    customer_number = Column(Text, nullable=False)

    users = relationship('User', secondary='Users_Customers')


class ProductClas(Base):
    __tablename__ = 'product_class'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(LONGTEXT, nullable=False)
    active = Column(TINYINT(1), nullable=False)
    created = Column(DateTime, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(LONGTEXT, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(LONGTEXT, nullable=False)
    created = Column(DateTime, nullable=False)
    country = Column(LONGTEXT, nullable=False)
    phone = Column(LONGTEXT, nullable=False)
    email = Column(LONGTEXT, nullable=False)
    active = Column(TINYINT(1), nullable=False)


t_Users_Customers = Table(
    'Users_Customers', metadata,
    Column('user_id', ForeignKey('users.id', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('customer_id', ForeignKey('customers.id', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    title = Column(LONGTEXT, nullable=False)
    description = Column(LONGTEXT, nullable=False)
    customer_id = Column(ForeignKey('customers.id'), nullable=False, index=True)
    function = Column(LONGTEXT, nullable=False)
    phone = Column(LONGTEXT, nullable=False)
    email = Column(LONGTEXT, nullable=False)
    linkedin = Column(LONGTEXT, nullable=False)
    xing = Column(LONGTEXT, nullable=False)
    created = Column(DateTime, nullable=False)

    customer = relationship('Customer')


class Goal(Base):
    __tablename__ = 'goals'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False)
    description = Column(LONGTEXT, nullable=False)
    country = Column(LONGTEXT, nullable=False)
    year = Column(INTEGER(11), nullable=False)
    january = Column(Float, nullable=False)
    february = Column(Float, nullable=False)
    march = Column(Float, nullable=False)
    april = Column(Float, nullable=False)
    may = Column(Float, nullable=False)
    june = Column(Float, nullable=False)
    july = Column(Float, nullable=False)
    august = Column(Float, nullable=False)
    september = Column(Float, nullable=False)
    october = Column(Float, nullable=False)
    november = Column(Float, nullable=False)
    december = Column(Float, nullable=False)

    user = relationship('User')


class Group(Base):
    __tablename__ = 'groups'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(LONGTEXT, nullable=False)
    owner_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False)

    owner = relationship('User')
    users = relationship('User', secondary='Users_Groups')


class ProductLine(Base):
    __tablename__ = 'product_line'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    product_class_id = Column(ForeignKey('product_class.id'), nullable=False, index=True)
    description = Column(LONGTEXT, nullable=False)
    active = Column(TINYINT(1), nullable=False)
    created = Column(DateTime, nullable=False)
    number = Column(String(255), nullable=False)

    product_class = relationship('ProductClas')


t_Users_Groups = Table(
    'Users_Groups', metadata,
    Column('user_id', ForeignKey('users.id', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('group_id', ForeignKey('groups.id', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class Plan(Base):
    __tablename__ = 'plans'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(LONGTEXT, nullable=False)
    owner_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    group_id = Column(ForeignKey('groups.id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False)
    due = Column(DateTime, nullable=False)
    account = Column(LONGTEXT, nullable=False)
    goal = Column(Float, nullable=False)
    chances = Column(Float, nullable=False)
    status = Column(LONGTEXT, nullable=False)
    action = Column(LONGTEXT, nullable=False)
    calls = Column(DECIMAL(10, 5), nullable=False)
    visits = Column(DECIMAL(10, 5), nullable=False)
    offers = Column(DECIMAL(10, 5), nullable=False)
    hot = Column(TINYINT(1), nullable=False)

    group = relationship('Group')
    owner = relationship('User')
    tasks = relationship('Task', secondary='Plans_Actions')
    users = relationship('User', secondary='Users_Plans')


class ProductType(Base):
    __tablename__ = 'product_type'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    product_line_id = Column(ForeignKey('product_line.id'), nullable=False, index=True)
    description = Column(LONGTEXT, nullable=False)
    active = Column(TINYINT(1), nullable=False)
    created = Column(DateTime, nullable=False)
    number = Column(String(255), nullable=False)

    product_line = relationship('ProductLine')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(INTEGER(11), primary_key=True)
    group_id = Column(ForeignKey('groups.id'), nullable=False, index=True)
    owner_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    plan = Column(LONGTEXT, nullable=False)
    account = Column(LONGTEXT, nullable=False)
    title = Column(LONGTEXT, nullable=False)
    description = Column(LONGTEXT, nullable=False)
    action = Column(LONGTEXT, nullable=False)
    created = Column(DateTime, nullable=False)
    due = Column(DateTime, nullable=False)
    status = Column(LONGTEXT, nullable=False)
    end = Column(DateTime, nullable=False)
    allday = Column(TINYINT(1), nullable=False)
    contact_id = Column(INTEGER(11), nullable=False)

    group = relationship('Group')
    owner = relationship('User')
    users = relationship('User', secondary='Users_Actions')


t_Plans_Actions = Table(
    'Plans_Actions', metadata,
    Column('plan_id', ForeignKey('plans.id', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('task_id', ForeignKey('tasks.id', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_Users_Actions = Table(
    'Users_Actions', metadata,
    Column('user_id', ForeignKey('users.id', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('task_id', ForeignKey('tasks.id', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_Users_Plans = Table(
    'Users_Plans', metadata,
    Column('user_id', ForeignKey('users.id', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('plan_id', ForeignKey('plans.id', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class Product(Base):
    __tablename__ = 'products'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    product_type_id = Column(ForeignKey('product_type.id'), nullable=False, index=True)
    description = Column(LONGTEXT, nullable=False)
    active = Column(TINYINT(1), nullable=False)
    created = Column(DateTime, nullable=False)
    number = Column(String(255), nullable=False)
    serial = Column(String(255), nullable=False)

    product_type = relationship('ProductType')


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(INTEGER(11), primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False, index=True)
    product_id = Column(ForeignKey('products.id'), nullable=False, index=True)
    quantity = Column(INTEGER(11), nullable=False)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    margin = Column(Float, nullable=False)
    year = Column(DECIMAL(10, 5), nullable=False)
    month = Column(DECIMAL(10, 5), nullable=False)
    date = Column(DateTime, nullable=False)
    invoice = Column(String(255), nullable=False)
    kam = Column(String(255), nullable=False)

    customer = relationship('Customer')
    product = relationship('Product')
