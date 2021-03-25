import sys

import MySQLdb as mysql

path = '/var/www/qyapp'
if path not in sys.path:
    sys.path.append(path)

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qyapp.settings")
from django.contrib.auth.models import User

from api.infrastructure.mysql import connection


def createCustomersTable(dbname, name="default", local=False, con=None):
    '''
    '''

    if con == None:
        CLOSE_CON = True
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
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

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def rename_users():
    '''
    '''
    users = User.objects.all()
    dbnames = []
    db = 'data'
    db = 'tasks'
    for user in users:
        if user.username != 'admin':
            # if 'martin_masip' in user.username:
            # if 'orbus' in user.email:
            if True:
                # if 'qymatix.best' in user.email:
                try:
                    group = user.email.split('@')[1].replace(".", "_").replace("-", "___")
                    print(group)
                    if group not in user.username:
                        print(user.username)
                        user.username = user.email.replace("@", "__").replace(".", "_").replace("-", "___")
                        print(user.username)
                        user.save()
                except Exception as e:
                    print(e)

            # try:
            ##print(user.email.split('@')[1].replace(".", "_"))
            ##dbnames.append(db + "_" + user.email.split('@')[1].replace(".", "_"))
            ##dbnames.append(db + "_" + user.email.split('@')[1].replace(".", "_").replace("-", "___"))
            # dbnames.append(db + "_" + user.email.split('@')[0].replace(".", "_").replace("-", "___"))
            # dbnames.append(db + "_" + user.email.split('@')[1].replace(".", "_").replace("-", "___"))
            # except:
            # print("^^^")
            # pass


def replaceAccountByAccountId(dbname, name="default", local=False, con=None):
    '''
    '''
    if con == None:
        CLOSE_CON = True
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
    else:
        CLOSE_CON = False

    cur = con.cursor()

    # account = unquote_plus(account)
    # try:
    # account  = account.decode('utf-8').encode('cp1252')
    # except:
    # account  = account.encode('cp1252')

    users = User.objects.all()
    dbnames = []
    db = 'data'
    db = 'tasks'
    for user in users:
        if name in user.email and user.username != 'admin':
            dbname = user.email.split('@')[1].replace(".", "_").replace("-", "___")
            print(dbname)
            try:
                query = "\
                    UPDATE data_{0}.tasks t\
                    INNER JOIN data_{0}.customers c ON t.account=c.name\
                    SET t.account=c.id\
                ".format(dbname)
                cur.execute(query)
                con.commit()

                query = "\
                    UPDATE data_{0}.plans p\
                    INNER JOIN data_{0}.customers c ON p.account=c.name\
                    SET p.account=c.id\
                ".format(dbname)
                cur.execute(query)
                con.commit()

            except mysql.Error as e:
                print("Error {}: {}".format(e.args[0], e.args[1]))
                # raise

            finally:
                if CLOSE_CON:
                    if con:
                        try:
                            con.close()
                        except:
                            pass


def deleteTasksItemsWithNonExistingAccounts(dbname, name="default", local=False, con=None):
    '''
    '''
    if con == None:
        CLOSE_CON = True
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
    else:
        CLOSE_CON = False

    cur = con.cursor()

    try:
        # SELECT pa.plan_id, pa.task_id, t.id, t.account, c.name FROM data_{0}.Plans_Actions pa\
        query = "\
            DELETE ua FROM data_{0}.Plans_Actions ua\
            LEFT JOIN data_{0}.tasks AS t\
            ON ua.task_id=t.id\
            LEFT JOIN data_{0}.customers AS c\
            ON c.id=t.account\
            WHERE c.id IS NULL\
        ".format(dbname)
        cur.execute(query)

        query = "\
            DELETE ua FROM data_{0}.Users_Actions ua\
            LEFT JOIN data_{0}.tasks AS t\
            ON ua.task_id=t.id\
            LEFT JOIN data_{0}.customers AS c\
            ON c.id=t.account\
            WHERE c.id IS NULL\
        ".format(dbname)
        cur.execute(query)
        con.commit()

        query = "\
            DELETE p FROM data_{0}.plans p\
            LEFT JOIN data_{0}.customers c ON p.account=c.id\
            WHERE c.id IS NULL\
        ".format(dbname)
        cur.execute(query)
        con.commit()

        query = "\
            DELETE t FROM data_{0}.tasks AS t\
            LEFT JOIN data_{0}.customers AS c ON t.account=c.id\
            WHERE c.id IS NULL\
        ".format(dbname)
        cur.execute(query)
        con.commit()

        # data = np.asarray(cur.fetchall())
        # cols = [desc[0] for desc in cur.description]
        # print(cols)


    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


if __name__ == "__main__":
    dbname = 'qymatix_best'
    dbname = 'qymatix_solutions'
    name = 'qymatix-solutions.com'
    replaceAccountByAccountId(dbname, name=name)
    # deleteTasksItemsWithNonExistingAccounts(dbname)
    # rename_users()
