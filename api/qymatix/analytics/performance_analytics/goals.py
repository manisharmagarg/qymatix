import datetime
import json
import logging
import os

import MySQLdb as mysql
import numpy as np
import pandas as pd
from django.conf import settings

from api.infrastructure.mysql import connection


logger = logging.getLogger(__name__)


def createGoal(dbname, data, local=False, lines=None):
    '''
    '''
    if 'name' not in data.keys():
        data['name'] = ''
    if 'user' not in data.keys():
        data['user'] = 'all'
    if 'user_id' not in data.keys():
        data['user_id'] = 1
    if 'description' not in data.keys():
        data['description'] = ''
    if 'country' not in data.keys():
        data['country'] = ''

    try:
        data['name'] = data['name'].decode('utf-8').encode('latin-1')
    except:
        data['name'] = data['name'].encode('latin-1')
    try:
        data['user'] = data['user'].decode('utf-8').encode('latin-1')
    except:
        data['user'] = data['user'].encode('latin-1')
    try:
        data['description'] = data['description'].decode('utf-8').encode('latin-1')
    except:
        data['description'] = data['description'].encode('latin-1')
    try:
        data['country'] = data['country'].decode('utf-8').encode('latin-1')
    except:
        data['country'] = data['country'].encode('latin-1')

    months = (
    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
    'december')
    for month in months:
        if month not in data.keys():
            data[month] = 0

    created = str(datetime.datetime.now())

    datadb = "data_" + dbname
    mysql_connection = connection.MySQLConnection(datadb)
    con = mysql_connection.connect()
    cur = con.cursor()

    try:
        script = "\
            INSERT INTO `goals`\
            (name, user_id, created, description, country, year, january, february, march, april, may, june, july, august, september, october, november, december)\
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');\
            ".format(data['name'], data['user_id'], created, data['description'], data['country'], \
                     data['year'], \
                     data['january'], \
                     data['february'], \
                     data['march'], \
                     data['april'], \
                     data['may'], \
                     data['june'], \
                     data['july'], \
                     data['august'], \
                     data['september'], \
                     data['october'], \
                     data['november'], \
                     data['december'], \
                     )

        cur.execute(script)
        con.commit()

        script = "\
            SELECT MAX(id) from goals;\
            "
        cur.execute(script)
        con.commit()

        goal_id = np.ravel(np.asarray(cur.fetchall()))[0]

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        raise
        if int(e.args[0]) == 1062:
            script = "\
                SELECT id FROM goals WHERE user_id='{}';\
                ".format(data['kam_id'])

            cur.execute(script)
            con.commit()

            goal_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return goal_id

    finally:
        if con:
            con.close()

    return goal_id


def create_goal(cur, data, user_id=0, username='', local=False, lines=None, user=''):
    '''
    '''
    # cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    cur.execute("USE data_{}".format(dbname))

    if 'name' not in data.keys():
        data['name'] = ''
    if 'user' not in data.keys():
        data['user'] = 'all'
    if 'user_id' not in data.keys():
        data['user_id'] = None
    if 'description' not in data.keys():
        data['description'] = ''
    if 'country' not in data.keys():
        data['country'] = ''

    if user_id == 0 and user != "":
        script = "SELECT id FROM users WHERE username = '{}'".format(user)
        cur.execute(script)
        # con.commit()

        try:
            user_id = np.ravel(np.asarray(cur.fetchall()))[0]
        except Exception as e:
            print(e)
            # raise
            print("User {} not found".format(user))
            return

    data['user_id'] = user_id

    try:
        data['name'] = data['name'].decode('utf-8').encode('latin-1')
    except:
        data['name'] = data['name'].encode('latin-1')
    try:
        data['user'] = data['user'].decode('utf-8').encode('latin-1')
    except:
        data['user'] = data['user'].encode('latin-1')
    try:
        data['description'] = data['description'].decode('utf-8').encode('latin-1')
    except:
        data['description'] = data['description'].encode('latin-1')
    try:
        data['country'] = data['country'].decode('utf-8').encode('latin-1')
    except:
        data['country'] = data['country'].encode('latin-1')

    months = (
    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
    'december')
    for month in months:
        if month not in data.keys():
            data[month] = 0

    created = str(datetime.datetime.now())

    try:
        script = "INSERT INTO `goals`(name, user_id, created, description, country, year, january, february, march, april, may, june, july, august, september, october, november, december) VALUES "\
            "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
                    data['name'], 
                    data['user_id'],
                    created, data['description'],
                    data['country'], 
                    data['year'], 
                    data['january'], 
                    data['february'], 
                    data['march'], 
                    data['april'], 
                    data['may'], 
                    data['june'], 
                    data['july'], 
                    data['august'], 
                    data['september'], 
                    data['october'], 
                    data['november'], 
                    data['december'], 

                )

        # print(script)
        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from goals;"
        cur.execute(script)
        con.commit()

        goal_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return goal_id

    except Exception as e:
        import traceback
        print(e)
        # sys.exit(1)
        # raise
        print("User {} not found".format(user))

        return traceback.format_exc()

        # if int(e.args[0]) == 1062:

        # script = "\
        # SELECT id FROM goals WHERE user_id='{}';\
        # ".format(data['kam_id'])

        # cur.execute(script)
        # con.commit()

        # goal_id = np.ravel(np.asarray(cur.fetchall()))[0]

        # return goal_id


