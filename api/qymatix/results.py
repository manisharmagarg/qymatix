import json
import logging
import sys
import traceback
from urllib.parse import unquote_plus

import MySQLdb as mdb
import numpy as np
import pandas as pd

from api.infrastructure.mysql import connection
from api.qymatix.users import getCustomersPerUser

logger = logging.getLogger('django.request')


def getCustomersIdList(cur, username):
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '')
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

    except mdb.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    finally:
        if con:
            con.close()

    return results


def getResults(dbname='username', raw=False, account='all', username=''):
    ''' Reads result's database, manipulate the data and returns it.
    '''
    # return "result"
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
            if account != "":
                script = "\
                    SELECT id FROM {}.customers WHERE name = '{}'\
                    ".format('data_' + dbname, account)


            cur.execute(script)
            con.commit()
            account_id = np.ravel(np.asarray(cur.fetchall()))[0]
            # account_id = int(account)

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
        raise

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
        # print ("Error %d: %s" % (e.args[0],e.args[1]))
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
        # print ("Error %d: %s" % (e.args[0],e.args[1]))
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
            script = "SELECT name, id FROM customers;"
        else:
            cust = getCustomersIdList(cur, username)
            script = "\
                SELECT c.name, c.id FROM {0}.customers AS c\
                LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                WHERE c.id IN {2}\
                ".format(datadb, tasksdb, cust)

        cur.execute(script)
        custlist = np.asarray(cur.fetchall())
        custlst = list()
        for data in custlist:
            item = {
                "name": data[0],
                "id": data[1]
            }
            custlst.append(item)

    except Exception as e:
        # print ("Error %d: %s" % (e.args[0],e.args[1]))
        # sys.exit(1)
        custlst = list()

    finally:
        try:
            con.close()
        except:
            pass

    return custlst


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
        # try:
        #     account = account.decode('utf-8').encode('cp1252')
        #     return "results"
        # except:
        #     account = account.encode('cp1252')
        #     return "error"

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
            # script_nop = "select c.*, u.name as 'kam' from {0}.customers as c left join {1}.Users_Customers as uc on c.id = uc.customer_id left join {1}.users as u on uc.user_id = u.id where c.id = '{2}';".\
            #                 format(datadb, tasksdb, account)    
            # print(script_nop)
            script_nop = "select * from customers"

            logger.info("{}".format(script_nop), extra={'type': 'Login'})

        #        TODO: test following lines
        #        cur.execute(script_nop)
        #        custlist = np.asarray(cur.fetchall()).reshape(-1)
        #        logger.info("{}".format(custlist), extra={'type': 'Login'})

        cur.execute(script_nop)
        custlist = np.asarray(cur.fetchall()).reshape(-1)
        custlist = custlist.reshape(len(custlist) // 17, 17)
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
        results['telephone'] = custlist[:, 13].tolist()
        results['customer_parent_id'] = custlist[:, 14].tolist()
        results['customer_number'] = custlist[:, 15].tolist()
        # ************** Fix Me ***************
        # results['kam'] = custlist[:, 13].tolist()

        # for x in range(len(results['customer'])):
        #     for k in ('customer', 'address', 'country', 'city', 'comment', 'kam'):
        #         if results[k][x] != None:
        #             results[k][x] = results[k][x].encode('latin-1').decode('cp1252')
        #         else:
        #             results[k][x] = ""

    # except Exception as e:
    #     print "Error %d: %s" % (e.args[0],e.args[1])

    except Exception as e:
        logger.info('{}'.format(traceback.format_exc()), extra={'type': 'Login'})
        print(traceback.format_exc())
        results = {
            "message": e,
            "error": traceback.format_exc()
        }
        # raise

    finally:
        try:
            con.close()
        except:
            pass

    return results


def get_linked_customer(dbname, account='all', username=''):
    datadb = 'data_{}'.format(dbname)
    tasksdb = 'data_{}'.format(dbname)
    account = json.loads(account)
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        # account = unquote_plus(account)
        # try:
        #     account = account.decode('utf-8').encode('cp1252')
        # except:
        #     account = account.encode('cp1252')

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
            # script_nop = "select c.*, u.name as 'kam' from {0}.customers as c left join {1}.Users_Customers as uc on c.id = uc.customer_id left join {1}.users as u on uc.user_id = u.id where c.id = '{2}';".\
            #                 format(datadb, tasksdb, account)    
            # print(script_nop)
            parent_id = account['customer_id']
            script_nop = "select * from customers where find_in_set({}, customer_parent_id)".format(
                int(parent_id)
            )

        cur.execute(script_nop)
        custlist = np.asarray(cur.fetchall()).reshape(-1)
        custlist = custlist.reshape(len(custlist) // 15, 15)
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
        results['telephone'] = custlist[:, 13].tolist()
        # ************** Fix Me ***************
        # results['kam'] = custlist[:, 13].tolist()

        # for x in range(len(results['customer'])):
        #     for k in ('customer', 'address', 'country', 'city', 'comment', 'kam'):
        #         if results[k][x] != None:
        #             results[k][x] = results[k][x].encode('latin-1').decode('cp1252')
        #         else:
        #             results[k][x] = ""

    # except Exception as e:
    #     print "Error %d: %s" % (e.args[0],e.args[1])
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        results = []
        # raise

    finally:
        try:
            con.close()
        except:
            pass

    return results


def get_parent_customer(dbname, account='all', username=''):
    datadb = 'data_{}'.format(dbname)
    tasksdb = 'data_{}'.format(dbname)
    account = json.loads(account)
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()
        if account:
            script = "SELECT customer_parent_id from customers where id = {};".format(
                account.get('customer_id')
            )
        # return script
        cur.execute(script)
        parent_id = np.ravel(np.asarray(cur.fetchall()))[0]

        if parent_id.any():
            script = "SELECT * from customers where id = {};".format(
                parent_id
            )
            cur.execute(script)
            custlist = np.asarray(cur.fetchall()).reshape(-1)
            custlist = custlist.reshape(len(custlist) // 15, 15)
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
            results['telephone'] = custlist[:, 13].tolist()
            return results
    except Exception as e:
        return str(traceback.format_exc())


def get_customers_crm(dbname, account='all', username=''):
    '''
    '''
    datadb = 'data_{}'.format(dbname)
    tasksdb = 'data_{}'.format(dbname)
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        '''
        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')
        '''

        if account == 'all':
            if username in ['', 'admin']:
                script_nop = "\
                    SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans FROM {0}.customers AS c\
                    LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                    LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                    LEFT JOIN {1}.tasks AS t ON t.account = c.id\
                    LEFT JOIN {1}.plans AS p ON p.account = c.id\
                    ".format(datadb, tasksdb, tasksdb.replace('data_', 'results_'))
            else:
                cust = getCustomersIdList(cur, username)
                script_nop = "\
                    SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans FROM {0}.customers AS c\
                    LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                    LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                    LEFT JOIN {1}.tasks AS t ON t.account = c.id\
                    LEFT JOIN {1}.plans AS p ON p.account = c.id\
                    WHERE c.id IN {2}\
                    ".format(datadb, tasksdb, cust, tasksdb.replace('data_', 'results_'))
        else:
            script_nop = "\
                SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans FROM {0}.customers AS c\
                LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                LEFT JOIN {1}.tasks AS t ON t.account = c.id\
                LEFT JOIN {1}.plans AS p ON p.account = c.id\
                WHERE c.id = '{2}';\
                ".format(datadb, tasksdb, account, tasksdb.replace('data_', 'results_'))

        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]
        try:
            df = pd.DataFrame(data, columns=cols)
            grouped = df.groupby('id')
            grouped2 = df[['id', 'plans', 'tasks']].groupby('id').count()

            customers = {}
            for name, group in grouped:
                customers[str(name)] = json.loads(group.to_json(orient='records'))[0]

            for k in customers.keys():
                try:
                    customers[k]['actions'] = str(grouped2[grouped2.index == k]['tasks'].values[0])
                    # customers[k]['actions'] = grouped2[grouped2.index==k]['tasks'].values[0]
                except:
                    customers[k]['actions'] = '0'
                try:
                    customers[k]['plans'] = str(grouped2[grouped2.index == k]['plans'].values[0])
                    # customers[k]['plans'] = grouped2[grouped2.index ==k]['plans'].values[0]
                except:
                    customers[k]['plans'] = '0'


        except Exception as e:
            print(e)
            customers = {}
            # pass
            # raise
    except:
        pass
        # raise

    return customers


def get_customers(dbname, account='all', username=''):
    '''
    '''
    datadb = 'data_{}'.format(dbname)
    tasksdb = 'data_{}'.format(dbname)
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        '''
        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')
        '''

        if account == 'all':
            if username in ['', 'admin']:
                # SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                script_nop = "\
                    SELECT c.*, u.name AS 'kam', t.account as tasks, t.created as created, t.due as due, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, " \
                             "cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                             LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                             LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                             LEFT JOIN {1}.tasks AS t ON t.account = c.id\
                             LEFT JOIN {1}.plans AS p ON p.account = c.id\
                             LEFT JOIN {2}.critters AS cr ON cr.name = c.id\
                             ".format(datadb, tasksdb, tasksdb.replace('data_', 'results_'))
            else:
                cust = getCustomersIdList(cur, username)
                # SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                script_nop = "\
                    SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                    LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                    LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                    LEFT JOIN {1}.tasks AS t ON t.account = c.id\
                    LEFT JOIN {1}.plans AS p ON p.account = c.id\
                    LEFT JOIN {3}.critters AS cr ON cr.name = c.id\
                    WHERE c.id IN {2}\
                    ".format(datadb, tasksdb, cust, tasksdb.replace('data_', 'results_'))
        else:
            # SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
            script_nop = "\
                SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                LEFT JOIN {1}.tasks AS t ON t.account = c.id\
                LEFT JOIN {1}.plans AS p ON p.account = c.id\
                LEFT JOIN {3}.critters AS cr ON cr.name = c.id\
                WHERE c.id = '{2}';\
                ".format(datadb, tasksdb, account, tasksdb.replace('data_', 'results_'))

        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]

        try:
            df = pd.DataFrame(data, columns=cols)
            for c in ('sales', 'margin', 'risk', 'ppb', 'ccbm'):
                # df[c] = df[c].apply(pd.to_numeric, errors='')
                df[c] = df[c].apply(pd.to_numeric)
                df['s' + c] = df[c] / df[c].max()
            # print(df)
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
            grouped2 = df[['id', 'plans', 'tasks']].groupby('id').count()

            customers = {}

            for name, group in grouped:
                # group = group.rename(columns={'due':'due', 'action':'type', 'description':'comment', 'plan':'plan_id'})
                # group[['due', 'id', 'created', 'action', 'title', 'description' ]]
                customers[str(name)] = json.loads(group.to_json(orient='records'))[0]
                # customers[int(name)] = group.to_json(orient='records')

            count_risk_high = 0
            count_risk_some = 0
            count_risk_low = 0
            count_risk_unknown = 0

            count_ppb_good = 0
            count_ppb_normal = 0
            count_ppb_bad = 0
            count_ppb_unknown = 0

            for k in customers.keys():
                scales = []
                # for c in ('sales', 'margin', 'risk', 'ppb', 'ccbm'):
                for c in ('sales', 'margin'):
                    try:
                        svalue = np.around(customers[k]['s' + c], 2)
                        value = np.around(customers[k][c], 2)
                    except:
                        value = 0
                        svalue = 0
                    scales.append({'y': svalue, 'value': value, 'label': value})

                c = 'risk'
                try:
                    _value = np.around(customers[k]['s' + c], 2)
                    value = customers[k][c]
                except:
                    _value = 0
                    value = 0

                if value > 1.3 and value <= 2:
                    label = 'low'
                    count_risk_high += 1
                elif value > 0.7 and value <= 1.3:
                    label = 'some'
                    count_risk_some += 1
                elif value > 0.0 and value <= 0.7:
                    label = 'high'
                    count_risk_low += 1
                else:
                    label = 'unknown'
                    count_risk_unknown += 1

                scales.append({'y': _value, 'value': value, 'label': label})

                c = 'ppb'
                try:
                    _value = np.around(customers[k]['s' + c], 2)
                except:
                    _value = 0

                value = customers[k][c]

                if value == 2:
                    label = 'good'
                    count_ppb_good += 1
                elif value == 1:
                    label = 'normal'
                    count_ppb_normal += 1
                elif value == 0:
                    label = 'bad'
                    count_ppb_bad += 1
                else:
                    label = 'unknown'
                    count_ppb_unknown += 1

                scales.append({'y': _value, 'value': value, 'label': label})

                c = 'ccbm'
                try:
                    value = np.around(customers[k]['s' + c], 2)
                except:
                    value = 0
                scales.append({'y': value, 'value': value, 'label': value})

                customers[k]['scales'] = scales

                try:
                    customers[k]['actions'] = str(grouped2[grouped2.index == k]['tasks'].values[0])
                except:
                    customers[k]['actions'] = 0

                try:
                    customers[k]['plans'] = str(grouped2[grouped2.index == k]['plans'].values[0])
                except:
                    customers[k]['plans'] = 0


        except Exception as e:
            print(e)
            customers = {}
            # pass
            raise
    except:
        # pass
        raise

    return customers


def get_group_customers(dbname, account='all', username=''):
    '''
    '''
    datadb = 'data_{}'.format(dbname)
    tasksdb = 'data_{}'.format(dbname)
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        '''
        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')
        '''

        if account == 'all':
            if username in ['', 'admin']:
                # SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                script_nop = "SELECT c.*, u.name AS 'kam', t.account as tasks, " \
                             "t.created as created, t.due as due, p.account as plans, " \
                             "cr.sales as sales, " \
                             "((cr.sales)+(SELECT IFNULL((select sum(scr.sales) " \
                             "from {result_db}.critters AS scr " \
                             "LEFT JOIN  {data_db}.customers ON {data_db}.customers.id = scr.name " \
                             "where {data_db}.customers.customer_parent_id = c.id) " \
                             ",0)as sale)) as groupsales, " \
                             "cr.margin, " \
                             "((cr.margin)+(SELECT IFNULL((select sum(scr.margin) " \
                             "from {result_db}.critters AS scr " \
                             "LEFT JOIN  {data_db}.customers ON {data_db}.customers.id = scr.name " \
                             "where {data_db}.customers.customer_parent_id = c.id) " \
                             ",0)as margin)) as groupmargin, " \
                             "cr.risk , " \
                             "((cr.risk)+(SELECT IFNULL((select avg(scr.risk) " \
                             "from {result_db}.critters AS scr " \
                             "LEFT JOIN  {data_db}.customers ON {data_db}.customers.id = scr.name " \
                             "where {data_db}.customers.customer_parent_id = c.id) " \
                             ",0)as risk)) as grouprisk, " \
                             "cr.ppb, " \
                             "((cr.ppb)+(SELECT IFNULL((select avg(scr.ppb) " \
                             "from {result_db}.critters AS scr " \
                             "LEFT JOIN  {data_db}.customers ON {data_db}.customers.id = scr.name " \
                             "where {data_db}.customers.customer_parent_id = c.id) " \
                             ",0)as ppb)) as groupppb, " \
                             "cr.ccbm, " \
                             "((cr.ccbm)+(SELECT IFNULL((select sum(scr.ccbm) " \
                             "from {result_db}.critters AS scr " \
                             "LEFT JOIN  {data_db}.customers ON {data_db}.customers.id = scr.name " \
                             "where {data_db}.customers.customer_parent_id = c.id) " \
                             ",0)as ccbm)) as groupccbm, " \
                             "cr.size, cr.product_cross_selling, cr.product_type_cross_selling, " \
                             "(select GROUP_CONCAT(name) from {data_db}.customers where customer_parent_id = c.id " \
                             "order by c.id) as child_name, " \
                             "(select GROUP_CONCAT(id) from {data_db}.customers where customer_parent_id = c.id " \
                             "order by c.id) as child_id " \
                             "FROM {data_db}.customers AS c " \
                             "LEFT JOIN {data_db}.Users_Customers AS uc ON c.id = uc.customer_id " \
                             "LEFT JOIN {data_db}.users AS u ON uc.user_id = u.id " \
                             "LEFT JOIN {data_db}.tasks AS t ON t.account = c.id " \
                             "LEFT JOIN {data_db}.plans AS p ON p.account = c.id " \
                             "LEFT JOIN {result_db}.critters AS cr ON cr.name = c.id;".format(
                    data_db=datadb,
                    result_db=tasksdb.replace('data_', 'results_')
                )
            else:
                cust = getCustomersIdList(cur, username)
                # SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                script_nop = "\
                    SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                    LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                    LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                    LEFT JOIN {1}.tasks AS t ON t.account = c.id\
                    LEFT JOIN {1}.plans AS p ON p.account = c.id\
                    LEFT JOIN {3}.critters AS cr ON cr.name = c.id\
                    WHERE c.id IN {2}\
                    ".format(datadb, tasksdb, cust, tasksdb.replace('data_', 'results_'))
        else:
            # SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
            script_nop = "\
                SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                LEFT JOIN {1}.Users_Customers AS uc ON c.id = uc.customer_id\
                LEFT JOIN {1}.users AS u ON uc.user_id = u.id\
                LEFT JOIN {1}.tasks AS t ON t.account = c.id\
                LEFT JOIN {1}.plans AS p ON p.account = c.id\
                LEFT JOIN {3}.critters AS cr ON cr.name = c.id\
                WHERE c.id = '{2}' OR c.customer_parent_id= {2};\
                ".format(datadb, tasksdb, account, tasksdb.replace('data_', 'results_'))
        # return script_nop
        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]

        try:
            df = pd.DataFrame(data, columns=cols)

            f = lambda x: x.isoformat().replace("T", " ") if x is not None else None
            df["created"] = df["created"].apply(f)
            df["due"] = df["due"].apply(f)
            for c in ('sales', 'margin', 'risk', 'ppb', 'ccbm', 'groupsales', 'groupmargin', 'grouprisk', 'groupppb',
                      'groupccbm'):
                # df[c] = df[c].apply(pd.to_numeric, errors='')
                df[c] = df[c].apply(pd.to_numeric)
                df['s' + c] = df[c] / df[c].max()
            # print(df)
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
            grouped2 = df[['id', 'plans', 'tasks']].groupby('id').count()

            customers = {}
            for name, group in grouped:
                # group = group.rename(columns={'due':'due', 'action':'type', 'description':'comment', 'plan':'plan_id'})
                # group[['due', 'id', 'created', 'action', 'title', 'description' ]]
                customers[str(name)] = json.loads(group.to_json(orient='records'))[0]
                # customers[int(name)] = group.to_json(orient='records')

            count_risk_high = 0
            count_risk_some = 0
            count_risk_low = 0
            count_risk_unknown = 0

            count_ppb_good = 0
            count_ppb_normal = 0
            count_ppb_bad = 0
            count_ppb_unknown = 0

            for k in customers.keys():
                scales = list()
                groupscales = list()
                # for c in ('sales', 'margin', 'risk', 'ppb', 'ccbm'):
                for c in ('sales', 'margin'):
                    try:
                        svalue = np.around(customers[k]['s' + c], 2)
                        value = np.around(customers[k][c], 2)
                    except:
                        value = 0
                        svalue = 0
                    scales.append({'y': svalue, 'value': value, 'label': value})

                c = 'risk'
                try:
                    _value = np.around(customers[k]['s' + c], 2)
                    value = customers[k][c]
                except:
                    _value = 0
                    value = 0

                if value > 1.3 and value <= 2:
                    label = 'low'
                    count_risk_high += 1
                elif value > 0.7 and value <= 1.3:
                    label = 'some'
                    count_risk_some += 1
                elif value > 0.0 and value <= 0.7:
                    label = 'high'
                    count_risk_low += 1
                else:
                    label = 'unknown'
                    count_risk_unknown += 1

                scales.append({'y': _value, 'value': value, 'label': label})

                c = 'ppb'
                try:
                    _value = np.around(customers[k]['s' + c], 2)
                except:
                    _value = 0

                value = customers[k][c]

                if value == 2:
                    label = 'good'
                    count_ppb_good += 1
                elif value == 1:
                    label = 'normal'
                    count_ppb_normal += 1
                elif value == 0:
                    label = 'bad'
                    count_ppb_bad += 1
                else:
                    label = 'unknown'
                    count_ppb_unknown += 1

                scales.append({'y': _value, 'value': value, 'label': label})

                c = 'ccbm'
                try:
                    value = np.around(customers[k]['s' + c], 2)
                except:
                    value = 0
                scales.append({'y': value, 'value': value, 'label': value})

                ###### group data ######
                for c in ('groupsales', 'groupmargin'):
                    try:
                        gp_svalue = np.around(customers[k]['s' + c], 2)
                        gp_value = np.around(customers[k][c], 2)
                    except:
                        gp_value = 0
                        gp_svalue = 0
                    groupscales.append({'y': gp_svalue, 'value': gp_value, 'label': gp_value})

                c = 'grouprisk'
                try:
                    gp_value = np.around(customers[k]['s' + c], 2)
                    gp_value = customers[k][c]
                except:
                    gp_value = 0
                    gp_value = 0

                if gp_value > 1.3 and gp_value <= 2:
                    label = 'low'
                    count_risk_high += 1
                elif gp_value > 0.7 and gp_value <= 1.3:
                    label = 'some'
                    count_risk_some += 1
                elif gp_value > 0.0 and gp_value <= 0.7:
                    label = 'high'
                    count_risk_low += 1
                else:
                    label = 'unknown'
                    count_risk_unknown += 1

                groupscales.append({'y': gp_value, 'value': gp_value, 'label': label})

                c = 'groupppb'
                try:
                    group_value = np.around(customers[k]['s' + c], 2)
                except:
                    group_value = 0

                gp_value = customers[k][c]

                if gp_value == 2:
                    label = 'good'
                    count_ppb_good += 1
                elif gp_value == 1:
                    label = 'normal'
                    count_ppb_normal += 1
                elif gp_value == 0:
                    label = 'bad'
                    count_ppb_bad += 1
                else:
                    label = 'unknown'
                    count_ppb_unknown += 1

                groupscales.append({'y': group_value, 'value': gp_value, 'label': label})

                c = 'groupccbm'
                try:
                    gp_value = np.around(customers[k]['s' + c], 2)
                except:
                    gp_value = 0
                groupscales.append({'y': gp_value, 'value': gp_value, 'label': gp_value})

                customers[k]['scales'] = scales
                customers[k]['groupscales'] = groupscales
                if not customers[k]['customer_parent_id']:
                    customers[k]['parent_account'] = True

                try:
                    customers[k]['actions'] = grouped2[grouped2.index == k]['tasks'].values[0]
                except:
                    customers[k]['actions'] = 0
                try:
                    customers[k]['plans'] = grouped2[grouped2.index == k]['plans'].values[0]
                except:
                    customers[k]['plans'] = 0

        except Exception as e:
            print(e)
            customers = {}
            # pass
            raise
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
            SELECT MAX(ccbm) AS ccbm, MAX(ppb) AS ppb, MAX(risk) AS risk FROM critters\
            "
        # GROUP BY name\
        # WHERE YEAR(sales.date)=2017\
    else:
        customers = getCustomersList(dbname, username)
        script_nop = "\
            SELECT MAX(ccbm) AS ccbm, MAX(ppb) AS ppb, MAX(risk) AS risk FROM critters\
            WHERE name IN {}\
            ".format(tuple(customer['name'] for customer in customers))
        # GROUP BY name\
        # WHERE YEAR(sales.date)=2017 AND customer_id IN {}\

    cur.execute(script_nop)
    data = np.asarray(cur.fetchall())
    cols = [desc[0] for desc in cur.description]

    df = pd.DataFrame(data, columns=cols)
    df = df.astype(float)
    df = df.fillna(0)
    return df.to_dict('records')[0]


