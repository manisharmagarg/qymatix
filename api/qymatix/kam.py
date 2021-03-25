import datetime
import sys
from ast import literal_eval as make_tuple

import MySQLdb as mysql
import numpy as np
import pandas as pd

path = '/var/www/qyapp'
if path not in sys.path:
    sys.path.append(path)

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qyapp.settings")
import django
django.setup()

from django.contrib.auth.models import User

# from api.groupsapi.groups import getGroupsPerUser
# from api.groupsapi.groups import getUsersPerGroup

from api.infrastructure.mysql import connection

import logging


logger = logging.getLogger(__name__)


def insertKamFromFile(dbname, filename=None, name="default", local=False, lines=None):
    created = str(datetime.datetime.now())

    mysql_connection = connection.MySQLConnection(dbname)
    con = mysql_connection.connect()
    cur = con.cursor()

    data = pd.read_excel(filename)
    print(data.columns)

    # for i in data.index.tolist():
    # if lines != None:
    # if i > lines:
    # return
    # sys.stdout.write("\r")
    # sys.stdout.write("{} form {}".format(i, len(data.index.tolist())))
    # sys.stdout.flush()

    for c in data.columns:
        if c in (u'KAM', u'kam'):
            sales_kams = data[c].unique()

            if sales_kams != []:
                for name in sales_kams:
                    try:
                        name = name.decode('utf-8').encode('latin-1')
                    except:
                        name = name.encode('latin-1')

                    try:
                        script = "\
                            INSERT INTO `users`\
                            (name, description, created)\
                            VALUES ('', '{}', '{}', '{}', '', '', '', 0);\
                            ".format(name, 'Added from list', created)
                        cur.execute(script)
                        con.commit()

                    except mysql.Error as e:
                        print("Error {}: {}".format(e.args[0], e.args[1]))
                        # sys.exit(1)
                        pass

    # finally:
    if con:
        con.close()


def insertKam(dbname, data, local=False, lines=None):
    '''
    '''
    if "username" not in data.keys():
        data['username'] = ''
        data['active'] = 0

    else:
        users = User.objects.all()
        usernames = []
        for user in users:
            usernames.append(user.username)
        if data['username'] not in usernames:
            data['username'] = ""
            data['active'] = 0

    if "description" not in data.keys():
        data['description'] = ''
    if "country" not in data.keys():
        data['country'] = ''
    if "phone" not in data.keys():
        data['phone'] = ''
    if "email" not in data.keys():
        data['email'] = ''

    # try:
    # data['name'] = data['name'].decode('utf-8').encode('latin-1')
    # except:
    # data['name'] = data['name'].encode('latin-1')
    # try:
    # data['description'] = data['description'].decode('utf-8').encode('latin-1')
    # except:
    # data['description'] = data['description'].encode('latin-1')

    for k in ('name', 'description'):
        pass
        # try:
        #     data[k] = data[k].strip().decode('utf-8').encode('latin-1')
        # except:
        #     data[k] = data[k].encode('latin-1')

    created = str(datetime.datetime.now())

    datadb = "data_" + dbname
    mysql_connection = connection.MySQLConnection(datadb)
    con = mysql_connection.connect()
    cur = con.cursor()

    try:
        script = "INSERT INTO `users`(username, name, description, created, country, phone, email, active) VALUES "\
        "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
            data['username'], 
            data['name'], 
            data['description'], 
            created, 
            data['country'], 
            data['phone'],
            data['email'], 
            data['active']
        )
        # print(script)
        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from users;"
        cur.execute(script)
        # con.commit()
        user_id = np.ravel(np.asarray(cur.fetchall()))[0]
        return user_id
    except mysql.Error as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        if int(e.args[0]) == 1062:
            script = "SELECT id FROM users WHERE name='{}';".format(data['name'])

            cur.execute(script)
            con.commit()

            user_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return user_id

        return -1

    finally:
        if con:
            con.close()

        return user_id


