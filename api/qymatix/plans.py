from __future__ import absolute_import

import datetime
import json
import logging
# from .actions import *
# from api.groupsapi.groups import getGroupsPerUser
from api.qymatix import groups
from urllib.parse import unquote_plus

# import MySQLdb as mysql
import mysql.connector
import numpy as np
import pandas as pd

# import actions
from api.qymatix import actions
from api.qymatix.analytics.plans_analytics import plans_analytics
from api.infrastructure.mysql import connection

logger = logging.getLogger('django.request')


def createPlan(dbname, plan, username=None):
    created = str(datetime.datetime.now())

    for k in plan.keys():
        # if k in ('name', 'description', 'account', 'owner'):
        if k in ('name', 'description', 'owner'):
            value = plan[k]
            value = unquote_plus(value)
            # try:
            #     value = value.decode('utf-8').encode('cp1252')
            # except:
            #     value = value.encode('cp1252')
            # plan[k] = value

    name = plan['name']
    description = plan['description']
    due = plan['due']
    account = plan['account']
    goal = float(plan.get('goal'))
    chances = plan['chances']
    status = plan['status']
    action = plan['action']
    calls = int(plan['calls'])
    visits = int(plan['visits'])
    offers = int(plan['offers'])

    if 'owner' not in plan.keys():
        owner = ''

    if 'group_id' not in plan.keys():
        group_id = 1
    else:
        group_id = plan['group_id']

    if 'hot' in plan.keys():
        hot = int(plan['hot'])
    else:
        hot = 0

    try:
        owner_id = int(plan['owner_id'])
    except:
        owner_id = 0

    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        if account != 'all':
            '''
            if account != "":
                script = "\
                    SELECT id FROM {}.customers WHERE name = '{}'\
                    ".format(dbname.replace('data_', 'data_'), account)
            cur.execute(script)
            con.commit()
            account_id = np.ravel(np.asarray(cur.fetchall()))[0]
            '''
            account_id = account

        if owner_id == 0 and owner == "":
            script = "SELECT id FROM users WHERE username = '{}';".format(username)
            cur.execute(script)
            # con.commit()
            owner_id = np.ravel(np.asarray(cur.fetchall()))

        if owner_id == 0 and owner != "":
            script = "SELECT id FROM users WHERE name = '{}';".format(owner)
            cur.execute(script)
            # con.commit()
            owner_id = np.ravel(np.asarray(cur.fetchall()))[0]

        script = "INSERT INTO `plans` (`name`, `description`, `owner_id`, `group_id`, `created`, `due`, `account`, `goal`, `chances`, `status`, `action`, `calls`, `visits`, `offers`, `hot`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
            name, 
            description, 
            owner_id, 
            group_id, 
            created, 
            due, 
            account_id, 
            goal, 
            chances, 
            status, 
            action,
            calls, 
            visits, 
            offers, 
            hot
        )
        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from plans;"
        cur.execute(script)
        # con.commit()
        plan_id = np.ravel(np.asarray(cur.fetchall()))[0]

        plans_analytics.analyzePlans(dbname.split("data_")[1], cur)

        return plan_id

    except Exception as e:
        return e
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # return "Error saving plan."
        # raise


def setPlan(dbname, plan):
    """
    """

    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        for col in plan.keys():
            if col != 'id':
                value = plan[col]
                if col in ('name', 'description', 'account'):
                    value = unquote_plus(value)
                    # try:
                    #     value = value.decode('utf-8').encode('cp1252')
                    # except:
                    #     value = value.encode('cp1252')
                    if col == 'account':
                        if value != "":
                            script = "SELECT id FROM {}.customers WHERE name = '{}';".format(
                                dbname.replace(
                                    'data_', 
                                    'data_'), 
                                value
                            )
                        cur.execute(script)
                        con.commit()
                        value = np.ravel(np.asarray(cur.fetchall()))[0]

                plan_id = plan['id']
                try:
                    script = "UPDATE `{}` SET `{}`='{}' WHERE id={};".format(
                        'plans', 
                        col, 
                        value, 
                        plan_id
                    )
                    # return script
                    cur.execute(script)
                    con.commit()
                except Exception as e:
                    import traceback
                    data = str(traceback.format_exc())
                    return data


        plans_analytics.analyzePlans(dbname.split("data_")[1], cur)

    # except mysql.Error as e:
    # print("Error {}: {}".format(e.args[0], e.args[1]))
    except Exception as e:
        print(e)
        # sys.exit(1)
        # raise

    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. Contact your administrator."
        # raise

    return 'Ok'