def min_values(cur, username=''):
    '''
    '''
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    cur.execute("use results_{}".format(dbname))
    #
    if username in ['', 'admin']:
        script_nop = "\
            SELECT MIN(ccbm) AS ccbm, MIN(ppb) AS ppb, MIN(risk) AS risk FROM critters\
            "
        # GROUP BY name\
        # WHERE YEAR(sales.date)=2017\
    else:
        customers = getCustomersList(dbname, username)
        script_nop = "\
            SELECT MIN(ccbm) AS ccbm, MIN(ppb) AS ppb, MIN(risk) AS risk FROM critters\
            WHERE name IN {}\
            ".format(tuple(customer['name'] for customer in customers))
        # GROUP BY name\
        # WHERE YEAR(sales.date)=2017 AND customer_id IN {}\

    cur.execute(script_nop)
    data = np.asarray(cur.fetchall())
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(data, columns=cols)
    df = df.astype(float)
    df = df.fillna(0)
    return df.to_dict('records')[0]


def average_values(cur, username=''):
    '''
    '''
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    cur.execute("use results_{}".format(dbname))

    if username in ['', 'admin']:
        script_nop = "\
            SELECT AVG(ccbm) AS ccbm, AVG(ppb) AS ppb, AVG(risk) AS risk FROM critters\
            "
        # GROUP BY name\
        # WHERE YEAR(sales.date)=2017\
    else:
        customers = getCustomersList(dbname, username)
        script_nop = "\
            SELECT AVG(ccbm) AS ccbm, AVG(ppb) AS ppb, AVG(risk) AS risk FROM critters\
            WHERE name IN {}\
            ".format(tuple(customer['name'] for customer in customers))
        # GROUP BY name\
        ##WHERE YEAR(sales.date)=2017 AND customer_id IN {}\
    #
    cur.execute(script_nop)
    data = np.asarray(cur.fetchall())
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(data, columns=cols)
    df = df.astype(float)
    df = df.fillna(0)
    return df.to_dict('records')[0]


