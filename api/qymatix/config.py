import datetime
import logging
import os
import sys

import numpy as np
import peewee as pw
from django.conf import settings

from api.qymatix import addtables
from api.infrastructure.mysql import connection


logger = logging.getLogger(__name__)

def createDatabase(dbname="dbname", host="remote", user="webadmin", passwd="passwd", local=False):
    '''
    '''
    try:
        dbname = None
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cursor = con.cursor()

        sql = 'CREATE DATABASE IF NOT EXISTS {}'.format(dbname)
        cursor.execute(sql)

    except Exception as e:
        print(e)
        raise

    con.close()


def dropDatabase(dbname="username", user="webadmin", passwd="passwd", which="all", local=False):
    '''
    '''

    dbname = None
    mysql_connection = connection.MySQLConnection(dbname)
    con = mysql_connection.connect()
    cursor = con.cursor()

    sys.stdout.write("\r")
    sys.stdout.write("{}".format(dbname))
    sys.stdout.flush()

    try:
        script = "set foreign_key_checks = 0;".format(dbname)
        cursor.execute(script)
        con.commit()

        sql = 'DROP DATABASE {}; FLUSH;'.format(dbname)
        cursor.execute(sql)
        con.commit()

        script = "set foreign_key_checks = 1;".format(dbname)
        cursor.execute(script)
        con.commit()

        print("\n{} ...deleted".format(dbname))
    except Exception as e:
        print("\n")
        print(e[1])
        # raise

    con.close()


def clear_table(dbname, local=False):
    '''
    '''
    dbname = None
    mysql_connection = connection.MySQLConnection(dbname)
    con = mysql_connection.connect()
    cursor = con.cursor()

    try:
        sql = 'TRUNCATE TABLE {}'.format(dbname)
        cursor.execute(sql)
        print("\n{} ...cleared".format(dbname))
    except Exception as e:
        print("\n")
        print(e[1])

    con.close()


def createTasksTable(dbname, local=False):
    '''
    '''
    dbname = None
    mysql_connection = connection.MySQLConnection(dbname)
    con = mysql_connection.connect()
    cursor = con.cursor()

    try:
        script = "\
			CREATE TABLE `tasks` (\
			  `id` int(11) NOT NULL AUTO_INCREMENT,\
			  `group_id` int(11) NOT NULL,\
			  `owner_id` int(11) NOT NULL,\
			  `plan` longtext NOT NULL,\
			  `account` longtext NOT NULL,\
			  `title` longtext NOT NULL,\
			  `description` longtext NOT NULL,\
			  `action` longtext NOT NULL,\
			  `created` datetime NOT NULL,\
			  `due` datetime NOT NULL,\
			  `status` longtext NOT NULL,\
			  `end` datetime NOT NULL,\
			  `allday` tinyint(1) NOT NULL,\
			  PRIMARY KEY (`id`),\
			  KEY `data_group_id` (`group_id`),\
			  KEY `data_owner_id` (`owner_id`),\
			  CONSTRAINT `data_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`),\
			  CONSTRAINT `data_ibfk_2` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)\
			) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1\
        "
        cursor.execute(script)
        print("\n{} ...cleared".format(dbname))
    except Exception as e:
        print("\n")
        print(e[1])

    con.close()


def checkDatabaseExists(dbname="dbname", host="localhost", user="sdsdsds", passwd="dfdfdfd"):
    '''
    '''
    mysql_connection = connection.MySQLConnection()
    con = mysql_connection.connect()
    cursor = con.cursor()

    # sql = 'use {}'.format('data_{}_{}'.format(userID, userName))
    sql = 'use {}'.format(dbname)
    try:
        cursor.execute(sql)
    except:
        con.close()
        return False

    con.close()
    return True


