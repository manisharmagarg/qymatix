import json
import sys
from urllib.parse import unquote_plus

import MySQLdb as mdb
import numpy as np
import pandas as pd
from api.qymatix.users import getCustomersPerUser

from api.infrastructure.mysql import connection


def getCustomersIdList(cur, username):
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    cust = getCustomersPerUser(dbname=dbname, username=username)
    cust = cust[next(iter(cust))].replace('[', '(').replace(']', ')')
    return cust


def getResultsTest():
    ''' TEST - Reads result's database, manipulate the data and returns it.
    '''

    try:
        dbname = 'data_username'
        mysql_connection = connection.MySQLConnection(dbname)
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

    except Exception as e:
        "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if con:
            con.close()

    return results


def getProductInfo():
    ''' Reads user's database, manipulate the data and returns it.
    '''

    try:
        dbname = 'data_username'
        mysql_connection = connection.MySQLConnection(dbname)
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
        "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if con:
            con.close()

    return results


def getResults(dbname='username', raw=False, account='all', username=''):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    resultsdb = 'results_{}'.format(dbname)

    try:
        mysql_connection = connection.MySQLConnection(resultsdb)
        con = mysql_connection.connect()
        cur = con.cursor()

        '''
        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
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
            account_id = int(account)

        if account == 'all':

            if username in ['', 'admin']:
                script_nop = "\
                    SELECT cr.*, c.name AS 'account' FROM critters AS cr\
                    LEFT JOIN {}.customers AS c ON cr.name=c.id\
                    ".format('data_' + dbname)
            else:
                cust = getCustomersIdList(cur, username)
                script_nop = "\
                    SELECT cr.*, c.name AS 'account' from critters AS cr\
                    LEFT JOIN {}.customers AS c ON cr.name=c.id\
                    WHERE cr.name IN {};\
                    ".format('data_' + dbname, cust)

        else:
            script_nop = "\
                SELECT cr.*, c.name AS 'account' from critters AS cr\
                LEFT JOIN {}.customers AS c ON cr.name=c.id\
                WHERE cr.id='{}';\
                ".format('data_' + dbname, account_id)

        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]

        results = dict()
        # for c in cols:
        for i in range(len(cols)):
            # values = np.ravel(data[:, np.where(cols==c)])
            values = np.ravel(data[:, i])
            c = cols[i]
            # print(values)
            if not raw:
                if c not in ('account', 'name', 'product_cross_selling', 'product_type_cross_selling'):
                    values = values.astype(np.float)
                    values = np.around(np.nan_to_num(values), 2)
                if c == 'account':
                    results['name'] = values.tolist()
                if c == 'risk':
                    results['rawRisk'] = values.tolist()
                    # values = colortables.convertToColor(values)
                    # values = colortables.colorK1(values, 'json')

            values[values == -np.inf] = 0
            results[c] = values.tolist()
        results.pop('account', None)

    except Exception as e:
        print(e)
        results = {}
        # raise

    finally:
        try:
            con.close()
        except:
            pass

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
        # print "Error %d: %s" % (e.args[0],e.args[1])
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
        # print "Error %d: %s" % (e.args[0],e.args[1])
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


def getCustomersList(dbname, username=''):
    '''
    '''
    datadb = 'data_{}'.format(dbname)
    tasksdb = 'data_{}'.format(dbname)
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if username in ['', 'admin']:
            script = "\
                SELECT name FROM customers\
                "
        else:
            cust = getCustomersIdList(cur, username)
            script = "\
                SELECT c.name FROM {0}.customers AS c\
                LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                WHERE c.id IN {2}\
                ".format(datadb, tasksdb, cust)

        cur.execute(script)
        custlist = np.asarray(cur.fetchall()).reshape(-1)
        # results = dict()
        # results['customers'] = custlist.tolist()
        results = custlist.tolist()

    except Exception as e:
        print
        "Error %d: %s" % (e.args[0], e.args[1])
        # sys.exit(1)
        results = {}

    finally:
        try:
            con.close()
        except:
            pass

    return results


def getCustomers(dbname, account='all', username=''):
    '''
    '''
    datadb = 'data_{}'.format(dbname)
    tasksdb = 'data_{}'.format(dbname)
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')

        if account == 'all':

            if username in ['', 'admin']:
                script_nop = "\
                    select c.*, u.name as 'kam' from {0}.customers as c\
                    left join {1}.Users_Customers as uc on c.id = uc.customer_id\
                    left join {1}.users as u on uc.user_id = u.id\
                    ".format(datadb, tasksdb)
            else:
                cust = getCustomersIdList(cur, username)
                script_nop = "\
                    select c.*, u.name as 'kam' from {0}.customers as c\
                    left join {1}.Users_Customers as uc on c.id = uc.customer_id\
                    left join {1}.users as u on uc.user_id = u.id\
                    where c.id IN {2}\
                    ".format(datadb, tasksdb, cust)

        else:
            script_nop = "\
                select c.*, u.name as 'kam' from {0}.customers as c\
                left join {1}.Users_Customers as uc on c.id = uc.customer_id\
                left join {1}.users as u on uc.user_id = u.id\
                where c.id = '{2}';\
                ".format(datadb, tasksdb, account)

        cur.execute(script_nop)

        custlist = np.asarray(cur.fetchall()).reshape(-1)
        custlist = custlist.reshape(len(custlist) / 14, 14)

        results = dict()
        results['customer_id'] = custlist[:, 0].tolist()
        results['customer'] = custlist[:, 1].tolist()
        # print([unicode(r.decode('latin-1')).encode('utf-8') for r in results['customer']])
        # print([r.encode('cp1252') for r in results['customer']])
        # results['customer'] = [r for r in results['customer']]
        # results['customer'] = [r.replace('\\\\', '\\') for r in results['customer']]
        # results['customer'] = [r.replace('\\\\', '\\').decode('latin-1') for r in results['customer']]
        # print(results['customer'])
        # print("<<<<<")
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

        for x in range(len(results['customer'])):
            for k in ('customer', 'address', 'country', 'city', 'comment', 'kam'):
                if results[k][x] != None:
                    results[k][x] = results[k][x].encode('latin-1').decode('cp1252')
                else:
                    results[k][x] = ""

    # except Exception as e:
    # print "Error %d: %s" % (e.args[0],e.args[1])
    except Exception as e:
        print(e)
        results = []
        # raise

    finally:
        try:
            con.close()
        except:
            pass

    return results


def get_customers(dbname, account='all', username=''):
    '''
    '''
    datadb = 'data_{}'.format(dbname)
    tasksdb = 'data_{}'.format(dbname)
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')

        if account == 'all':
            if username in ['', 'admin']:
                script_nop = "\
                    SELECT c.*, u.name AS 'kam', cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                    LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                    LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                    LEFT JOIN {2}.critters AS cr ON cr.name = c.id\
                    ".format(datadb, tasksdb, tasksdb.replace('data_', 'results_'))
            else:
                cust = getCustomersIdList(cur, username)
                script_nop = "\
                    SELECT c.*, u.name AS 'kam', cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                    LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                    LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                    LEFT JOIN {3}.critters AS cr ON cr.name = c.id\
                    WHERE c.id IN {2}\
                    ".format(datadb, tasksdb, cust, tasksdb.replace('data_', 'results_'))
        else:
            script_nop = "\
                SELECT c.*, u.name AS 'kam', cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                LEFT JOIN {3}.critters AS cr ON cr.name = c.id\
                WHERE c.id = '{2}';\
                ".format(datadb, tasksdb, account, tasksdb.replace('data_', 'results_'))

        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]

        try:
            df = pd.DataFrame(data, columns=cols)
            for c in ('sales', 'margin', 'risk', 'ppb', 'ccbm'):
                df[c] = df[c].apply(pd.to_numeric, errors='')
                df['s' + c] = df[c] / df[c].max()
            # df.drop(df.columns[[14, 15]], inplace=True, axis=1)
            # df.drop(df.columns(np.argwhere(df.columns.duplicated())[0]), inplace=True, axis=1)

            # s = lambda x: x.encode('latin-1').decode('cp1252')
            # df['description'] = df['description'].apply(s)
            # df['account'] = df['account_name']
            # df.drop('account_name', inplace=True, axis=1)
            # df['account'].replace('None', 'Missing account', inplace=True)
            # df['account'].fillna('Missing account', inplace=True)
            # df['account'] = df['account'].apply(s)

            grouped = df.groupby('id')

            customers = {}
            for name, group in grouped:
                # group = group.rename(columns={'due':'due', 'action':'type', 'description':'comment', 'plan':'plan_id'})
                # group[['due', 'id', 'created', 'action', 'title', 'description' ]]
                customers[int(name)] = json.loads(group.to_json(orient='records'))[0]
                # customers[int(name)] = group.to_json(orient='records')

            for k in customers.keys():
                scales = []
                for c in ('sales', 'margin', 'risk', 'ppb', 'ccbm'):
                    try:
                        value = np.around(customers[k]['s' + c], 2)
                    except:
                        value = 'null'
                    scales.append({'y': value, 'value': value, 'label': value})
                customers[k]['scales'] = scales

        except Exception as e:
            print(e)
            customers = {}
            # pass
            # raise
    except:
        # pass
        raise

    return customers


def max_values(cur, username=''):
    '''
    '''
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    cur.execute("use results_{}".format(dbname))

    if username in ['', 'admin']:
        script_nop = "\
            SELECT MAX(ccbm) AS max_ccbm, MAX(ppb) AS max_ppb, MAX(risk) AS max_risk FROM critters\
            GROUP BY name\
            "
        # WHERE YEAR(sales.date)=2017\
    else:
        cust = getCustomersList(cur, username)
        script_nop = "\
            SELECT MAX(ccbm) AS max_ccbm, MAX(ppb) AS max_ppb, MAX(risk) AS max_risk FROM critters\
            WHERE name IN {}\
            GROUP BY name\
            ".format(cust)
        # WHERE YEAR(sales.date)=2017 AND customer_id IN {}\

    cur.execute(script_nop)
    _data = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    values = {}
    try:
        values[cols[0]] = float(_data[0][0])
    except:
        values[cols[0]] = _data[0][0]
    try:
        values[cols[1]] = float(_data[0][1])
    except:
        values[cols[1]] = _data[0][1]
    try:
        values[cols[2]] = float(_data[0][2])
    except:
        values[cols[2]] = _data[0][2]
    # print(min_values)

    return values
    # d = [i[0] for i in _data]
    # return d


def min_values(cur, username=''):
    '''
    '''
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    cur.execute("use results_{}".format(dbname))

    if username in ['', 'admin']:
        script_nop = "\
            SELECT MIN(ccbm) AS min_ccbm, MIN(ppb) AS min_ppb, MIN(risk) AS min_risk FROM critters\
            GROUP BY name\
            "
        # WHERE YEAR(sales.date)=2017\
    else:
        cust = getCustomersList(cur, username)
        script_nop = "\
            SELECT MIN(ccbm) AS min_ccbm, MIN(ppb) AS min_ppb, MIN(risk) AS min_risk FROM critters\
            WHERE name IN {}\
            GROUP BY name\
            ".format(cust)
        # WHERE YEAR(sales.date)=2017 AND customer_id IN {}\

    cur.execute(script_nop)
    _data = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    values = {}
    try:
        values[cols[0]] = float(_data[0][0])
    except:
        values[cols[0]] = _data[0][0]
    try:
        values[cols[1]] = float(_data[0][1])
    except:
        values[cols[1]] = _data[0][1]
    try:
        values[cols[2]] = float(_data[0][2])
    except:
        values[cols[2]] = _data[0][2]
    # print(min_values)

    return values


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
    account = 'all'

    # username = 'ep__mtm___ne_de'
    # dbname = 'mtm___ne_de'

    # results = getCustomers(username="martin_masip_data_test_1_xlsx", account=name)
    # results = getCustomers(username="qymatix_best", account=name)
    # results = getCustomers(username=dbname, account=account)
    # results = getCustomers(username="coldjet_qy", account=name)
    # dbname = "coldjet_qy"
    dbname = "qy___test_com"
    dbname = "qymatix_de"
    username = ''
    username = 'lucas_pedretti__qymatix_de'
    dbname = "qymatix_best"
    username = 'admin'
    username = 'chancho_babe__qymatix_best'
    # results = getResults(dbname=dbname, account=account, username=username)
    # print(results)
    # results = getCustomers(dbname=dbname, account=account, username=username)
    results = get_customers(dbname=dbname, account=account, username=username)
    print(results)
    # results = getCustomersList(dbname=dbname, username=username)
    # print(results)

    # print([r.encode('cp1252') for r in results['customer']])
    # import json
    # data = json.dumps(results['customer'], encoding='latin-1')
    # print(data)

    # filename = '/home/martin/Data/products_customers.json'
    # saveData(data, filename)