def count_ppb_risk(con, username=''):
    '''
    '''
    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    cur.execute("USE results_{};".format(dbname))

    if username in ['', 'admin']:
        script_nop = "SELECT risk, ppb FROM critters;"
        # GROUP BY name\
        # WHERE YEAR(sales.date)=2017\
    else:
        customers = getCustomersList(dbname, username)
        script_nop = "SELECT risk, ppb FROM critters WHERE name IN {}\
                    ".format(tuple(customer['id'] for customer in customers))
        # GROUP BY name\
        # WHERE YEAR(sales.date)=2017 AND customer_id IN {}\
    try:
        cur.execute(script_nop)
        counts_ppb = dict()
        counts_risk = dict()
        data = np.asarray(cur.fetchall())

        cols = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=cols)
        df = df.astype(float)
        counts_ppb['good'] = str(df[df['ppb'] == 2]['ppb'].count())
        counts_ppb['normal'] = str(df[df['ppb'] == 0]['ppb'].count())
        counts_ppb['bad'] = str(df[df['ppb'] == 1]['ppb'].count())
        counts_ppb['unknown'] = str(df[(df['ppb'] < 0) & (df['ppb'] < 0)]['ppb'].count())

        counts_risk['low'] = str(df[(df['risk'] > 1.3) & (df['risk'] <= 2)]['risk'].count())
        counts_risk['some'] = str(df[(df['risk'] > 0.7) & (df['risk'] <= 1.3)]['risk'].count())
        counts_risk['high'] = str(df[(df['risk'] <= 0.7) & (df['risk'] >= 0)]['risk'].count())
        counts_risk['unknown'] = str(df[(df['risk'] < 0) & (df['risk'] > 2)]['risk'].count())
        return counts_ppb, counts_risk

    except Exception as e:
        # print(e)
        # return traceback.format_exc()
        raise