def dropPlan(dbname, planid):
    """
    """

    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        script = "\
            DELETE FROM Plans_Actions WHERE plan_id={};\
            ".format(int(planid))

        cur.execute(script)
        con.commit()

        script = "\
            DELETE FROM plans WHERE id = {}\
            ".format(planid)
        cur.execute(script)
        con.commit()

        # data = np.asarray(cur.fetchall())

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)


def getPlans(dbname='username', account='all', group_id=0, user_id=0, username=""):
    ''' Reads plans' database, manipulate the data and returns it.
    '''

    if username == 'admin':
        username = ''
        user_id = 0
        group_id = 0

    try:
        datadb = "data_" + dbname

        mysql_connection = connection.MySQLConnection(datadb)

        con = mysql_connection.connect()

        cur = con.cursor()

        '''
        _account = account
        account = unquote_plus(account)
        try:
            account = account.decode('utf-8')
        except:
            pass
        account = account.encode('cp1252')
        '''

        if account != 'all':
            '''
            if account != "":
                script = "\
                    SELECT id FROM {}.customers WHERE name = '{}'\
                    ".format('data_' + dbname, account)
            cur.execute(script)
            con.commit()
            account_id = np.ravel(np.asarray(cur.fetchall()))[0]
            '''
            account_id = account

        if user_id == 0 and username != "":
            script = "SELECT id FROM users "\
                    "WHERE username = '{}'".format(
                        username
                    )
            cur.execute(script)
            user_id = np.ravel(np.asarray(cur.fetchall()))[0]

        if group_id == -1:
            try:
                # group_id = getGroupsPerUser(dbname, user_id=user_id)[user_id]
                group_id = groups.getGroupsPerUser(dbname, username=username, user_id=user_id)[user_id]
            except:
                group_id = "(-1)"

            try:
                group_id = ''.join(str(group_id))[1:-1]
            except:
                pass

        if account == 'all' and group_id == 0 and user_id == 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                ".format('data_' + dbname)

        elif account == 'all' and group_id != 0 and user_id == 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.group_id IN ({})\
                ".format('data_' + dbname, group_id)

        elif account == 'all' and group_id == 0 and user_id != 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.owner_id = '{}'\
                ".format('data_' + dbname, user_id)

        elif account == 'all' and group_id != 0 and user_id != 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.group_id IN ({}) OR p.owner_id = '{}'\
                ".format('data_' + dbname, group_id, user_id)

        elif account != 'all' and group_id != 0 and user_id == 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.account = '{}' and p.group_id IN ({})\
                ".format('data_' + dbname, account_id, group_id)

        elif account != 'all' and group_id != 0 and user_id != 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.account = '{}' AND (p.group_id IN ({}) OR p.owner_id = '{}')\
                ".format('data_' + dbname, account_id, group_id, user_id)

        elif account != 'all' and group_id == 0 and user_id != 0:
            # else:
            script = "\
                SELECT p.*, c.name AS 'account_name' from plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.account = '{}' and p.owner_id = '{}'\
                ".format('data_' + dbname, account_id, user_id)
        elif account != 'all' and group_id == 0 and user_id == 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.account = '{}'\
                ".format('data_' + dbname, account_id, user_id)

        cur.execute(script)
        data = np.asarray(cur.fetchall())
        logger.info("Plans {}".format(data), extra={'type': 'Plans'})
        # print(data)
        cols = [desc[0] for desc in cur.description]
        try:
            df = pd.DataFrame(data, columns=cols)

            s = lambda x: x.encode('latin-1').decode('cp1252')
            df['description'] = df['description'].apply(s)
            df['name'] = df['name'].apply(s)

            df['account_id'] = df['account']
            df['account'] = df['account_name']
            df.drop('account_name', inplace=True, axis=1)
            df['account'].replace('None', 'Missing account', inplace=True)
            df['account'].fillna('Missing account', inplace=True)
            df['account'] = df['account'].apply(s)

            # f = lambda x: x.isoformat().split("T")[0]
            f = lambda x: x.isoformat().replace("T", " ")
            try:
                df['due'] = df['due'].apply(f)
            except:
                pass
            try:
                df['created'] = df['created'].apply(f)
            except:
                pass

            grouped = df.groupby('account_id')

            plans = {}
            for name, group in grouped:
                # group = group.rename(columns={'due':'date', 'action':'type', 'description':'Comment'})
                # group[['due', 'id', 'created', 'action', 'title', 'description' ]]
                plans[name] = group.to_json(orient='records')
                # b = ast.literal_eval(a)

            a = actions.getActionsGroupedByPlan(dbname, account=account)

            # if account != 'all':
            for acc in plans.keys():
                plans_ = json.loads(plans[acc])
                # import ast
                # plans_ = ast.literal_eval(plans[acc])
                # for v in plans_:
                for i in range(len(plans_)):
                    plan_id = plans_[i]['id']
                    if a != []:
                        if plan_id in a.keys():
                            plans_[i]['actions_id'] = a[plan_id]
                        else:
                            plans_[i]['actions_id'] = "[]"
                    else:
                        plans_[i]['actions_id'] = "[]"

                plans[acc] = plans_

        except Exception as e:
            logger.error("getPlans Error {}".format(e), extra={'type': 'Plans'})
            plans = {}

    except Exception as e:
        logger.error("getPlans Error {}".format(e), extra={'type': 'Plans'})

        plans = {}

    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. Contact your administrator."

    return plans