def createCustomersTable(dbname='data_userID_username', db=None, lines=None, local=False):
    '''
    '''
    mysql_connection = connection.MySQLConnection()
    con = mysql_connection.connect()
    cursor = con.cursor()

    if 'data_' not in dbname:
        sql = 'use data_{}'.format(dbname)
    cursor.execute(sql)

    try:
        script = "\
				 CREATE TABLE `customers` (\
				  `id` int(11) NOT NULL AUTO_INCREMENT,\
				  `name` varchar(255) NOT NULL,\
				  `address` varchar(255) NOT NULL,\
				  `postcode` varchar(255) NOT NULL,\
				  `city` varchar(255) NOT NULL,\
				  `country` varchar(255) NOT NULL,\
				  `revenue` double NOT NULL,\
				  `employees` int(11) NOT NULL,\
				  `industry` varchar(255) NOT NULL,\
				  `classification` varchar(255) NOT NULL,\
				  `website` text NOT NULL,\
				  `comment` longtext NOT NULL,\
				  `favorite` tinyint(1) NOT NULL,\
				  PRIMARY KEY (`id`)\
				) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1\
				"
        # PRIMARY KEY (`id`),\
        # UNIQUE KEY `customers_name` (`name`)\
        cursor.execute(script)
        print("\nData tables for {} created.".format(dbname))
    except Exception as e:
        print("\n")
        print(e[1])

    con.close()


def createContactsTable(dbname='data_userID_username', db=None, lines=None, local=False):
    '''
    '''
    mysql_connection = connection.MySQLConnection(dbname)
    con = mysql_connection.connect()
    cursor = con.cursor()

    if 'data_' not in dbname:
        sql = 'use data_{}'.format(dbname)
    cursor.execute(sql)

    try:
        script = "\
				 CREATE TABLE `contacts` (\
				  `id` int(11) NOT NULL AUTO_INCREMENT,\
				  `name` varchar(255) NOT NULL,\
				  `title` longtext NOT NULL,\
				  `description` longtext NOT NULL,\
				  `customer_id` int(11) NOT NULL,\
				  `function` longtext NOT NULL,\
				  `phone` longtext NOT NULL,\
				  `email` longtext NOT NULL,\
				  `linkedin` longtext NOT NULL,\
				  `xing` longtext NOT NULL,\
				  `created` datetime NOT NULL,\
				  PRIMARY KEY (`id`),\
				  UNIQUE KEY `contacts_name` (`name`),\
				  KEY `contacts_customer_id` (`customer_id`),\
				  CONSTRAINT `contacts_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)\
				) ENGINE=InnoDB DEFAULT CHARSET=latin1\
				"
        cursor.execute(script)
        print("\nCustomers table for {} created.".format(dbname))
    except Exception as e:
        print("\n")
        print(e[1])

    con.close()


def createSalesTable(dbname='data_userID_username', db=None, lines=None, local=False):
    '''
    '''
    mysql_connection = connection.MySQLConnection(dbname)
    con = mysql_connection.connect()
    cursor = con.cursor()

    if 'data_' not in dbname:
        sql = 'use data_{}'.format(dbname)
    cursor.execute(sql)

    try:
        script = "\
				CREATE TABLE `sales` (\
				  `id` int(11) NOT NULL AUTO_INCREMENT,\
				  `customer_id` int(11) NOT NULL,\
				  `product_id` int(11) NOT NULL,\
				  `quantity` int(11) NOT NULL,\
				  `price` double NOT NULL,\
				  `cost` double NOT NULL,\
				  `margin` double NOT NULL,\
				  `year` decimal(10,5) NOT NULL,\
				  `month` decimal(10,5) NOT NULL,\
				  `date` datetime NOT NULL,\
				  `invoice` varchar(255) NOT NULL,\
				  `kam` varchar(255) NOT NULL,\
				  PRIMARY KEY (`id`),\
				  KEY `sales_customer_id` (`customer_id`),\
				  KEY `sales_product_id` (`product_id`),\
				  CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),\
				  CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)\
				) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1\
				"
        cursor.execute(script)
        print("\nCustomers table for {} created.".format(dbname))
    except Exception as e:
        print("\n")
        print(e[1])

    con.close()