def get_sales_per_customer(dbname, account='all', username=''):
    '''
    '''
    datadb = 'data_{}'.format(dbname)
    resultsdb = 'results_{}'.format(dbname)
    month_value = account.get("month_value")
    customer_id = account.get("customer_id")
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        '''
        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')
        '''
        if (month_value and customer_id):
            if username in ['', 'admin']:
                # SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                script_nop = "SELECT SUM(t.account) as tasks, SUM(p.account) as plans, " \
                             "SUM(cr.sales) as sales, SUM(cr.margin) as margin, " \
                             "SUM(cr.risk) as risk, SUM(cr.ppb) as ppb, " \
                             "SUM(cr.ccbm) as ccbm, SUM(cr.size) as size, count(*) as total " \
                             "FROM {_db}.customers as c " \
                             "LEFT JOIN {_db}.Users_Customers as uc ON c.id = uc.customer_id " \
                             "LEFT JOIN {_db}.users as u ON uc.user_id = u.id  " \
                             "LEFT JOIN {_db}.tasks as t ON t.account = c.id " \
                             "LEFT JOIN {_db}.plans as p ON p.account = c.id " \
                             "LEFT JOIN {res_db}.critters as cr ON cr.name = c.id " \
                             "LEFT JOIN {_db}.sales as s ON s.customer_id = c.id  " \
                             "where c.id = {_id} AND s.date BETWEEN CURDATE() AND " \
                             "DATE_ADD(CURDATE(), INTERVAL {_month_value} MONTH);".format(
                    _db=datadb,
                    res_db=resultsdb,
                    _id=customer_id,
                    _month_value=month_value
                )
            else:
                cust = getCustomersIdList(cur, username)
                # SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
                script_nop = "SELECT SUM(t.account) as tasks, SUM(p.account) as plans, " \
                             "SUM(cr.sales) as sales, SUM(cr.margin) as margin, " \
                             "SUM(cr.risk) as risk, SUM(cr.ppb) as ppb, " \
                             "SUM(cr.ccbm) as ccbm, SUM(cr.size) as size, count(*) as total " \
                             "FROM {_db}.customers as c " \
                             "LEFT JOIN {_db}.Users_Customers as uc ON c.id = uc.customer_id " \
                             "LEFT JOIN {_db}.users as u ON uc.user_id = u.id  " \
                             "LEFT JOIN {_db}.tasks as t ON t.account = c.id " \
                             "LEFT JOIN {_db}.plans as p ON p.account = c.id " \
                             "LEFT JOIN {res_db}.critters as cr ON cr.name = c.id " \
                             "LEFT JOIN {_db}.sales as s ON s.customer_id = c.id  " \
                             "where c.id = {_id} AND s.date BETWEEN CURDATE() AND " \
                             "DATE_ADD(CURDATE(), INTERVAL {_month_value} MONTH);".format(
                    _db=datadb,
                    res_db=resultsdb,
                    _id=customer_id,
                    _month_value=month_value
                )
        else:
            # SELECT c.*, u.name AS 'kam', t.account as tasks, p.account as plans, cr.sales, cr.size, cr.risk, cr.margin, cr.ppb, cr.ccbm, cr.product_cross_selling, cr.product_type_cross_selling FROM {0}.customers AS c\
            script_nop = "SELECT SUM(t.account) as tasks, SUM(p.account) as plans, " \
                         "SUM(cr.sales) as sales, SUM(cr.margin) as margin, " \
                         "SUM(cr.risk) as risk, SUM(cr.ppb) as ppb, " \
                         "SUM(cr.ccbm) as ccbm, SUM(cr.size) as size, count(*) as total " \
                         "FROM {_db}.customers as c " \
                         "LEFT JOIN {_db}.Users_Customers as uc ON c.id = uc.customer_id " \
                         "LEFT JOIN {_db}.users as u ON uc.user_id = u.id  " \
                         "LEFT JOIN {_db}.tasks as t ON t.account = c.id " \
                         "LEFT JOIN {_db}.plans as p ON p.account = c.id " \
                         "LEFT JOIN {res_db}.critters as cr ON cr.name = c.id " \
                         "LEFT JOIN {_db}.sales as s ON s.customer_id = c.id  " \
                         "where c.id = {_id} AND s.date BETWEEN CURDATE() AND " \
                         "DATE_ADD(CURDATE(), INTERVAL {_month_value} MONTH);".format(
                _db=datadb,
                res_db=resultsdb,
                _id=customer_id,
                _month_value=month_value
            )

        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]
        if data.any():
            df = pd.DataFrame(data, columns=cols)
            df = df.to_dict("records")
            '''
            {
                "tasks": 564.0, 
                "plans": 564.0, 
                "sales": 2256809.8270559995, 
                "margin": 713138.4042347999, 
                "risk": 1.8592027581120003, 
                "ppb": 12.0, 
                "ccbm": 30.42778864464, 
                "size": 145.73467371960004
            }
            '''
            for data in df:
                scales_three_month = list()
                total = data.get("total")
                sales = data.get("sales")
                margin_value = data.get("margin")
                risk_value = data.get("risk")
                ppb_value = data.get("ppb")
                ccbm_value = data.get("ccbm")
                # sales
                try:
                    total_sales = np.around(sales, 2)
                except:
                    total_sales = 0
                # margin
                try:
                    value_margin = np.around(margin_value, 2)
                except:
                    value_margin = 0

                # risk
                try:
                    _risk = np.around(risk_value, 2)
                    value_risk = _risk / total
                except:
                    value_risk = 0

                risk_label = ''
                if value_risk > 1.3 and value_risk <= 2:
                    risk_label = 'low'
                    # count_risk_high += 1
                elif value_risk > 0.7 and value_risk <= 1.3:
                    risk_label = 'some'
                    # count_risk_some += 1
                elif value_risk > 0.0 and value_risk <= 0.7:
                    risk_label = 'high'
                    # count_risk_low += 1
                else:
                    risk_label = 'unknown'
                    # count_risk_unknown += 1
                # ppb
                try:
                    _ppb = np.around(ppb_value, 2)
                    value_ppb = _ppb / total
                except:
                    value_ppb = 0
                ppb_label = ''
                if value_ppb == 2:
                    ppb_label = 'good'
                    count_ppb_good += 1
                elif value_ppb == 1:
                    ppb_label = 'normal'
                    # count_ppb_normal += 1
                elif value_ppb == 0:
                    ppb_label = 'bad'
                    # count_ppb_bad += 1
                else:
                    ppb_label = 'unknown'
                    # count_ppb_unknown += 1

                # ccbm
                try:
                    value_ccbm = np.around(ccbm_value, 2)
                except:
                    value_ccbm = 0

                final_sales = {
                    "sales": total_sales,
                    "margin": value_margin,
                    "risk": risk_label,
                    "risk_value": value_risk,
                    "ppb": ppb_label,
                    "ppb_value": value_ppb,
                    "ccbm": value_ccbm,
                }
                scales_three_month.append(final_sales)
            return scales_three_month
        else:
            return "Record Not found"

    except Exception as e:
        return str(traceback.format_exc())