def modifyGoal(dbname, data):
    """
    """

    try:
        datadb = "data_" + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        for col in data.keys():
            if col not in ('id', 'goal_id', 'created'):
                value = data[col]
                if col in ('country', 'description', 'name'):
                    try:
                        value = value.decode('utf-8').encode('latin-1')
                    except:
                        value = value.encode('latin-1')
                goal_id = data['id']
                script = "UPDATE {} SET {}='{}' WHERE id={}".format('goals', col, value, goal_id)
                cur.execute(script)
                con.commit()

        response = data['id']

    # except:
    # raise
    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        response = 'false'

    finally:
        try:
            if con:
                con.close()
                return response
        except:
            return "Problem connecting to the database. Contact your administrator."


def deleteGoal(dbname, goal_id):
    """
    """

    try:
        datadb = "data_" + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        # script = "\
        # DELETE FROM Users_Actions WHERE user_id={};\
        # ".format(int(user_id))
        # cur.execute(script)
        # con.commit()

        # script = "\
        # DELETE FROM Users_Plans WHERE user_id={};\
        # ".format(int(user_id))
        # cur.execute(script)
        # con.commit()

        script = "\
            DELETE FROM goals WHERE id = {}\
            ".format(goal_id)
        cur.execute(script)
        con.commit()
        # data = np.asarray(cur.fetchall())

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        # return e.args[1]


def getGoals(dbname, data={}, groupedby='user_id', raw=False, local=False):
    ''' Reads tasks's database, manipulate the data and returns it.
    '''

    try:
        if 'user' not in data.keys():
            data['user'] = 'all'
        if 'user_id' not in data.keys():
            data['user_id'] = 0
        if 'country' not in data.keys():
            data['country'] = ''
        try:
            data['user'] = data['user'].decode('utf-8').encode('latin-1')
        except:
            data['user'] = data['user'].encode('latin-1')
        try:
            data['country'] = data['country'].decode('utf-8').encode('latin-1')
        except:
            data['country'] = data['country'].encode('latin-1')

        datadb = "data_" + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if data['user_id'] == 0 and data['user'] == 'all':
            if 'year' in data.keys():
                script = "\
                    SELECT * from goals WHERE year='{}';\
                    ".format(data['year'])
            else:
                script = "\
                    SELECT * from goals;\
                    "
        elif data['user'] != 'all':
            script = "\
                SELECT id FROM users WHERE name='{}';\
                ".format(data.get('name'))
            cur.execute(script)
            con.commit()
            data['user_id'] = np.ravel(np.asarray(cur.fetchall()))[0]
        elif data['user_id'] != 0:
            if 'year' in data.keys():
                script = "\
                    SELECT * from goals\
                    WHERE user_id='{}' AND year='{}';\
                    ".format(data['user_id'], data['year'])
            else:
                script = "\
                    SELECT * from goals\
                    WHERE user_id='{}';\
                    ".format(data['user_id'])

        cur.execute(script)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]

        try:
            df = pd.DataFrame(data, columns=cols)

            # f = lambda x: x.isoformat().split("T")[0]
            # df['due'] = df['due'].apply(f)
            f = lambda x: x.isoformat().replace("T", " ")
            df['created'] = df['created'].apply(f)

            grouped = df.groupby(groupedby)

            tasks = {}
            for name, group in grouped:
                # group = group.rename(columns={'due':'date', 'action':'type', 'description':'Comment'})
                # group[['due', 'id', 'created', 'action', 'title', 'description' ]]
                tasks[str(name)] = json.loads(group.to_json(orient='records'))[0]
                # tasks[str(name)] = group.to_json(orient='records')[1:-1]
        except:
            tasks = {}

    except Exception as e:
        # print ("Error %d: %s" % (e.args[0],e.args[1]))
        # sys.exit(1)
        tasks = {}

    finally:
        if con:
            con.close()

    return tasks


