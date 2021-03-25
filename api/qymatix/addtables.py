import sys

import MySQLdb as mysql

path = '/var/www/qyapp'
if path not in sys.path:
    sys.path.append(path)

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qyapp.settings")
from django.contrib.auth.models import User


def createCustomersTable(dbname, name="default", local=False, con=None):
    '''
    '''

    if con == None:
        CLOSE_CON = True
        if local == False:
            print("\nConnecting to remote database {}".format(dbname))
            con = mysql.connect('80.147.39.6', 'webuser', 'Qymatix!!!', 'data_' + dbname);
        else:
            print("\nConnecting to local database {}".format(dbname))
            con = mysql.connect('localhost', 'webadmin', 'Qymatix!!!', 'data_' + dbname);
    else:
        CLOSE_CON = False

    cur = con.cursor()

    try:
        query = "\
           CREATE TABLE `customers` (\
              `id` int(11) NOT NULL AUTO_INCREMENT,\
              `name` varchar(255) NOT NULL,\
              `address` varchar(255) NOT NULL,\
              `postcode` varchar(255) NOT NULL,\
              `city` varchar(255) NOT NULL,\
              `country` varchar(255) NOT NULL,\
              `revenue` double NOT NULL,\
              `employees` int(11) NOT NULL,\
              `telephone` int(20) NOT NULL, \
              `industry` varchar(255) NOT NULL,\
              `classification` varchar(255) NOT NULL,\
              `website` text NOT NULL,\
              `comment` longtext NOT NULL,\
              `favorite` bool NOT NULL,\
              PRIMARY KEY (`id`),\
              UNIQUE KEY `customers_name` (`name`)\
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;\
        "
        cur.execute(query)
        con.commit()

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def createSalesTable(dbname, name="default", local=False, con=None):
    '''
    '''

    if con == None:
        CLOSE_CON = True
        if local == False:
            print("\nConnecting to remote database {}".format(dbname))
            con = mysql.connect('80.147.39.6', 'webuser', 'Qymatix!!!', 'data_' + dbname);
        else:
            print("\nConnecting to local database {}".format(dbname))
            con = mysql.connect('localhost', 'webadmin', 'Qymatix!!!', 'data_' + dbname);
    else:
        CLOSE_CON = False

    cur = con.cursor()

    try:
        query = "\
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
              CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),\
              KEY `sales_product_id` (`product_id`),\
              CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)\
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;\
        "
        cur.execute(query)
        con.commit()

        '''
        script = "\
        ALTER TABLE sales ADD UNIQUE UNIQUE_INDEX(customer_id, product_id, quantity, price, cost, margin, year, month, date);\
        "
        cur.execute(script)
        con.commit()
        '''

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def createContactsTable(dbname, name="default", local=False, con=None):
    '''
    '''

    if con == None:
        CLOSE_CON = True
        if local == False:
            print("\nConnecting to remote database {}".format(dbname))
            con = mysql.connect('80.147.39.6', 'webuser', 'Qymatix!!!', 'data_' + dbname);
        else:
            print("\nConnecting to local database {}".format(dbname))
            con = mysql.connect('localhost', 'webadmin', 'Qymatix!!!', 'data_' + dbname);
    else:
        CLOSE_CON = False

    cur = con.cursor()

    try:
        query = "\
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
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;\
        "
        cur.execute(query)
        con.commit()

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def connectDB(dbname, local=False):
    '''
    '''
    try:
        if local == False:
            print("\nConnecting to remote database {}".format(dbname))
            con = mysql.connect('80.147.39.6', 'webuser', 'Qymatix!!!', dbname);
        else:
            print("\nConnecting to local database {}".format(dbname))
            con = mysql.connect('localhost', 'webadmin', 'Qymatix!!!', dbname);

        return con

    except mysql.Error as e:
        print("Cannot connect to db")
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise


