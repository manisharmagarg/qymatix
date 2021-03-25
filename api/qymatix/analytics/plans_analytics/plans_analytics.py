import datetime
import sys

import numpy as np
import pandas as pd

from api.infrastructure.mysql import connection


def analyzePlans(dbname, groupby='customer_id', raw=False, account='all', local=False, cur=None):
    '''
    '''
    sys.stdout.write("Analysing plans...\r")
    sys.stdout.write(dbname + "\r")

    try:
        if cur == None:
            datadb = 'data_{}'.format(dbname)
            mysql_connection = connection.MySQLConnection(datadb)
            con = mysql_connection.connect()
            cur = con.cursor()

        try:
            script = "\
                SELECT p.*, cr.ccbm FROM plans AS p\
                LEFT JOIN {}.critters AS cr ON p.id=cr.name\
            ".format('results_' + dbname)
        except:
            script = "\
                SELECT p.* FROM plans AS p\
            "

        cur.execute(script)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=cols)
        df['account'] = df['account'].astype(int)
        df['chances'] = df['chances'].astype(float)
        try:
            df['ccbm'] = df['ccbm'].astype(float)
        except:
            df['ccbm'] = 0.8

        df['action'] = df['action'].astype(str)

        c1 = df['action'] != 'stop'
        c2 = ~df['status'].str.contains('Closed')
        meanGoal = df['goal'].mean()
        stdGoal = df['goal'].std()
        c3 = (df['goal'] >= (meanGoal - stdGoal)) & (df['goal'] < (2 * stdGoal + meanGoal))
        meanChances = df['chances'].mean()
        c4 = df['chances'] >= meanChances

        c5 = df['created'] > datetime.datetime.now() - datetime.timedelta(4 * 30)

        df.loc[c1 & c2 & c3 & c4 & c5, 'hot'] = 1

        sys.stdout.write("Analyzing plans...Done\n")
        return df
    except Exception as e:
        # return None
        # raise
        pass


if __name__ == "__main__":
    username = 'martinmasip'
    local = True
    local = False
    dbname = 'qymatix___solutions_com'
    # username = 'coldjet_qy'
    dbname = 'qymatix___solutions_com'
    dbname = 'qymatix_best'
    dbname = 'qy___test_com'
    # dbname = 'orbusneich_com'
    results = analyzePlans(dbname)
    # print(results)