def get_goals(con, data={}, groupby='user_id', orient='records', raw=False, local=False):
    ''' Reads tasks's database, manipulate the data and returns it.
    '''
    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    cur.execute("USE data_{}".format(dbname))

    try:
        if 'user' not in data.keys():
            data['user'] = 'all'
        if 'user_id' not in data.keys():
            data['user_id'] = 0
        if 'country' not in data.keys():
            data['country'] = ''
        # try:
        #     data['user'] = data['user'].decode('utf-8').encode('latin-1')
        # except:
        #     data['user'] = data['user'].encode('latin-1')
        # try:
        #     data['country'] = data['country'].decode('utf-8').encode('latin-1')
        # except:
        #     data['country'] = data['country'].encode('latin-1')

        if data['user_id'] == 0 and data['user'] == 'all':
            if 'year' in data.keys():
                script = "\
                    SELECT * from goals WHERE year='{}';\
                    ".format(data['year'])
            else:
                script = "\
                    SELECT * from goals;\
                    "
        elif data['user'] != 'all':
            script = "\
                SELECT id FROM users WHERE name='{}';\
                ".format(data['name'])
            cur.execute(script)
            # con.commit()
            data['user_id'] = np.ravel(np.asarray(cur.fetchall()))[0]
        elif data['user_id'] != 0:
            if 'year' in data.keys():
                script = "\
                    SELECT * from goals\
                    WHERE user_id='{}' AND year='{}';\
                    ".format(data['user_id'], data['year'])
            else:
                script = "\
                    SELECT * from goals\
                    WHERE user_id='{}';\
                    ".format(data['user_id'])

        cur.execute(script)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]

        try:
            df = pd.DataFrame(data, columns=cols)

            # f = lambda x: x.isoformat().split("T")[0]
            # df['due'] = df['due'].apply(f)
            f = lambda x: x.isoformat().replace("T", " ")
            df['created'] = df['created'].apply(f)

            grouped = df.groupby(groupby)

            tasks = {}
            for name, group in grouped:
                # group = group.rename(columns={'due':'date', 'action':'type', 'description':'Comment'})
                # group[['due', 'id', 'created', 'action', 'title', 'description' ]]
                # tasks[str(name)] = json.loads(group.to_json(orient='records'))[0]
                tasks[str(name)] = group.to_dict(orient=orient)
        except:
            tasks = {}
            # raise

    # except mysql.Error as e:
    # print "Error %d: %s" % (e.args[0],e.args[1])
    except Exception as e:
        # sys.exit(1)
        # print(e)
        tasks = {}
        raise

    return tasks