def createUserGroupTable(dbname, local=False, con=None):
    '''
    '''
    if con == None:
        CLOSE_CON = True
        con = connectDB(dbname)
    else:
        CLOSE_CON = False

    if con == None:
        return
    else:
        cur = con.cursor()

    try:
        script = "use {};".format(dbname)
        cur.execute(script)
        con.commit()
        script = "CREATE TABLE Users_Groups (user_id INT NOT NULL,\
        group_id INT NOT NULL,PRIMARY KEY\
        (user_id,group_id),FOREIGN KEY (user_id) REFERENCES\
        users(id) ON UPDATE CASCADE,FOREIGN KEY (group_id)\
        REFERENCES groups(id) ON UPDATE CASCADE);"
        cur.execute(script)
        con.commit()

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def addProductTable(dbname, name, parent=None, local=False, con=None):
    '''
    '''
    print(dbname)
    if con == None:
        CLOSE_CON = True
        con = connectDB(dbname)
    else:
        CLOSE_CON = False

    if con == None:
        return
    else:
        cur = con.cursor()

    try:
        if parent != None:
            script = "use {};".format(dbname)
            cur.execute(script)
            con.commit()
            if parent == 'product_type':
                script = "\
                   CREATE TABLE `{0}` (\
                      `id` int(11) NOT NULL AUTO_INCREMENT,\
                      `name` varchar(255) NOT NULL,\
                      `{1}_id` int(11) NOT NULL,\
                      `description` longtext NOT NULL,\
                      `active` bool NOT NULL,\
                      `created` datetime NOT NULL,\
                      `number` varchar(255) NOT NULL,\
                      `serial` varchar(255) NOT NULL,\
                      PRIMARY KEY (`id`),\
                      UNIQUE KEY `{0}_name` (`name`),\
                      KEY `{0}_{1}_id` (`{1}_id`),\
                      CONSTRAINT `{0}_ibfk_1` FOREIGN KEY (`{1}_id`) REFERENCES `{1}` (`id`)\
                    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;\
                ".format(name, parent)
            else:
                script = "\
                   CREATE TABLE `{0}` (\
                      `id` int(11) NOT NULL AUTO_INCREMENT,\
                      `name` varchar(255) NOT NULL,\
                      `{1}_id` int(11) NOT NULL,\
                      `description` longtext NOT NULL,\
                      `active` bool NOT NULL,\
                      `created` datetime NOT NULL,\
                      `number` varchar(255) NOT NULL,\
                      PRIMARY KEY (`id`),\
                      UNIQUE KEY `{0}_name` (`name`),\
                      KEY `{0}_{1}_id` (`{1}_id`),\
                      CONSTRAINT `{0}_ibfk_1` FOREIGN KEY (`{1}_id`) REFERENCES `{1}` (`id`)\
                    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;\
                ".format(name, parent)
        else:
            script = "use {};".format(dbname)
            cur.execute(script)
            con.commit()
            script = "\
               CREATE TABLE `{0}` (\
                  `id` int(11) NOT NULL AUTO_INCREMENT,\
                  `name` varchar(255) NOT NULL,\
                  `description` longtext NOT NULL,\
                  `active` bool NOT NULL,\
                  `created` datetime NOT NULL,\
                  PRIMARY KEY (`id`),\
                  UNIQUE KEY `{0}_name` (`name`)\
                ) ENGINE=InnoDB DEFAULT CHARSET=latin1;\
            ".format(name, parent)

        cur.execute(script)
        con.commit()


    except mysql.Error as e:
        print(">>>")
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def addColumnToTable(dbname, table, column=None, col_type='int(11)', fk_table=None, fk='id', after=None, local=False,
                     con=None):
    '''
    '''
    print(dbname)
    if con == None:
        CLOSE_CON = True
        con = connectDB(dbname)
    else:
        CLOSE_CON = False

    if con == None:
        return
    else:
        cur = con.cursor()

    try:
        script = "set foreign_key_checks = 0;".format(dbname)
        cur.execute(script)
        con.commit()

        if fk_table != None:
            if column == None:
                column = fk_table + "_" + fk
            script = "use {};".format(dbname)
            cur.execute(script)
            con.commit()
            if after == None:
                script = "\
                   ALTER TABLE `{0}`\
                      ADD COLUMN `{1}` {2} NOT NULL,\
                      ADD CONSTRAINT `{1}_ibfk_1` FOREIGN KEY (`{3}_{4}`) REFERENCES `{3}` (`{4}`)\
                ".format(table, column, col_type, fk_table, fk)
            else:
                script = "\
                   ALTER TABLE `{0}`\
                      ADD COLUMN `{1}` {2} NOT NULL AFTER {5},\
                      ADD CONSTRAINT `{1}_ibfk_1` FOREIGN KEY (`{3}_{4}`) REFERENCES `{3}` (`{4}`)\
                ".format(table, column, col_type, fk_table, fk, after)


        else:
            if column == None:
                print("If not using fk, define a column name.")
                return

            script = "use {};".format(dbname)
            cur.execute(script)
            con.commit()
            if after == None:
                script = "\
                   ALTER TABLE `{0}`\
                      ADD COLUMN `{1}` {2} NOT NULL\
                ".format(table, column, col_type)
            else:
                script = "\
                   ALTER TABLE `{0}`\
                      ADD COLUMN `{1}` {2} NOT NULL AFTER {3}\
                ".format(table, column, col_type, after)

        print(script)
        cur.execute(script)
        con.commit()
        script = "set foreign_key_checks = 1;".format(dbname)
        cur.execute(script)
        con.commit()


    except mysql.Error as e:
        print(">>>")
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def runScript(dbname, script, local=False, con=None):
    '''
    '''
    print(dbname)
    if con == None:
        CLOSE_CON = True
        con = connectDB(dbname)
    else:
        CLOSE_CON = False

    if con == None:
        return
    else:
        cur = con.cursor()

    try:
        cur.execute(script)
        con.commit()
    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