def createDataTables(dbname='data_userID_username', db=None, lines=None, local=False):
    '''
    '''
    createCustomersTable(dbname, local=False)
    createContactsTable(dbname, local=False)
    createSalesTable(dbname, local=False)


def createDataTables_(dbname='data_userID_username', db=None, lines=None, local=False):
    '''
    '''

    host = os.getenv("MYSQL_HOST")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    db = pw.MySQLDatabase(dbname, host=host, user=user, passwd=password)

    # db = pw.MySQLDatabase(db_name, host='localhost', user='martin', passwd='martin')

    class Customers(pw.Model):
        name = pw.CharField(unique=True)
        address = pw.CharField(default='null')
        postcode = pw.CharField(default='null')
        city = pw.CharField(default='null')
        country = pw.CharField(default='null')
        revenue = pw.DoubleField(default='null')
        employees = pw.IntegerField(default='null')
        industry = pw.CharField(default='null')
        classification = pw.CharField(default='null')
        website = pw.CharField(default='null')
        comment = pw.TextField(default='null')
        favorite = pw.BooleanField(default='null')

        # created = pw.DateTimeField()

        class Meta:
            database = db

    class Products(pw.Model):
        # name = pw.ForeignKeyField(Customers, related_name='prods')
        name = pw.CharField(unique=True)

        # price = pw.DecimalField()
        # cost = pw.DecimalField()

        class Meta:
            database = db

    class Sales(pw.Model):
        customer = pw.ForeignKeyField(Customers, related_name='cust_sales')
        product = pw.ForeignKeyField(Products, related_name='prod_sales')
        quantity = pw.IntegerField()
        price = pw.DoubleField()
        cost = pw.DoubleField()
        margin = pw.DoubleField()
        year = pw.DecimalField()
        month = pw.DecimalField()
        date = pw.DateTimeField()
        kam = pw.CharField(default='null')

        class Meta:
            database = db

    class Contacts(pw.Model):
        name = pw.CharField(unique=True)
        title = pw.TextField()
        description = pw.TextField()
        customer = pw.ForeignKeyField(Customers, related_name='cust_contacts')
        function = pw.TextField()
        phone = pw.TextField()
        email = pw.TextField()
        linkedin = pw.TextField()
        xing = pw.TextField()
        created = pw.DateTimeField()

        class Meta:
            database = db

    try:
        db.create_tables([Customers, Sales, Products, Contacts])
    except Exception as e:
        print(e)
        # pass
        raise


def addTasksTables(dbname, db=None, local=False):
    '''
    '''
    try:
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")

        if db == None:
            db = pw.MySQLDatabase(dbname, host=host, user=user, passwd=password)

        class Users(pw.Model):
            username = pw.TextField()
            name = pw.CharField(unique=True)
            description = pw.TextField()
            created = pw.DateTimeField()
            country = pw.TextField()
            phone = pw.TextField()
            email = pw.TextField()
            active = pw.BooleanField()

            class Meta:
                database = db

        class Goals(pw.Model):
            # name =  pw.CharField(unique=True)
            name = pw.CharField()
            user = pw.ForeignKeyField(Users, related_name='user_goals')
            created = pw.DateTimeField()
            description = pw.TextField()
            country = pw.TextField()
            year = pw.IntegerField()
            january = pw.DoubleField()
            february = pw.DoubleField()
            march = pw.DoubleField()
            april = pw.DoubleField()
            may = pw.DoubleField()
            june = pw.DoubleField()
            july = pw.DoubleField()
            august = pw.DoubleField()
            september = pw.DoubleField()
            october = pw.DoubleField()
            november = pw.DoubleField()
            december = pw.DoubleField()

            class Meta:
                database = db

        class Groups(pw.Model):
            name = pw.CharField(unique=True)
            description = pw.TextField()
            owner = pw.ForeignKeyField(Users, related_name='group_owner')
            created = pw.DateTimeField()

            class Meta:
                database = db

        class Plans(pw.Model):
            # name =  pw.CharField(unique=True)
            name = pw.CharField()
            description = pw.TextField()
            owner = pw.ForeignKeyField(Users, related_name='plan_owner')
            group = pw.ForeignKeyField(Groups, related_name='plan_group')
            created = pw.DateTimeField()
            due = pw.DateTimeField()
            account = pw.TextField()
            goal = pw.DoubleField()
            chances = pw.DoubleField()
            status = pw.TextField()
            action = pw.TextField()
            calls = pw.DecimalField()
            visits = pw.DecimalField()
            offers = pw.DecimalField()
            hot = pw.BooleanField()

            class Meta:
                database = db

        class Accounts(pw.Model):
            name = pw.CharField(unique=True)

            class Meta:
                database = db

        class Tasks(pw.Model):
            group = pw.ForeignKeyField(Groups, related_name='task_group')
            owner = pw.ForeignKeyField(Users, related_name='task_owner')
            # plan = pw.ForeignKeyField(Plans, related_name='task_plan')
            plan = pw.TextField()
            account = pw.TextField()
            title = pw.TextField()
            description = pw.TextField()
            action = pw.TextField()
            created = pw.DateTimeField()
            due = pw.DateTimeField()
            status = pw.TextField()
            end = pw.DateTimeField()
            allday = pw.BooleanField(default='null')

            class Meta:
                database = db

        db.create_tables([Users, Groups, Plans, Tasks, Goals])

    except:
        raise
        pass