def get_plans(dbname='username', account='all', group_id=0, user_id=0, username=""):
    ''' Reads plans' database, manipulate the data and returns it.
    '''
    if username == 'admin':
        username = ''
        user_id = 0
        group_id = 0

    try:
        datadb = "data_" + dbname
        mysql_connection = connection.MySQLConnection(datadb)

        con = mysql_connection.connect()

        cur = con.cursor()

        if account != 'all':
            account_id = account

        if user_id == 0 and username != "":
            script = "\
                SELECT id FROM users WHERE username = '{}'\
                ".format(username)
            cur.execute(script)
            con.commit()
            user_id = np.ravel(np.asarray(cur.fetchall()))[0]

        if group_id == -1:
            try:
                group_id = getGroupsPerUser(dbname, username=username, user_id=user_id)[user_id]
            except:
                group_id = "(-1)"

            try:
                group_id = ''.join(str(group_id))[1:-1]
            except:
                pass
        if account == 'all' and group_id == 0 and user_id == 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from data_{}.plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                ".format(dbname, 'data_' + dbname)

        elif account == 'all' and group_id != 0 and user_id == 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from data_{}.plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.group_id IN ({})\
                ".format(dbname, 'data_' + dbname, group_id)

        elif account == 'all' and group_id == 0 and user_id != 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from data_{}.plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.owner_id = '{}'\
                ".format(dbname, 'data_' + dbname, user_id)

        elif account == 'all' and group_id != 0 and user_id != 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from data_{}.plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.group_id IN ({}) OR p.owner_id = '{}'\
                ".format(dbname, 'data_' + dbname, group_id, user_id)

        elif account != 'all' and group_id != 0 and user_id == 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from data_{}.plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.account = '{}' and p.group_id IN ({})\
                ".format(dbname, 'data_' + dbname, account_id, group_id)

        elif account != 'all' and group_id != 0 and user_id != 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from data_{}.plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.account = '{}' AND (p.group_id IN ({}) OR p.owner_id = '{}')\
                ".format(dbname, 'data_' + dbname, account_id, group_id, user_id)

        elif account != 'all' and group_id == 0 and user_id != 0:
            # else:
            script = "\
                SELECT p.*, c.name AS 'account_name' from data_{}.plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.account = '{}' and p.owner_id = '{}'\
                ".format(dbname, 'data_' + dbname, account_id, user_id)

        elif account != 'all' and group_id == 0 and user_id == 0:
            script = "\
                SELECT p.*, c.name AS 'account_name' from data_{}.plans AS p\
                LEFT JOIN {}.customers AS c ON c.id=p.account\
                WHERE p.account = '{}'\
                ".format(dbname, 'data_' + dbname, account_id, user_id)

        cur.execute(script)
        data = np.asarray(cur.fetchall())

        cols = [desc[0] for desc in cur.description]
        try:
            df = pd.DataFrame(data, columns=cols)

            s = lambda x: x.encode('latin-1').decode('cp1252')
            df['description'] = df['description'].apply(s)
            df['name'] = df['name'].apply(s)

            df['account_id'] = df['account']
            df['account'] = df['account_name']
            df.drop('account_name', inplace=True, axis=1)
            df['account'].replace('None', 'Missing account', inplace=True)
            df['account'].fillna('Missing account', inplace=True)
            df['account'] = df['account'].apply(s)

            # f = lambda x: x.isoformat().split("T")[0]
            f = lambda x: x.isoformat().replace("T", " ")
            try:
                df['due'] = df['due'].apply(f)
            except:
                pass
            try:
                df['created'] = df['created'].apply(f)
            except:
                pass

            grouped = df.groupby('account_id')

            plans = dict()
            for name, group in grouped:
                # group = group.rename(columns={'due':'date', 'action':'type', 'description':'Comment'})
                # group[['due', 'id', 'created', 'action', 'title', 'description' ]]
                plans[name] = json.loads(group.to_json(orient='records'))
                # b = ast.literal_eval(a)

            a = actions.getActionsGroupedByPlan(dbname, account=account)

            # if account != 'all':

            for acc in plans.keys():
                # plans_ = json.loads(plans[acc])
                plans_ = plans[acc]
                # import ast
                # plans_ = ast.literal_eval(plans[acc])
                # for v in plans_:
                for i in range(len(plans_)):
                    plan_id = plans_[i]['id']
                    if a != []:
                        if plan_id in a.keys():
                            plans_[i]['actions_id'] = a[plan_id]
                        else:
                            plans_[i]['actions_id'] = "[]"
                    else:
                        plans_[i]['actions_id'] = "[]"

                # plans_ = json.dumps(plans_)
                plans[acc] = plans_

        except Exception as e:
            plans = {}
            # raise


    # except mysql.Error as e:
    except Exception as e:
        # print "Error %d: %s" % (e.args[0],e.args[1])
        # sys.exit(1)
        plans = {}
        # raise

    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. Contact your administrator."

    return plans