# def insertRowIntoTable(dbname, table, data, local=False, con=None):
def initNewTable(dbname, name, parent, local=False, con=None):
    '''
    '''
    print(dbname)
    if con == None:
        CLOSE_CON = True
        con = connectDB(dbname)
    else:
        CLOSE_CON = False

    if con == None:
        return
    else:
        cur = con.cursor()

    try:
        # data['created'] = str(datetime.datetime.now())
        # script = "set foreign_key_checks = 0;".format(dbname)
        # cur.execute(script)
        # con.commit()

        if parent != None:
            script = "\
                INSERT INTO `{0}`\
                (name, {1}_id)\
                VALUES ('{2}','{3}');\
                ".format( \
                name,
                parent,
                'empty',
                1
            )
        else:
            script = "\
                INSERT INTO `{0}`\
                (name)\
                VALUES ('{1}');\
                ".format( \
                name,
                'empty'
            )
        cur.execute(script)
        con.commit()

    except mysql.Error as e:
        print(">>>")
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def createProductTables(dbname, local=False):
    '''
    '''
    dbname = 'data_' + dbname
    con = connectDB(dbname)

    addProductTable(dbname, name='product_class', parent=None, con=con)
    addProductTable(dbname, name='product_line', parent='product_class', con=con)
    addProductTable(dbname, name='product_type', parent='product_line', con=con)
    addProductTable(dbname, name='products', parent='product_type', con=con)

    initNewTable(dbname, name='product_class', parent=None, con=con)
    initNewTable(dbname, name='product_line', parent='product_class', con=con)
    initNewTable(dbname, name='product_type', parent='product_line', con=con)


def createUsersAccountType(dbname, name="default", local=False, con=None):
    '''
    '''

    if con == None:
        CLOSE_CON = True
        if local == False:
            print("\nConnecting to remote database {}".format(dbname))
            # con = mysql.connect('80.147.39.6', 'webuser', 'Qymatix!!!', 'data_' + dbname);
            con = mysql.connect('80.147.39.6', 'webuser', 'Qymatix!!!', dbname);
        else:
            print("\nConnecting to local database {}".format(dbname))
            # con = mysql.connect('localhost', 'webadmin', 'Qymatix!!!', 'data_' + dbname);
            con = mysql.connect('localhost', 'webadmin', 'Qymatix!!!', dbname);
    else:
        CLOSE_CON = False

    cur = con.cursor()

    try:
        query = "CREATE TABLE Users_AccountType (\
                    user_id INT NOT NULL,\
                    accountType_id INT NOT NULL,\
                    PRIMARY KEY (user_id),\
                    UNIQUE KEY `Users_AccountType_user_id` (`user_id`),\
                    FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE\
                    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;\
                "
        # FOREIGN KEY (group_id) REFERENCES groups(id) ON UPDATE CASCADE\

        cur.execute(query)
        con.commit()

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


