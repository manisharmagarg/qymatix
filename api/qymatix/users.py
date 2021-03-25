import numpy as np
import pandas as pd

from api.infrastructure.mysql import connection


import logging

logger = logging.getLogger(__name__)


def getCustomersPerUser(dbname='username', cur='', username='all', user_id=0, raw=False, local=False):
    '''
    '''

    dbname = dbname.replace('results_', 'data_')

    if "data_" not in dbname:
        dbname = "data_" + dbname


    try:
        if cur == '':
            mysql_connection = connection.MySQLConnection(dbname)
            con = mysql_connection.connect()
            cur = con.cursor()

        if username == 'all' and user_id == 0:

            script = "\
                SELECT {0}.customers.id, {1}.users.id\
                FROM ({1}.Users_Customers\
                LEFT JOIN {0}.customers\
                ON {1}.Users_Customers.customer_id={0}.customers.id)\
                LEFT JOIN {1}.users\
                ON {1}.Users_Customers.user_id=users.id\
                ".format(dbname.replace('data_', 'data_'), dbname)

        elif username != 'all' and user_id == 0:
            script = "\
                SELECT {0}.customers.id, {1}.users.id\
                FROM ({1}.Users_Customers\
                LEFT JOIN {0}.customers\
                ON {1}.Users_Customers.customer_id={0}.customers.id)\
                LEFT JOIN {1}.users\
                ON {1}.Users_Customers.user_id=users.id\
                WHERE {1}.users.username='{2}';\
                ".format(dbname.replace('data_', 'data_'), dbname, username)

        else:
            script = "\
                SELECT {0}.customers.id, {1}.users.id\
                FROM ({1}.Users_Customers\
                LEFT JOIN {0}.customers\
                ON {1}.Users_Customers.customer_id={0}.customers.id)\
                LEFT JOIN {1}.users\
                ON {1}.Users_Customers.user_id=users.id\
                WHERE {1}.users.id='{2}';\
                ".format(dbname.replace('data_', 'data_'), dbname, user_id)

        cur.execute(script)
        data = np.asarray(cur.fetchall())

        try:
            df = pd.DataFrame(data, columns=['customer_id', 'user_id'])
            grouped = df.groupby('user_id')

            groups = {}
            for name, group in grouped:
                groups[name] = group['customer_id'].to_json(orient='records')
        except Exception as e:
            print(e)
            groups = {}
            # raise
            # groups = {'No groups': 2}


    except Exception as e:
        # print("Error {}: {}".format(e.args[0],e.args[1]))
        groups = e.args[1]
        groups = ''
        return groups

    finally:
        try:
            if con:
                con.close()
        except:
            return "DB connection failed."

    return groups


if __name__ == "__main__":
    dbname = 'qymatix_de'
    # groups = getGroups(dbname, username=username, user_id=0)
    # groups = getGroups(dbname, username="chancho_babe", user_id=0)
    # print(groups)
    # addUserToGroup(dbname, 1, 2)
    # addUserToGroup(dbname, 20, 1)
    # addUserToGroup(dbname, 17, 2)

    # username = 'all'
    # customers = getCustomersPerUser(dbname, username=username, user_id=0)
    username = 'all'
    # username = 'paul__qy___test_com'
    user_id = 20
    user_id = 141
    user_id = 0
    dbname = 'qymatix_best'
    username = 'all'

    username = 'philipp__spm_li'
    dbname = 'spm_li'

    customers = getCustomersPerUser(dbname, username=username, user_id=user_id)
    print(customers)
    print(customers[customers.keys()[0]])