def setKam(dbname, data, local=False):
    """
    """

    try:
        datadb = "data_" + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        for col in data.keys():
            if col != ['id', 'created']:
                value = data[col]
                if col in ('name', 'description'):
                    value = value #.decode('utf-8').encode('latin-1')
                user_id = data['id']
                script = "UPDATE {} SET {}='{}' WHERE id={}".format('users', col, value, user_id)
                cur.execute(script)
                con.commit()

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)

    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. Contact your administrator."

    return data['id']


def dropKam(dbname, user_id, local=False):
    """
    """

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "\
            DELETE FROM Users_Actions WHERE user_id={};\
            ".format(int(user_id))
        cur.execute(script)
        con.commit()

        script = "\
            DELETE FROM Users_Plans WHERE user_id={};\
            ".format(int(user_id))
        cur.execute(script)
        con.commit()

        script = "\
            DELETE FROM Users_Customers WHERE user_id={};\
            ".format(int(user_id))
        cur.execute(script)
        con.commit()

        # DELETE FROM tasks WHERE id = {} AND id_product = 2 LIMIT 1\
        script = "\
            DELETE FROM users WHERE id={}\
            ".format(user_id)
        cur.execute(script)
        con.commit()
        # data = np.asarray(cur.fetchall())

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        pass
        # sys.exit(1)
        # return e.args[1]


def getKam(dbname='username', user='all', group_id=0, user_id=0, username='', raw=False, local=False):
    ''' Reads tasks's database, manipulate the data and returns it.
    '''
    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        # try:
        #     user = user.decode('utf-8').encode('latin-1')
        # except:
        #     user = user.encode('latin-1')

        if username == 'admin':
            if user == 'all':
                script = "SELECT * from users;"
            else:
                script = "SELECT * from users WHERE username='{}';".format(
                    user
                )

        else:
            if user_id == 0 and username != "":
                script = "SELECT * FROM users WHERE username = '{}';".format(
                    username
                )
                cur.execute(script)
                # con.commit()
                user_id = np.ravel(np.asarray(cur.fetchall()))[0]

            if group_id == -1:
                try:
                    group_id = getGroupsPerUser(dbname.replace('data_', ''), username=username, user_id=user_id)[
                        user_id]
                except:
                    group_id = "(-1)"

                user_per_group = []
                for g in make_tuple(group_id):
                    upg = getUsersPerGroup(dbname.replace('data_', ''), username=username, user_id=0)[g]
                    upg = upg[1:-1].split(',')
                    user_per_group += upg

                user_per_group = tuple((int(u) for u in user_per_group))

            try:
                group_id = ''.join(str(group_id))[1:-1]
            except Exception as e:
                pass

            script = "SELECT * from users WHERE id IN {};".format(
                user_per_group
            )

        cur.execute(script)
        cols = [desc[0] for desc in cur.description]
        data = np.asarray(cur.fetchall())

        try:
            df = pd.DataFrame(data, columns=cols)

            # f = lambda x: x.isoformat().split("T")[0]
            # df['due'] = df['due'].apply(f)
            # df['created'] = df['created'].apply(f)

            grouped = df.groupby('name')
            tasks = {}
            for name, group in grouped:
                # group = group.rename(columns={'due':'date', 'action':'type', 'description':'Comment'})
                # group[['due', 'id', 'created', 'action', 'title', 'description' ]]
                if not name:
                    continue
                tasks[name] = group.to_json(orient='records')

                # tasks[name] = group.to_dict(orient='records')
        except Exception as e:
            tasks = []
            raise


    except Exception as e:
        # print("Error %d: %s" % (e.args[0],e.args[1]))
        # sys.exit(1)
        tasks = []

    finally:
        if con:
            con.close()

    return tasks