def initTasksTables(dbname, username, name="", email='', local=False, con=None):
    '''
    '''
    now = datetime.datetime.now()
    created = str(now)
    year = now.year

    if email == '':
        email = username.replace("___", "-").replace("__", "@").replace("_", ".")

    if con == None:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()

    cur = con.cursor()

    try:
        script = "\
            INSERT INTO `users`\
            (username, name, description, created, country, phone, email, active)\
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');\
            ".format(username, name, 'default', created, '', '', email, 1)
        cur.execute(script)
        con.commit()

        script = "\
            INSERT INTO `groups`\
            (name, description, owner_id, created)\
            VALUES ('{}', '{}', '{}', '{}')\
            ".format('default', 'default', cur.lastrowid, created)

        cur.execute(script)
        con.commit()

        script = "SELECT country FROM users WHERE name='{}'".format(name)
        cur.execute(script)
        con.commit()
        country = np.ravel(np.asarray(cur.fetchall()))[0]

        script = "\
            INSERT INTO `goals`\
            (name, user_id, created, description, country, year, january, february, march, april, may, june, july, august, september, october, november, december)\
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');\
            ".format('', 1, created, '', country, year, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cur.execute(script)
        con.commit()

        script = "CREATE TABLE Plans_Actions (plan_id INT NOT NULL,\
        task_id INT NOT NULL,PRIMARY KEY\
        (plan_id,task_id),FOREIGN KEY (plan_id) REFERENCES\
        plans(id) ON UPDATE CASCADE,FOREIGN KEY (task_id)\
        REFERENCES tasks(id) ON UPDATE CASCADE);"
        cur.execute(script)
        con.commit()

        script = "CREATE TABLE Users_Actions (user_id INT NOT NULL,\
        task_id INT NOT NULL,PRIMARY KEY\
        (user_id,task_id),FOREIGN KEY (user_id) REFERENCES\
        users(id) ON UPDATE CASCADE,FOREIGN KEY (task_id)\
        REFERENCES tasks(id) ON UPDATE CASCADE);"
        cur.execute(script)
        con.commit()

        script = "CREATE TABLE Users_Plans (user_id INT NOT NULL,\
        plan_id INT NOT NULL,PRIMARY KEY\
        (user_id,plan_id),FOREIGN KEY (user_id) REFERENCES\
        users(id) ON UPDATE CASCADE,FOREIGN KEY (plan_id)\
        REFERENCES plans(id) ON UPDATE CASCADE);"
        cur.execute(script)
        con.commit()

        createUsersCustomersTable(dbname.replace("data_", "data_"), local=False, con=con)

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        raise

    finally:
        if con:
            con.close()


def createUsersCustomersTable(dbname, name="default", local=False, con=None):
    now = datetime.datetime.now()

    if con == None:
        CLOSE_CON = True
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
    else:
        CLOSE_CON = False

    cur = con.cursor()

    try:
        script = "CREATE TABLE Users_Customers (user_id INT NOT NULL,\
        customer_id INT NOT NULL,PRIMARY KEY\
        (user_id,customer_id),FOREIGN KEY (user_id) REFERENCES\
        users(id) ON UPDATE CASCADE,FOREIGN KEY (customer_id)\
        REFERENCES {}.customers(id) ON UPDATE CASCADE);".format(dbname.replace("data_", "data_"))
        cur.execute(script)
        con.commit()

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise
        print(e)

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def initTasksTableGoals(dbname, name="default", local=False):
    created = str(datetime.datetime.now())

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "SELECT country FROM users WHERE name='{}'".format(name)
        cur.execute(script)
        con.commit()
        country = np.ravel(np.asarray(cur.fetchall()))[0]

        script = "\
            INSERT INTO `goals`\
            (name, user_id, created, description, country, january, february, march, april, may, june, july, august, september, october, november, december)\
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');\
            ".format('', 1, created, '', country, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cur.execute(script)
        con.commit()

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        raise

    finally:
        if con:
            con.close()


def delete_databases(dbname, local=False):
    '''
    '''

    print("Deleting old database...")
    try:
        dropDatabase(dbname='data_' + dbname, local=local)
    except Exception as e:
        print(e)

    try:
        dropDatabase(dbname='results_' + dbname, local=local)
    except Exception as e:
        print(e)

    try:
        dropDatabase(dbname='data_' + dbname, local=local)
    except Exception as e:
        print(e)


# def init_databases(dbname, username, local=False):
def createDatabases(dbname, local=False):
    '''
    '''
    createDatabase(dbname='data_' + dbname, local=local)
    createDatabase(dbname='results_' + dbname, local=local)
    createDatabase(dbname="data_" + dbname, local=local)


# def createTables(dbname, username, local=False):
def createTasksTables(dbname, username, name="", local=False):
    '''
    '''
    # createDataTables(dbname='data_' + dbname, local=local)
    addTasksTables(dbname="data_" + dbname, local=local)
    initTasksTables(dbname="data_" + dbname, username=username, name=name, local=local)
    createUsersCustomersTable(dbname="data_" + dbname, local=local)
    addtables.createUserGroupTable(dbname="data_" + dbname, local=local)


def createProductTables(dbname, local=False):
    '''
    '''
    dbname = 'data_' + dbname
    con = addtables.connectDB(dbname)

    addtables.addProductTable(dbname, name='product_class', parent=None, con=con)
    addtables.addProductTable(dbname, name='product_line', parent='product_class', con=con)
    addtables.addProductTable(dbname, name='product_type', parent='product_line', con=con)
    addtables.addProductTable(dbname, name='products', parent='product_type', con=con)

    addtables.initNewTable(dbname, name='product_class', parent=None, con=con)
    addtables.initNewTable(dbname, name='product_line', parent='product_class', con=con)
    addtables.initNewTable(dbname, name='product_type', parent='product_line', con=con)


if __name__ == "__main__":
    dbname = 'qymatix_best'
    dbname = 'coldjet_qy'
    username = 'robert_gruen'

    username = 'bob'
    username = 'alice'
    dbname = 'qy-test.com'.replace("-", "___").replace(".", "_")
    dbname = 'qymatix-solutions.com'.replace("-", "___").replace("@", "__").replace(".", "_")
    dbname = 'qymatix-aet.com'.replace("-", "___").replace("@", "__").replace(".", "_")

    # delete_databases(dbname=dbname)
    # createDatabases(dbname=dbname)
    # createProductTables(dbname)
    # createCustomersTable(dbname)
    # createContactsTable(dbname)
    # createSalesTable(dbname)
    # createTasksTables(dbname=dbname, username=username)
    # createUsersCustomersTable(dbname='data_' + dbname)