if __name__ == "__main__":

    # from django.conf import settings
    # print(settings.ENVIRONMENT_VARIABLE)

    users = User.objects.all()
    dbnames = []
    db = 'data'
    db = 'tasks'
    for user in users:
        if user.username != 'admin':
            # dbnames.append(db + "_" + user.username)

            # if 'martin_masip' in user.username:
            # if 'orbus' in user.email:
            # if True:
            # if 'qymatix.best' in user.email:
            # if 'qymatix.de' in user.email:
            # if 'aet.at' in user.email:
            # if 'qy-wine.con' in user.email:
            # if 'manhand-test.de' in user.email:
            if 'spm.li' in user.email:
                print(user.email)
                # print(user.email.split('@')[1].replace(".", "_"))
                try:
                    # print(user.email.split('@')[1].replace(".", "_"))
                    # dbnames.append(db + "_" + user.email.split('@')[1].replace(".", "_"))
                    # dbnames.append(db + "_" + user.email.split('@')[1].replace(".", "_").replace("-", "___"))
                    dbnames.append(db + "_" + user.email.split('@')[0].replace(".", "_").replace("-", "___"))
                    dbnames.append(db + "_" + user.email.split('@')[1].replace(".", "_").replace("-", "___"))
                except:
                    print("^^^")
                    pass

    for dbname in dbnames:
        print(dbname)
        try:
            # createUserGroupTable(dbname)
            if False:
                createUsersAccountType(dbname)

            if False:
                addProductTable(dbname, name='product_class', parent=None)
                addProductTable(dbname, name='product_line', parent='product_class')
                addProductTable(dbname, name='product_type', parent='product_line')

                initNewTable(dbname, name='product_class', parent=None)
                initNewTable(dbname, name='product_line', parent='product_class')
                initNewTable(dbname, name='product_type', parent='product_line')

                addColumnToTable(dbname, table='products', col_type='int(11)', fk_table='product_type', fk='id')
                addColumnToTable(dbname, table='products', column='description', col_type='longtext')
                addColumnToTable(dbname, table='products', column='active', col_type='bool')
                addColumnToTable(dbname, table='products', column='created', col_type='datetime')
                addColumnToTable(dbname, table='products', column='number', col_type='varchar(255)')
                addColumnToTable(dbname, table='products', column='serial', col_type='varchar(255)')

                addColumnToTable(dbname, table='product_type', column='number', col_type='varchar(255)')
                addColumnToTable(dbname, table='product_line', column='number', col_type='varchar(255)')
                addColumnToTable(dbname, table='product_class', column='number', col_type='varchar(255)')

            if False:
                addColumnToTable(dbname, table='sales', column='quantity', after='product_id', col_type='int(11)')
                addColumnToTable(dbname, table='sales', column='invoice', after='date', col_type='varchar(255)')

            if False:
                addColumnToTable(dbname, table='users', column='username', after='id', col_type='longtext')
                addColumnToTable(dbname, table='users', column='active', after='email', col_type='bool')

            if False:
                script = "ALTER TABLE tasks DROP COLUMN username;"
                runScript(dbname, script)

            if True:
                addColumnToTable(dbname, table='tasks', column='contact_id', after='allday', col_type='int(11)')

            # table = 'product_class'
            # data = {'name': 'empty'}
            # insertRowIntoTable(dbname, table, data, local=False, con=None)
            # table = 'product_line'
            # data = {'name': 'empty', 'product_class_id': 0}
            # insertRowIntoTable(dbname, table, data, local=False, con=None)
            # print(data.keys())

            # addColumnToTable(dbname, table='product_type', col_type='int(11)', fk_table='product_line', fk='id')
            # addColumnToTable(dbname, table='product_line', col_type='int(11)', fk_table='product_class', fk='id')
        except mysql.Error as e:
            print("Error {}: {}".format(e.args[0], e.args[1]))
        # except:
        # raise