def linkUserToAction(dbname, user_id, task_id, local=False):
    '''
    '''

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "\
            INSERT INTO Users_Actions (user_id, task_id) VALUES({},{});\
            ".format(int(user_id), int(task_id))

        cur.execute(script)
        con.commit()
        '''
        try:
            data = np.asarray(cur.fetchall())
            logger.debug("__xxxyyy_____")
            logger.debug(data)
        except:
            data = {}
        '''
        data = "{}"

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        # data = e.args[1]
        data = {}
        data = 'Error'

    finally:
        if con:
            con.close()

    return data


def unlinkUserFromAction(dbname, user_id, task_id, local=False):
    '''
    '''

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "\
            DELETE FROM Users_Actions WHERE user_id={} AND task_id={};\
            ".format(int(user_id), int(task_id))

        cur.execute(script)
        con.commit()
        data = np.asarray(cur.fetchall())

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        data = e.args[1]

    finally:
        if con:
            con.close()

    return data


def linkUserToPlan(dbname, user_id, plan_id, local=False):
    '''
    '''

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "\
            INSERT INTO Users_Plan (user_id, plan_id) VALUES({},{});\
            ".format(int(user_id), int(plan_id))

        cur.execute(script)
        con.commit()
        '''
        try:
            data = np.asarray(cur.fetchall())
            logger.debug("__xxxyyy_____")
            logger.debug(data)
        except:
            data = {}
        '''
        data = "{}"

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        # data = e.args[1]
        data = {}
        data = 'Error'

    finally:
        if con:
            con.close()

    return data


def unlinkUserFromPlan(dbname, user_id, plan_id, local=False):
    '''
    '''

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "\
            DELETE FROM Users_Plans WHERE user_id={} AND plan_id={};\
            ".format(int(user_id), int(plan_id))

        cur.execute(script)
        con.commit()
        data = np.asarray(cur.fetchall())

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        data = e.args[1]

    finally:
        if con:
            con.close()

    return data


def linkUserToCustomer(dbname, user_id, customer_id, local=False):
    '''
    '''

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "\
            INSERT INTO Users_Customers (user_id, customer_id) VALUES({},{});\
            ".format(int(user_id), int(customer_id))

        cur.execute(script)
        con.commit()
        '''
        try:
            data = np.asarray(cur.fetchall())
            logger.debug("__xxxyyy_____")
            logger.debug(data)
        except:
            data = {}
        '''
        data = "{}"

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        # data = e.args[1]
        data = {}
        data = 'Error'

    finally:
        if con:
            con.close()

    return data


def unlinkUserFromCustomer(dbname, user_id, customer_id, local=False):
    '''
    '''

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "\
            DELETE FROM Users_Customers WHERE user_id={} AND customer_id={};\
            ".format(int(user_id), int(customer_id))

        cur.execute(script)
        con.commit()
        data = np.asarray(cur.fetchall())

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        data = e.args[1]

    finally:
        if con:
            con.close()

    return data


def getPerformance(dbname, user_id='all', local=False):
    '''
    '''
    try:
        if False:
            mysql_connection = connection.MySQLConnection(dbname)
            con = mysql_connection.connect()
            cur = con.cursor()

        # script = "\
        # DELETE FROM Users_Customers WHERE user_id={} AND customer_id={};\
        # ".format(int(user_id), int(customer_id))

        # cur.execute(script)
        # con.commit()
        # data = np.asarray(cur.fetchall())

        data = \
            { \
                "Acrion": [{ \
                    "sales_QTD": 1234, \
                    "growth_QTD": 12.33, \
                    "pipeline": 4444, \
                    "KAM": "Jenny Salesfrau" \
                    }], \
                "Aedesia": [{ \
                    "sales_QTD": 1234, \
                    "growth_QTD": 12.33, \
                    "pipeline": 4444, \
                    "KAM": "Max Represent" \
                    }], \
                "Boethus": [{ \
                    "sales_QTD": 1234, \
                    "growth_QTD": 2.31, \
                    "pipeline": 4444, \
                    "KAM": "Jenny Salesfrau" \
                    }], \
                "Buselos": [{ \
                    "sales_QTD": 7000, \
                    "growth_QTD": 4.33, \
                    "pipeline": 12000, \
                    "KAM": "John Salesman" \
                    }], \
                "Diotimus": [{ \
                    "sales_QTD": 1234, \
                    "growth_QTD": 2.33, \
                    "pipeline": 4444, \
                    "KAM": "John Salesman" \
                    }], \
                "EURI": [{ \
                    "sales_QTD": 123, \
                    "growth_QTD": 12.33, \
                    "pipeline": 666, \
                    "KAM": "Jenny Salesfrau" \
                    }], \
                "Metro": [{ \
                    "sales_QTD": 1234, \
                    "growth_QTD": -0.23, \
                    "pipeline": 3333, \
                    "KAM": "Max Represent" \
                    }] \
                }

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        data = e.args[1]

    finally:
        try:
            con.close()
        except:
            pass

    return data