def getPlansPerAction(dbname='username', account='all'):
    '''
    '''

    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        account = unquote_plus(account)
        try:
            account = account.decode('utf-8')
        except:
            pass
        account = account.encode('cp1252')

        if account == 'all':

            script = "\
                SELECT plans.id, tasks.id\
                FROM (Plans_Actions\
                LEFT JOIN plans\
                ON Plans_Actions.plan_id=plans.id)\
                LEFT JOIN tasks\
                ON Plans_Actions.task_id=tasks.id\
                "

            cur.execute(script)
            data = np.asarray(cur.fetchall())

        else:
            if account != "":
                script = "SELECT id FROM {}.customers WHERE name = '{}'".format('data_' + dbname, account)
                cur.execute(script)
                con.commit()
                account_id = np.ravel(np.asarray(cur.fetchall()))[0]

            script = "\
                SELECT plans.id, tasks.id\
                FROM (Plans_Actions\
                LEFT JOIN plans\
                ON Plans_Actions.plan_id=plans.id)\
                LEFT JOIN tasks\
                ON Plans_Actions.task_id=tasks.id\
                WHERE plans.account='{}';\
                ".format(account_id)

            cur.execute(script)
            data = np.asarray(cur.fetchall())

        try:
            df = pd.DataFrame(data, columns=['plan_id', 'task_id'])
            grouped = df.groupby('task_id')

            plans = {}
            for name, group in grouped:
                plans[name] = group['plan_id'].to_json(orient='records')
        except:
            plans = []

    except mysql.Error as e:
        import traceback
        print(traceback.format_exc())
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        plans = e.args[1]
        return plans

    finally:
        try:
            if con:
                con.close()
        except:
            return "DB connection failed."

    return plans


def linkPlanToAction(dbname, plan_id, task_id):
    '''
    '''

    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        script = "\
            INSERT INTO Plans_Actions (plan_id, task_id) VALUES({},{});\
            ".format(int(plan_id), int(task_id))

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

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        # data = e.args[1]
        data = {}
        data = 'Error'

    finally:
        if con:
            con.close()

    return data


def unlinkPlanFromAction(dbname, plan_id, task_id):
    '''
    '''

    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        script = "\
            DELETE FROM Plans_Actions WHERE plan_id={} AND task_id={};\
            ".format(int(plan_id), int(task_id))

        cur.execute(script)
        con.commit()
        data = np.asarray(cur.fetchall())

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        data = e.args[1]

    finally:
        if con:
            con.close()

    return data