def add_linked_customer(dbname, account='all', username=''):
    datadb = 'data_{}'.format(dbname)
    resultsdb = 'results_{}'.format(dbname)
    parent_customer_id = account.get("parent_customer_id")
    linked_customer_id = account.get("linked_customer_id")
    # return "{}, {}".format(linked_customer_id, convert_list_tuple(linked_customer_id))
    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()
        if (parent_customer_id and linked_customer_id):
            """
            script = "UPDATE customers SET customer_parent_id = {} WHERE id IN {}".format(
                parent_customer_id,
                convert_list_tuple(str(linked_customer_id))
            )
            # return script
            cur.execute(script)
            con.commit()
            return "Customers Linked Successfully"
            """

            for ids in linked_customer_id:
                script = "SELECT customer_parent_id from customers WHERE id = {}".format(
                    ids
                )
                # return
                cur.execute(script)
                data = np.asarray(cur.fetchall())
                cols = [desc[0] for desc in cur.description]

                df = pd.DataFrame(data, columns=cols)
                # return  df.values.any()
                if df.values.any() != "":
                    exists_ids = df['customer_parent_id'].tolist()
                    lst = list()

                    if len(exists_ids) < 1:
                        for ex_id in exists_ids:
                            for sub_e in ex_id.split(","):
                                if int(sub_e) == int(parent_customer_id):
                                    continue
                                lst.append(int(sub_e))
                    else:
                        for ex_id in exists_ids:
                            if int(ex_id) == int(parent_customer_id):
                                continue
                            lst.append(ex_id)

                    lst.append(parent_customer_id)
                    list_of_parent_ids = ",".join(str(st) for st in lst)

                    script_nop = "UPDATE customers SET customer_parent_id = '{}' WHERE id IN {}".format(
                        str(list_of_parent_ids),
                        convert_list_tuple(str(linked_customer_id))
                    )
                    cur.execute(script_nop)
                    con.commit()
                else:
                    script_nop = "UPDATE customers SET customer_parent_id = '{}' WHERE id IN {}".format(
                        parent_customer_id,
                        convert_list_tuple(str(linked_customer_id))
                    )
                    cur.execute(script_nop)
                    con.commit()

            return "Customers Linked Successfully"
    except Exception as e:
        return str(traceback.format_exc())