def getGoalsPerQuarter(dbname, data={}, con=None, local=False):
    '''
    '''
    try:

        if 'user' not in data.keys():
            data['user'] = 'all'
        if 'user_id' not in data.keys():
            data['user_id'] = 0
        if 'country' not in data.keys():
            data['country'] = ''

        try:
            data['user'] = data['user'].decode('utf-8').encode('latin-1')
        except:
            data['user'] = data['user'].encode('latin-1')
        try:
            data['country'] = data['country'].decode('utf-8').encode('latin-1')
        except:
            data['country'] = data['country'].encode('latin-1')

        if dbname != None:
            datadb = "data_" + dbname
            mysql_connection = connection.MySQLConnection(datadb)
            con = mysql_connection.connect()
            cur = con.cursor()

        if con == None:
            return "Error"

        cur = con.cursor()

        '''
        script_cols = "\
            SELECT `COLUMN_NAME`\
            FROM `INFORMATION_SCHEMA`.`COLUMNS`\
            WHERE `TABLE_SCHEMA`='{}'\
            AND `TABLE_NAME`='{}';\
            ".format(dbname, 'goals')

        cur.execute(script_cols)
        cols = np.ravel(np.asarray(cur.fetchall()))
        '''

        if data['user_id'] == 0 and data['user'] == 'all':
            if 'year' in data.keys():
                script = "\
                    SELECT * from goals WHERE year='{}';\
                    ".format(data['year'])
            else:
                script = "\
                    SELECT * from goals;\
                    "
        elif data['user'] != 'all':
            script = "\
                SELECT id FROM users WHERE name='{}';\
                ".format(data.get('name'))
            cur.execute(script)
            con.commit()
            data['user_id'] = np.ravel(np.asarray(cur.fetchall()))[0]
        elif data['user_id'] != 0:
            if 'year' in data.keys():
                script = "\
                    SELECT * from goals\
                    WHERE user_id='{}' AND year='{}';\
                    ".format(data['user_id'], data['year'])
            else:
                script = "\
                    SELECT * from goals\
                    WHERE user_id='{}';\
                    ".format(data['user_id'])

        cur.execute(script)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]

        try:
            df = pd.DataFrame(data, columns=cols)

            # f = lambda x: x.isoformat().split("T")[0]
            # df['due'] = df['due'].apply(f)
            f = lambda x: x.isoformat().replace("T", " ")
            df['created'] = df['created'].apply(f)

            grouped = df.groupby('year')

            goals_per_quarter = {}
            for name, group in grouped:
                ##group = group.rename(columns={'due':'date', 'action':'type', 'description':'Comment'})
                ##group[['due', 'id', 'created', 'action', 'title', 'description' ]]
                # tasks[name] = group.to_json(orient='records')
                q1 = group[['january', 'february', 'march']].sum().sum()
                q2 = group[['april', 'may', 'june']].sum().sum()
                q3 = group[['july', 'august', 'september']].sum().sum()
                q4 = group[['october', 'november', 'december']].sum().sum()
                # print(q1)
                # print(q2)
                # print(q3)
                # print(q4)
                goals_per_quarter[name] = [{"1": q1, "2": q2, "3": q3, "4": q4}]

        except:
            goals_per_quarter = {}

    except Exception as e:
        # print ("Error %d: %s" % (e.args[0],e.args[1]))
        # sys.exit(1)
        # tasks = []
        # raise
        goals_per_quarter = {}

    finally:
        if con:
            con.close()

    return goals_per_quarter


def getIdFromName(name):
    dbname = "data_martinmasip_data_test_2015_2016_copy_super_reduced_xlsx"

    local = False

    try:
        datadb = "data_" + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "SELECT id FROM users WHERE name='{}'".format(name)
        cur.execute(script)
        con.commit()

        user_id = np.ravel(np.asarray(cur.fetchall()))[0]
        # print(user_id)

    except mysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        raise


if __name__ == "__main__":
    # getIdFromName('martinmasip')

    dbname = "data_martinmasip_data_test_2015_2016_copy_super_reduced_xlsx"
    dbname = "data_martinmasip"

    username = 'sapo_pepe'
    dbname = "qymatix_best"
    local = False

    # data = {'country': 'Germany', 'year': 2018, 'january':1000, 'march': 4000, 'august':4000, 'november':10000}
    # goal = createGoal(dbname, data)
    # print(goal)

    # data = {'year': 2018}
    # data = {}
    # results = getGoalsPerQuarter(dbname, data)
    # print(results)

    data = {'id': 1, 'january': 2000}
    data = {'id': 1, 'year': 2017}
    # goal_id = modifyGoal(dbname, data)
    data = {'year': 2018, 'country': ''}
    data = {}
    groupedby = 'year'
    goals = getGoals(dbname, data, groupedby=groupedby)
    print(goals)
    print(goals.keys())