def plansToActions(dbname='username', account='all'):
    '''
    '''

    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        account = unquote_plus(account)
        try:
            account = account.decode('utf-8')
        except:
            pass
        account = account.encode('cp1252')

        if account == 'all':
            try:
                script = "\
                    SELECT plans.id, tasks.id\
                    FROM (Plans_Actions\
                    LEFT JOIN plans\
                    ON Plans_Actions.plan_id=plans.id)\
                    LEFT JOIN tasks\
                    ON Plans_Actions.task_id=tasks.id\
                    "
                cur.execute(script)
                plans = np.asarray(cur.fetchall())

            except mysql.Error as e:
                logger.debug("Error {}: {}".format(e.args[0], e.args[1]))

        else:
            try:
                script = "\
                    SELECT id FROM {}.customers WHERE name = '{}'\
                    ".format('data_' + dbname, account)
                cur.execute(script)
                con.commit()
                account_id = np.ravel(np.asarray(cur.fetchall()))[0]

                script = "\
                    SELECT plans.id, tasks.id\
                    FROM (Plans_Actions\
                    LEFT JOIN plans\
                    ON Plans_Actions.plan_id=plans.id)\
                    LEFT JOIN tasks\
                    ON Plans_Actions.task_id=tasks.id\
                    WHERE plans.account='{}';\
                    ".format(account_id)

                cur.execute(script)
                plans = np.asarray(cur.fetchall())
                return plans
            except mysql.Error as e:
                logger.debug("Error {}: {}".format(e.args[0], e.args[1]))


    except mysql.Error as e:
        # print "Error %d: %s" % (e.args[0],e.args[1])
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        plans = e.args[1]
        return plans

    finally:
        try:
            if con:
                con.close()
        except:
            return "DB connection failed."


if __name__ == "__main__":
    created = str(datetime.datetime.now())

    plan = {}
    plan['name'] = "Plan B"
    plan['description'] = "Plan A description"
    plan['due'] = created
    plan['account'] = "Klinikum Kalsburg"
    plan['account'] = "Hufeland Klinikum"
    plan['account'] = "Acrion Solutions"
    plan['account'] = "Diotimus AG"
    plan['goal'] = 300000
    plan['chances'] = 0
    plan['status'] = ""
    plan['action'] = ""
    plan['calls'] = 20
    plan['visits'] = 10
    plan['offers'] = 8
    plan['hot'] = True

    local = True
    local = False
    username = 'martinmasip'
    username = 'crmtest1'
    username = 'coldjet_qy'
    username = 'qy___test_com'
    # dbname = 'data_{}'.format(username)
    # createPlan(dbname, plan, local=local)
    # plans = getPlansPerAction(dbname, local=local)
    # plans = getPlans(dbname, account="Herz-Zentrum Landau", group_id=-1, user_id=0, username='sapo_pepe', local=local)

    username = 'alice__qymatix___solutions_com'
    dbname = 'qymatix___solutions_com'

    # username = 'ep__mtm___ne_de'
    # dbname = 'mtm___ne_de'
    username = 'martin_masip__qymatix_de'
    username = 'admin'
    dbname = 'qymatix_de'
    username = 'chancho_babe__qymatix_best'
    dbname = 'qymatix_best'

    # createPlan('data_' + dbname, plan,username=username, local=local)
    account = 'HH'
    # account = 'Diotimus AG'
    # account = 'A100 Row Gmbh'
    account = 'all'
    # account = 38
    # account = 170
    username = 'admin'
    # username = 'chancho_babe__qymatix_best'
    dbname = 'qymatix_best'

    # for p in plans.keys():
    # if 'Deut' in p:
    ##print(json.loads(plans[p])[0]['description'].encode('latin-1').decode('cp1252'))
    # print(json.loads(plans[p])[0]['description'])
    # print(plans[p])

    plan = {"name": "d", "description": "DD", "account": "Xeniades", "goal": "50000", "status": "Solution%20Specified",
            "chances": "2", "due": "2017-10-19 16:00:00", "action": 0, "visits": 0, "offers": 0, "calls": 0,
            "group_id": 18}
    plan = {"id": 73, "name": "d", "description": "DD", "account": "Xeniades", "goal": "50000",
            "status": "Solution%20Specified", "chances": "2", "due": "2017-10-19 16:00:00", "action": 0, "visits": 0,
            "offers": 0, "calls": 0, "group_id": 18}
    plan = {'status': 'Solution Specified', 'account': 'Xeniades', 'goal': 50000, 'chances': 2, 'description': 'DDE',
            'due': '2017-10-19 16:00:00', 'id': 73, 'name': 'DD'}
    # setPlan('data_' + dbname, plan)
    # createPlan('data_' + dbname, plan, username=username, local=local)
    # plans = getPlans(dbname, account=account, group_id=-1, user_id=0, username=username, local=local)
    plans = get_plans(dbname, account=account, group_id=-1, user_id=0, username=username, local=local)
    print(plans)