def remove_linked_customer(dbname, account='all', username=''):
    datadb = 'data_{}'.format(dbname)
    resultsdb = 'results_{}'.format(dbname)
    parent_customer_id = account.get("parent_customer_id")
    linked_customer_id = account.get("linked_customer_id")

    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()
        if (parent_customer_id and linked_customer_id):
            script = "SELECT customer_parent_id from {db_}.customers " \
                     "where find_in_set({parent_customer_id}, " \
                     "customer_parent_id) AND id = " \
                     "{linked_customer_id}".format(
                db_=datadb,
                parent_customer_id=parent_customer_id,
                linked_customer_id=linked_customer_id
            )

            cur.execute(script)
            data = np.asarray(cur.fetchall())
            cols = [desc[0] for desc in cur.description]
            df = pd.DataFrame(data, columns=cols)
            parents_ids = df['customer_parent_id'].tolist()

            lst = list()

            for pt_id in parents_ids:
                try:
                    pt_ids = pt_id.split(",")

                    for sub_e in pt_ids:
                        if int(sub_e) == int(parent_customer_id):
                            continue
                        lst.append(int(sub_e))
                except:
                    lst.append(pt_id)
                    script_nop = "UPDATE {db_}.customers SET " \
                                 "customer_parent_id = '' " \
                                 "WHERE id = {linked_customer_id}".format(
                        db_=datadb,
                        linked_customer_id=linked_customer_id
                    )

                    cur.execute(script_nop)
                    con.commit()
                    return "Csutomer Removed Successfully"

            list_of_parent_ids = ",".join(str(st) for st in lst)

            script_nop = "UPDATE {db_}.customers SET " \
                         "customer_parent_id = '{list_of_parent_ids}' " \
                         "WHERE id = {linked_customer_id}".format(
                db_=datadb,
                list_of_parent_ids=str(list_of_parent_ids),
                linked_customer_id=linked_customer_id
            )

            cur.execute(script_nop)
            con.commit()
            return "Csutomer Removed Successfully"
    except Exception as e:
        return str(traceback.format_exc())


