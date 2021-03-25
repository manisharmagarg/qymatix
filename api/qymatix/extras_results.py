import sys

import MySQLdb as mdb
import numpy as np

# import colortables
from api.infrastructure.mysql import connection


def getResultsTest():
    ''' TEST - Reads result's database, manipulate the data and returns it.
    '''

    try:
        datadb = 'data_username'
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()

        cur = con.cursor()

        script_nop = "\
            SELECT customers.name,\
            COUNT(sales.product_id) AS NumberOfProducts FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            GROUP BY customers.name;\
            "
        cur.execute(script_nop)
        data_nop = cur.fetchall()

        script_sales = "\
            SELECT customers.name,\
            SUM(sales.price) AS NumberOfProducts FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            GROUP BY customers.name;\
            "
        cur.execute(script_sales)
        data_sales = cur.fetchall()

        names = [n for n in zip(*data_sales)[0]]
        sales = np.around(0.001 * np.asarray([float(r) for r in zip(*data_sales)[1]]), 2)
        K_size = 0.5 * np.asarray([float(r) for r in zip(*data_nop)[1]])
        risk = np.around(sales / K_size, 2)
        margin = np.around(0.1 * risk, 2)
        ccbm = 0.1 * sales
        ppb = np.gradient(sales)

        results = {
            'name': names,
            'sales': sales.tolist(),
            'K_size': K_size.tolist(),
            'risk': risk.tolist(),
            'margin': margin.tolist(),
            'PPB': ppb.tolist(),
            'CCBM': ccbm.tolist(),
        }

        # print(results)

    except mdb.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    finally:
        if con:
            con.close()

    return results


def getProductInfo():
    ''' Reads user's database, manipulate the data and returns it.
    '''

    try:
        datadb = 'data_username'
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()

        cur = con.cursor()

        script_nop = "\
            SELECT customers.name,\
            COUNT(sales.product_id) AS NumberOfProducts FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            GROUP BY customers.name;\
            "
        cur.execute(script_nop)
        data_nop = cur.fetchall()

        script_sales = "\
            SELECT customers.name,\
            SUM(sales.price) AS NumberOfProducts FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            GROUP BY customers.name;\
            "
        cur.execute(script_sales)
        data_sales = cur.fetchall()

        script_prods = "\
            SELECT products.name, customers.name,\
            COUNT(sales.product_id) AS NumberOfOrders\
            FROM ((sales\
            INNER JOIN products\
            ON sales.product_id=products.id)\
            INNER JOIN customers\
            ON sales.customer_id=customers.id)\
            GROUP BY products.name,customers.name;\
            "
        cur.execute(script_prods)

        data_prods = np.asarray(cur.fetchall())
        results = dict()
        results['product'] = data_prods[:, 0].tolist()
        results['customer'] = data_prods[:, 1].tolist()
        results['count'] = data_prods[:, 2].tolist()

        # print(results)

    except Exception as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    finally:
        if con:
            con.close()

    return results


def getResults(username='username', raw=False, account='all'):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    print(username)
    # username = 'username'
    resultsdb = 'results_{}'.format(username)

    try:
        mysql_connection = connection.MySQLConnection(resultsdb)
        con = mysql_connection.connect()

        cur = con.cursor()

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

            values[values == -np.inf] = 0
            results[c] = values.tolist()

    except Exception as e:
        print("Error {0}: {1}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        results = {}
    finally:
        if con:
            con.close()

    return results


def getResultsRoadmap(username='username', func="CCBM", raw=False):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    print(username)
    # username = 'username'
    resultsdb = 'results_{}'.format(username)

    try:
        mysql_connection = connection.MySQLConnection(resultsdb)
        con = mysql_connection.connect()

        cur = con.cursor()

        script_nop = "\
            SELECT * from {};\
            ".format(func)

        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())

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
            AND `TABLE_NAME`='{}';\
            ".format(username, func)
        # show columns from customers;\

        cur.execute(script_nop)
        cols = np.ravel(np.asarray(cur.fetchall()))

        results = dict()
        results[func] = dict()
        for c in cols:
            values = np.ravel(data[:, np.where(cols == c)])
            if not raw:
                if c not in ['Customer', 'customer']:
                    values = values.astype(np.float)
                    values = np.around(np.nan_to_num(values), 2)
                # if c == 'risk':
                ##values = colortables.convertToColor(values)
                # values = colortables.colorK1(values, 'json')

            results[func][c] = values.tolist()

    except Exception as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    finally:
        if con:
            con.close()

    return results


