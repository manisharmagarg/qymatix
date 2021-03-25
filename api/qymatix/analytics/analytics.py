from urllib.parse import unquote_plus

import numpy as np
import pandas as pd

from api.qymatix.analytics.sales_analytics import sales_analytics
from api.infrastructure.mysql import connection


def getResults(username='username', raw=False, account='all', local=False):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    # username = 'username'
    resultsdb = 'results_{}'.format(username)

    try:
        mysql_connection = connection.MySQLConnection(resultsdb)
        con = mysql_connection.connect()
        cur = con.cursor()

        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')

        # script_nop = "\
        # SELECT * from customers;\
        # "
        if account == 'all':
            script_nop = "\
                SELECT * from critters;\
                "
        else:
            script_nop = "\
                SELECT * from critters\
                WHERE name='{}';\
                ".format(account)

        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())
        # print(data)

        # script_nop = "\
        # SELECT `COLUMN_NAME`\
        # FROM `INFORMATION_SCHEMA`.`COLUMNS`\
        # WHERE `TABLE_SCHEMA`='results_{}'\
        # AND `TABLE_NAME`='customers';\
        # ".format(username)

        script_nop = "\
            SELECT `COLUMN_NAME`\
            FROM `INFORMATION_SCHEMA`.`COLUMNS`\
            WHERE `TABLE_SCHEMA`='results_{}'\
            AND `TABLE_NAME`='critters';\
            ".format(username)
        # show columns from customers;\

        cur.execute(script_nop)
        cols = np.ravel(np.asarray(cur.fetchall()))

        results = dict()
        for c in cols:
            values = np.ravel(data[:, np.where(cols == c)])
            if not raw:
                if c != 'name':
                    values = values.astype(np.float)
                    values = np.around(np.nan_to_num(values), 2)
                # if c == 'ccbm':
                if c == 'risk':
                    results['rawRisk'] = values.tolist()
                    # values = colortables.convertToColor(values)
                    # values = colortables.colorK1(values, 'json')

            results[c] = values.tolist()

    except Exception as e:
        # print("Error {0}: {1}".format(e.args[0], e.args[1]))
        print("XXXX")
        # sys.exit(1)
        results = {}
    finally:
        try:
            con.close()
        except:
            pass

    return results


def results(dbname, groupby='customer_id', account='all'):
    '''
    '''

    print("Running analysis...")
    try:
        cars = sales_analytics.car(username=dbname)

        ppbs = sales_analytics.ppb(username=dbname)

        cars['risk'] = cars['risk'].astype(float)
        cars['risk'] = cars['risk'] * (-1) + 1

        # results = pd.merge(ppbs, cars, how='outer', on='customer_id')
        results = pd.merge(ppbs, cars, on='customer_id')
        results['row_names'] = results.index
        results['customer_id'] = results['customer_id'].astype(int)

        # Association by product_type
        prod_type_cross_selling = sales_analytics.getItemSuggestions(dbname, item='product_type')
        prod_type_cross_selling.rename(columns={'potential_items': 'product_type_cross_selling'}, inplace=True)
        prod_type_cross_selling['customer_id'] = prod_type_cross_selling['customer_id'].astype(int)
        results = pd.merge(results, prod_type_cross_selling, on='customer_id')

        # Association by product
        prod_cross_selling = sales_analytics.getItemSuggestions(dbname, item='product')
        prod_cross_selling.rename(columns={'potential_items': 'product_cross_selling'}, inplace=True)
        prod_cross_selling['customer_id'] = prod_cross_selling['customer_id'].astype(int)
        results = pd.merge(results, prod_cross_selling, on='customer_id')

        print(len(results['customer_id'].unique()))
        print("/////")
        # ddd

        results.rename(columns={'price': 'sales', 'potential_y': 'ccbm'}, inplace=True)
        # print(results.columns)
        results.drop(['item_name_x', 'item_name_y', 'potential_x'], axis=1, inplace=True)

        results['ccbm'] = results['ccbm'] / results['risk']

        results['ccbm'] = results['ccbm'].rank(pct=True)

        results['ccbm'] = results['ccbm'] - results['ccbm'].min()

        print("Running nalysis...Done")

    except:
        raise

    return results


if __name__ == "__main__":
    username = 'martinmasip'
    local = True
    local = False
    dbname = 'qymatix___solutions_com'
    # username = 'coldjet_qy'
    # addResultsTable(username, local=local)
    dbname = 'qymatix___solutions_com'
    dbname = 'qy___test_com'
    dbname = 'qymatix_best'
    # dbname = 'orbusneich_com'
    dbname = 'aet_at'
    dbname = 'qymatix___aet_com'

    results = results(dbname)
    print(results)