def customer_by_products(dbname, account='all', username=''):
    datadb = 'data_{}'.format(dbname)
    resultsdb = 'results_{}'.format(dbname)

    product_id = account.get("product_id")

    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if product_id:
            script = "select cr.name as customer_id, " \
                     "c.name as customer_name," \
                     "ROUND(avg(s.price), 2) as avg_price, " \
                     "max(s.price) as max_price, " \
                     "ROUND(sum(s.price), 2) as total_price, " \
                     "ROUND(sum(cr.sales), 2) as sales, " \
                     "avg(cr.ppb) as ppb from {data_db}.sales as s " \
                     "LEFT join {data_db}.customers as c on c.id = s.customer_id " \
                     "LEFT join {results_db}.critters as cr on " \
                     "cr.name = s.customer_id " \
                     "where s.product_id = {product_id} " \
                     "group by s.customer_id;".format(
                data_db=datadb,
                results_db=resultsdb,
                product_id=product_id
            )

            cur.execute(script)
            data = np.asarray(cur.fetchall())
            cols = [desc[0] for desc in cur.description]
            df = pd.DataFrame(data, columns=cols)
            return df.to_dict("records")
    except Exception as e:
        return str(traceback.format_exc())


def customer_by_product_types(dbname, account='all', username=''):
    datadb = 'data_{}'.format(dbname)
    resultsdb = 'results_{}'.format(dbname)

    product_type_id = account.get("product_type_id")

    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if product_type_id:
            script = "select cr.name as customer_id, " \
                     "c.name as customer_name, " \
                     "ROUND(avg(s.price), 2) as avg_price, " \
                     "max(s.price) as max_price, " \
                     "ROUND(sum(s.price), 2) as total_price, " \
                     "ROUND(sum(cr.sales), 2) as sales, " \
                     "avg(cr.ppb) as ppb from {datadb_}.sales as s " \
                     "LEFT join {datadb_}.customers as c " \
                     "on c.id = s.customer_id " \
                     "LEFT join {datadb_}.products as p " \
                     "on p.id = s.product_id " \
                     "LEFT join {resultsdb_}.critters as cr on " \
                     "cr.name = s.customer_id where " \
                     "p.product_type_id = {product_type_id} " \
                     "group by s.customer_id;".format(
                datadb_=datadb,
                resultsdb_=resultsdb,
                product_type_id=product_type_id
            )

            cur.execute(script)
            data = np.asarray(cur.fetchall())
            cols = [desc[0] for desc in cur.description]
            df = pd.DataFrame(data, columns=cols)

            return df.to_dict("records")
    except Exception as e:
        return str(traceback.format_exc())


def convert_list_tuple(list_data):
    print(type(list_data))
    return list_data.replace('[', '(').replace(']', ')')


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
    username = 'chancho_babe__qymatix_best'
    dbname = 'aet_at'
    username = 'admin'
    # results = getResults(dbname=dbname, account=account, username=username)
    # print(results)
    # results = getCustomers(dbname=dbname, account=account, username=username)
    # results = get_customers(dbname=dbname, account=account, username=username)

    # account = '200702'
    dbname = "qymatix_de"
    username = "wolfgang__qy___test_com"
    username = 'all'
    username = 'max__qy___test_com'
    dbname = "qy___test_com"

    username = 'philipp__spm_li'
    username = ''
    dbname = 'spm_li'
    results = get_customers_crm(dbname=dbname, account=account, username=username)
    print(results)

    # print(results['200221'])
    # print(results[1]['plans'])

    # results = getCustomersList(dbname=dbname, username=username)
    # print(results)

    # print([r.encode('cp1252') for r in results['customer']])
    # import json
    # data = json.dumps(results['customer'], encoding='latin-1')
    # print(data)

    # filename = '/home/martin/Data/products_customers.json'
    # saveData(data, filename)