def getResultsHist(username='username', customer=None, param='price', yearMin=None, yearMax=2014):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    if yearMin > yearMax:
        yearMax_ = yearMin
        yearMax = yearMin
        yearMin = yearMax_

    if yearMin == None:
        yearMin = yearMax

    datadb = 'data_{}'.format(username)
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()

        cur = con.cursor()

        script_sales = "\
            SELECT customers.name, sales.month,\
            SUM(sales.{}) AS NumberOfProducts FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.name = '{}' AND sales.year BETWEEN {} AND {}\
            GROUP BY sales.month;\
            ".format(param, customer, yearMin, yearMax)
        # GROUP BY customers.name;\
        cur.execute(script_sales)
        # data = cur.fetchall()

        cols = np.asarray(cur.fetchall())
        # print(cols)

        # month = ['Jan', 'Feb', 'Mar', 'Apr', 'Mar', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month = range(1, 13)
        _months = []

        results = []
        for i in range(12):
            results += [{'frequency': 0.0, 'letter': i + 1}]

        for c in cols:
            _results = dict()
            _results['frequency'] = float(c[2])
            _results['letter'] = int(c[1])
            _months.append(month[int(c[1]) - 1])
            # _months.append(month[int(c[1]) - 1])
            # _results['letter'] = str(month[int(c[1]) - 1])
            # _months.append(str(month[int(c[1]) - 1]))

            results[int(c[1]) - 1] = _results
            # results.append(_results)
            # print(_results)

        # print("XXXX")
        # print(results)

        # _r = []
        # for m in list(set(month) - set(_months)):
        # _r.append({'frequency': 0.0, 'letter': m})
        # results += _r

    except Exception as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        # sys.exit(1)
        results = {}

    finally:
        if con:
            con.close()

    return results


def saveData(data, filename):
    '''
    '''
    f = open(filename, 'w')
    f.write(data)
    f.close()
    print("Data saved to: {}".format(filename))


def getCustomersList(username):
    '''
    '''
    datadb = 'data_{}'.format(username)
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()

        cur = con.cursor()

        script_nop = "\
            SELECT name FROM customers\
            "
        cur.execute(script_nop)

        custlist = np.asarray(cur.fetchall()).reshape(-1)
        # results = dict()
        # results['customers'] = custlist.tolist()
        results = custlist.tolist()

    except Exception as e:
        # print "Error %d: %s" % (e.args[0],e.args[1])
        # sys.exit(1)
        results = []

    finally:
        if con:
            con.close()

    return results


def getCustomers(username, account='all'):
    '''
    '''
    datadb = 'data_{}'.format(username)
    tasksdb = 'data_{}'.format(username)
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()

        cur = con.cursor()

        if account == 'all':

            script_nop = "\
                select c.*, u.name as 'kam' from {0}.customers as c\
                left join {1}.Users_Customers as uc on c.id = uc.customer_id\
                left join {1}.users as u on uc.user_id = u.id\
                ".format(datadb, tasksdb)

            # script_nop = "\
            # SELECT * FROM customers\
            # "
        else:
            # SELECT name, address, city, postcode, country FROM customers\
            # script_nop = "\
            # SELECT * FROM customers\
            # WHERE name = '{}'\
            # ".format(account)
            script_nop = "\
                select c.*, u.name as 'kam' from {0}.customers as c\
                left join {1}.Users_Customers as uc on c.id = uc.customer_id\
                left join {1}.users as u on uc.user_id = u.id\
                where c.name = '{2}'\
                ".format(datadb, tasksdb, account)

        cur.execute(script_nop)

        custlist = np.asarray(cur.fetchall()).reshape(-1)
        custlist = custlist.reshape(len(custlist) / 14, 14)

        results = dict()
        results['customer_id'] = custlist[:, 0].tolist()
        results['customer'] = custlist[:, 1].tolist()
        results['address'] = custlist[:, 2].tolist()
        results['postcode'] = custlist[:, 3].tolist()
        results['city'] = custlist[:, 4].tolist()
        results['country'] = custlist[:, 5].tolist()
        results['revenue'] = custlist[:, 6].tolist()
        results['employees'] = custlist[:, 7].tolist()
        results['industry'] = custlist[:, 8].tolist()
        results['classification'] = custlist[:, 9].tolist()
        results['website'] = custlist[:, 10].tolist()
        results['comment'] = custlist[:, 11].tolist()
        results['favorite'] = custlist[:, 12].tolist()
        results['kam'] = custlist[:, 13].tolist()
        results['telephone'] = custlist[:, 14].tolist()

    except Exception as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        results = []
        # raise

    finally:
        if con:
            con.close()

    return results


if __name__ == '__main__':
    # results = getResults()
    # results = getResultsHist('Acrion  AG', y)
    # results = getResultsHist(username='LGuerraz_data_reducedL_22_xlsx',
    # customer='Acrion  AG',\
    # param='price',\
    ##yearMin=2008,\
    # yearMax=2008)

    # results = getResults(raw=False)
    # results = getResultsRoadmap(username="yoyo_data_reduced_xlsx", func="CCPM")

    # results = getProductInfo()
    # print(results)

    # results = getCustomersList(username="yoyo_data_reduced_xlsx")
    # results = getCustomers(username="test")
    name = None
    name = 'Acrion'
    name = 'all'
    results = getCustomers(username="martin_masip_data_test_1_xlsx", account=name)
    print(results)

    # import json
    # data = json.dumps(results)

    # filename = '/home/martin/Data/products_customers.json'
    # saveData(data, filename)