def getPerformanceKpi(dbname, user_id='all', local=False):
    '''
    '''
    try:
        if False:
            mysql_connection = connection.MySQLConnection(dbname)
            con = mysql_connection.connect()
            cur = con.cursor()

        # script = "\
        # DELETE FROM Users_Customers WHERE user_id={} AND customer_id={};\
        # ".format(int(user_id), int(customer_id))

        # cur.execute(script)
        # con.commit()
        # data = np.asarray(cur.fetchall())

        data = \
            {
                "active_accounts": [
                    {"Nabay": 14645.94},
                    {"Zama": 26693.45},
                    {"Metro": 45760.03},
                    {"Siro": 10257.93},
                    {"Xeniades": 6037.95},
                    {"Tara": 15425.23},
                    {"Solvent": 41854.7},
                    {"Boethus": 8671.69},
                    {"Polemon": 21200.29},
                    {"Diotimus": 43128.16},
                    {"Aedesia": 42083.93},
                    {"EURI": 14509.9},
                    {"Buselos": 18304.95}
                ],
                "active_accounts_last_quarter": [
                    {"Nabay": 14645.94},
                    {"New company": 26693.45},
                    {"Metro": 45760.03},
                    {"Siro": 10257.93},
                    {"Xeniades": 6037.95},
                    {"Tara": 15425.23},
                    {"Solvent": 41854.7},
                    {"Boethus": 8671.69},
                    {"Polemon": 21200.29},
                    {"Aedesia": 42083.93},
                    {"EURI": 14509.9},
                    {"Buselos": 18304.95}
                ],
                "penetration_ratio": 92.85714285714286,
                "penetration_ratio_last_month": 82.85714285714286,
                "sales_QTD": 88888,
                "sales_QTD_last_quarter": 77777,
                "lost_accounts": ["Acrion"],
                "lost_accounts_last_quarter": ["Diotimus", "Acrion"],
                "actions_per_day": [
                    {"2016-01-08": 2},
                    {"2016-02-14": 1}
                ],
                "actions_this_month": 8,
                "actions_last_month": 7,
                "plans_per_account": {"AKS": 1, "EGF": 13, "Nabay": 12},
                "plans_per_account_last_month": {"AKS": 1, "EGF": 13}
            }

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        data = e.args[1]

    finally:
        try:
            con.close()
        except:
            pass

    return data


if __name__ == "__main__":
    dbname = 'martinmasip'
    dbname = 'qymatix_best'
    data = {'username': 'something', 'name': 'John'}
    insertKam(dbname, data)
    dbname = 'qymatix_best'
    # username = 'chancho_babe__qymatix_best'
    username = 'chancho_babe__qymatix_best'
    # username = 'admin'
    user = 'all'
    group_id = -1
    kams = getKam('data_' + dbname, group_id=group_id, user=user, username=username)
    print(kams)
    print(kams.keys())
