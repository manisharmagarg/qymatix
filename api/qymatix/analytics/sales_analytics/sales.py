import datetime
import json
import os
import sys

import pandas as pd
from numpy import asarray
from numpy import ravel

try:
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from users import getCustomersPerUser
except:
    pass

try:
    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    from users import getCustomersPerUser
except:
    pass

try:
    from api.qymatix.users import getCustomersPerUser
except:
    pass


def getCustomersList(cur, username):
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '')
    if username in ['', 'admin']:
        username = 'all'
    cust = getCustomersPerUser(dbname=dbname, username=username)
    cust = cust[next(iter(cust))].replace('[', '(').replace(']', ')')
    return cust


def accounts(cur, username=''):
    '''
    '''
    if username in ['', 'admin']:
        script_nop = "\
            SELECT customers.id\
            FROM customers;\
            "
    else:
        cust = getCustomersList(cur, username)
        script_nop = "\
            SELECT customers.id\
            FROM customers\
            WHERE customers.id IN {0};\
            ".format(cust)

    cur.execute(script_nop)
    _data = cur.fetchall()

    d = [i[0] for i in _data]

    return d


def min_values(cur, username=''):
    '''
    '''
    if username in ['', 'admin']:
        script_nop = "\
            SELECT MIN(min_price) AS sales, MIN(min_margin) AS margin FROM\
            (SELECT MIN(price) AS min_price, MIN(margin) AS min_margin FROM sales\
            GROUP BY customer_id) AS min\
            "
        # WHERE YEAR(sales.date)=2017\
    else:
        cust = getCustomersList(cur, username)
        script_nop = "\
            SELECT MIN(min_price) AS sales, MIN(min_margin) AS margin FROM\
            (SELECT MIN(price) AS min_price, MIN(margin) AS min_margin FROM sales\
            WHERE customer_id IN {}\
            GROUP BY customer_id) AS min\
            ".format(cust)
        # WHERE YEAR(sales.date)=2017 AND customer_id IN {}\

    cur.execute(script_nop)
    _data = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    min_values = {}
    min_values[cols[0]] = _data[0][0]
    min_values[cols[1]] = _data[0][1]

    return min_values


def max_values(cur, username=''):
    '''
    '''
    if username in ['', 'admin']:
        script_nop = "\
            SELECT MAX(max_price) AS sales, MAX(max_margin) AS margin FROM\
            (SELECT MAX(price) AS max_price, MAX(margin) AS max_margin FROM sales\
            GROUP BY customer_id) AS max\
            "
        # WHERE YEAR(sales.date)=2017\
    else:
        cust = getCustomersList(cur, username)
        script_nop = "\
            SELECT MAX(max_price) AS sales, MAX(max_margin) AS margin FROM\
            (SELECT MAX(price) AS max_price, MAX(margin) AS max_margin FROM sales\
            WHERE customer_id IN {}\
            GROUP BY customer_id) AS max\
            ".format(cust)
        # WHERE YEAR(sales.date)=2017 AND customer_id IN {}\

    cur.execute(script_nop)
    _data = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    min_values = {}
    min_values[cols[0]] = _data[0][0]
    min_values[cols[1]] = _data[0][1]

    return min_values


def average_values(cur, username=''):
    '''
    '''
    if username in ['', 'admin']:
        script_nop = "\
            SELECT AVG(price) AS sales, AVG(margin) AS margin FROM sales\
            GROUP BY customer_id\
            "
        # WHERE YEAR(sales.date)=2017\
    else:
        cust = getCustomersList(cur, username)
        script_nop = "\
            SELECT MAX(max_price) AS sales, MAX(max_margin) AS margin FROM\
            (SELECT MAX(price) AS max_price, MAX(margin) AS max_margin FROM sales\
            WHERE customer_id IN {}\
            GROUP BY customer_id) AS max\
            ".format(cust)
        # WHERE YEAR(sales.date)=2017 AND customer_id IN {}\
        script_nop = "\
            SELECT AVG(price) AS sales, AVG(margin) AS margin FROM sales\
            WHERE customer_id IN {}\
            GROUP BY customer_id\
            ".format(cust)
        # WHERE YEAR(sales.date)=2017 AND customer_id IN {}\

    cur.execute(script_nop)
    _data = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    min_values = {}
    if _data:
        min_values[cols[0]] = _data[0][0]
        min_values[cols[1]] = _data[0][1]

    return min_values


def salesYTD(cur, param='price', account='all', username=''):
    '''
    '''
    today = str(datetime.datetime.now()).split(" ")[0]
    firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))

    # try:
    # account = account.decode('utf-8')
    # except:
    # pass
    # account = account.encode('latin-1')

    if account == 'all':
        if username in ['', 'admin']:
            script_nop = "\
                SELECT SUM(sales.{})\
                FROM sales\
                WHERE DATE(sales.date) BETWEEN '{}' AND '{}'\
                ".format(param, firstday, today)
        else:
            cust = getCustomersList(cur, username)
            script_nop = u"\
                SELECT customers.id, SUM(sales.{})\
                FROM sales\
                LEFT JOIN customers\
                ON sales.customer_id=customers.id\
                WHERE customers.id IN {} AND DATE(sales.date) BETWEEN '{}' AND '{}';\
                ".format(param, cust, firstday, today).encode('latin-1')

    else:
        script_nop = u"\
            SELECT customers.id, SUM(sales.{})\
            FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.id={} AND DATE(sales.date) BETWEEN '{}' AND '{}';\
            ".format(param, account, firstday, today).encode('latin-1')

    # print(script_nop)
    cur.execute(script_nop)
    _data = cur.fetchall()

    if account == 'all':
        result = ravel(asarray(_data))[0]
        return result

    d = dict()
    try:
        if _data[0][0] == None:
            d = 0.0
        else:
            for i in range(len(_data)):
                # d[_data[i][0]] = round(_data[i][1], 2)
                d = round(_data[i][1], 2)
    except:
        d = 0.0
        # raise

    try:
        return d[account]
    except:
        return d


def sales_ytd(cur, param='price', account='all', username=''):
    '''
    '''
    today = str(datetime.datetime.now()).split(" ")[0]
    firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))

    # try:
    # account = account.decode('utf-8')
    # except:
    # pass
    # account = account.encode('latin-1')

    if account == 'all':
        if username in ['', 'admin']:
            script_nop = "\
                SELECT SUM(sales.{})\
                FROM sales\
                WHERE DATE(sales.date) BETWEEN '{}' AND '{}'\
                ".format(param, firstday, today)
        else:
            cust = getCustomersList(cur, username)
            script_nop = u"\
                SELECT customers.id, SUM(sales.{})\
                FROM sales\
                LEFT JOIN customers\
                ON sales.customer_id=customers.id\
                WHERE customers.id IN {} AND DATE(sales.date) BETWEEN '{}' AND '{}';\
                ".format(param, cust, firstday, today).encode('latin-1')

    else:
        script_nop = u"\
            SELECT customers.id, SUM(sales.{})\
            FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.id={} AND DATE(sales.date) BETWEEN '{}' AND '{}';\
            ".format(param, account, firstday, today).encode('latin-1')

    # print(script_nop)
    cur.execute(script_nop)
    _data = cur.fetchall()

    if account == 'all':
        result = ravel(asarray(_data))[0]
        return result

    d = dict()
    try:
        if _data[0][0] == None:
            d = 0.0
        else:
            for i in range(len(_data)):
                d[_data[i][0]] = round(float(_data[i][1]), 2)
    except:
        d = 0.0
        # raise

    try:
        return d[account]
    except:
        return d


def salesMTD(cur, param='price', account='all', username=''):
    '''
    '''
    month = str(datetime.datetime.now().month)
    year = str(datetime.datetime.now().year)

    # try:
    # account = account.decode('utf-8')
    # except:
    # pass
    # account = account.encode('latin-1')

    if account == 'all':
        if username in ['', 'admin']:
            script_nop = "\
                SELECT SUM(sales.{}) from sales\
                WHERE MONTH(sales.date)={} AND YEAR(sales.date)={};\
                ".format(param, month, year)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT SUM(sales.{}) FROM sales\
                LEFT JOIN customers\
                ON sales.customer_id=customers.id\
                WHERE customers.id IN {} AND MONTH(sales.date)={} AND YEAR(sales.date)={};\
                ".format(param, cust, month, year)
    else:
        script_nop = "\
            SELECT SUM(sales.{}) FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.id= '{}' AND MONTH(sales.date)={} AND YEAR(sales.date)={};\
            ".format(param, account, month, year)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        if _data[0][0] == None:
            return 0
        else:
            return round(_data[0][0], 2)
    except:
        return 0


def salesQTD(cur, param='price', year=None, account='all', username=''):
    '''
    '''
    if year == None:
        year = datetime.datetime.now().year

    year = str(year)

    today = str(datetime.datetime.now()).split(" ")[0]

    # try:
    # account = account.decode('utf-8')
    # except:
    # pass
    # account = account.encode('latin-1')

    if account == 'all':
        if username in ['', 'admin']:
            script_nop = "\
            SELECT SUM(sales.{}) from sales\
            WHERE QUARTER(sales.date)<=QUARTER('{}') AND YEAR(sales.date)='{}';\
            ".format(param, today, year)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT customers.id, SUM(sales.{}) FROM sales\
                LEFT JOIN customers\
                ON sales.customer_id=customers.id\
                WHERE customers.id IN {} AND QUARTER(sales.date)<=QUARTER('{}') AND YEAR(sales.date)='{}'\
                GROUP BY customers.id;\
                ".format(param, cust, today, year)

    else:
        script_nop = "\
            SELECT customers.id, SUM(sales.{}) FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.id= '{}' AND QUARTER(sales.date)<=QUARTER('{}') AND YEAR(sales.date)='{}'\
            GROUP BY customers.id;\
            ".format(param, account, today, year)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        if _data[0][0] == None:
            return 0
        else:
            return round(_data[0][0], 2)
    except:
        return 0


def salesPerQuarter(cur, param='price', year=None, account='all', username=''):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year -1)

    '''
    try:
        account = account.decode('utf-8')
    except:
        pass
    account = account.encode('latin-1')
    '''

    if account == 'all':
        if username in ['', 'admin']:
            script_nop = "\
                SELECT QUARTER(sales.date), SUM(sales.{}) from sales\
                WHERE YEAR(sales.date)={}\
                GROUP BY QUARTER(sales.date);\
                ".format(param,year)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT QUARTER(sales.date), SUM(sales.{}) FROM sales\
                LEFT JOIN customers\
                ON sales.customer_id=customers.id\
                WHERE customers.id IN {} AND YEAR(sales.date)='{}'\
                GROUP BY QUARTER(sales.date);\
                ".format(param, cust, year)

    else:
        # SELECT customers.name, QUARTER(sales.date), SUM(sales.{}) FROM sales\
        script_nop = "\
            SELECT QUARTER(sales.date), SUM(sales.{}) FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.id= '{}' AND YEAR(sales.date)='{}'\
            GROUP BY QUARTER(sales.date);\
            ".format(param, account, year)
        # GROUP BY customers.name;\
    # return script_nop
    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        # return int(_data[0][0])
        d = dict()
        for i in range(len(_data)):
            d[int(_data[i][0])] = round(_data[i][1], 2)

        if d == {}:
            today = datetime.datetime.now()
            quarter = (today.month - 1) // 3 + 1
            for q in range(1, quarter + 1):
                d[q] = 0
    except:
        # return 0
        raise

    if 1 not in d.keys():
        d[1] = 0.0
    if 2 not in d.keys():
        d[2] = 0.0
    if 3 not in d.keys():
        d[3] = 0.0
    if 4 not in d.keys():
        d[4] = 0.0

    return d


def values_per_quarter(cur, param='price', year=None, account='all', username=''):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

    cyear = datetime.datetime.now().year
    lyear = cyear - 1

    if account == 'all':
        if username in ['', 'admin']:
            script_nop = "\
                SELECT YEAR(sales.date) AS year, QUARTER(sales.date) AS quarter, SUM(sales.price) AS sales, SUM(sales.margin) AS margin, SUM(sales.cost) AS costs from sales\
                WHERE YEAR(sales.date) BETWEEN {} AND {}\
                GROUP BY QUARTER(sales.date), YEAR(sales.date);\
                ".format(lyear, cyear)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT YEAR(sales.date) AS year, QUARTER(sales.date) AS quarter, SUM(sales.price) AS sales, SUM(sales.margin) AS margin, SUM(sales.cost) AS costs from sales\
                LEFT JOIN customers\
                ON sales.customer_id=customers.id\
                WHERE customers.id IN {} AND YEAR(sales.date) BETWEEN {} AND {}\
                GROUP BY QUARTER(sales.date), YEAR(sales.date);\
                ".format(cust, lyear, cyear)

    else:
        script_nop = "\
            SELECT YEAR(sales.date) AS year, QUARTER(sales.date) AS quarter, SUM(sales.price) AS sales, SUM(sales.margin) AS margin, SUM(sales.cost) AS costs from sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.id= '{}' AND YEAR(sales.date) BETWEEN {} AND {}\
            GROUP BY QUARTER(sales.date), YEAR(sales.date);\
            ".format(account, lyear, cyear)

    cur.execute(script_nop)
    data = asarray(cur.fetchall())
    cols = [desc[0] for desc in cur.description]

    try:
        df = pd.DataFrame(data, columns=cols)
        grouped = df.groupby('year')
        values = {}
        for name, group in grouped:
            values[int(name)] = group.to_dict('list')
            for m in range(1, 5):
                if m not in values[int(name)]['quarter']:
                    values[int(name)]['quarter'].insert(m, m)
                    values[int(name)]['sales'].insert(m, 0.0)
                    values[int(name)]['margin'].insert(m, 0.0)
                    values[int(name)]['costs'].insert(m, 0.0)

        if lyear not in values.keys():
            values[lyear] = {}
            values[lyear]['quarter'] = str(range(1, 5))
            values[lyear]['sales'] = [0, 0, 0, 0, 0]
            values[lyear]['margin'] = [0, 0, 0, 0, 0]
            values[lyear]['costs'] = [0, 0, 0, 0, 0]

        if cyear not in values.keys():
            values[cyear] = {}
            values[cyear]['quarter'] = str(range(1, 5))
            values[cyear]['sales'] = [0, 0, 0, 0, 0]
            values[cyear]['margin'] = [0, 0, 0, 0, 0]
            values[cyear]['costs'] = [0, 0, 0, 0, 0]

        return values

    except:
        # return 0
        # raise
        values = {}

        values[lyear] = {}
        values[lyear]['quarter'] = str(range(1, 5))
        values[lyear]['sales'] = [0, 0, 0, 0, 0]
        values[lyear]['margin'] = [0, 0, 0, 0, 0]
        values[lyear]['costs'] = [0, 0, 0, 0, 0]

        values[cyear] = {}
        values[cyear]['quarter'] = str(range(1, 5))
        values[cyear]['sales'] = [0, 0, 0, 0, 0]
        values[cyear]['margin'] = [0, 0, 0, 0, 0]
        values[cyear]['costs'] = [0, 0, 0, 0, 0]

        return values


def pipelines(cur):
    '''
    '''
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')

    year = datetime.datetime.now().year - 1

    try:
        sql = "\
           SELECT SUM((1+cr.ccbm) * s.sales)/(SELECT SUM(goal) AS pipelines FROM data_{0}.plans) AS pipeline \
           FROM data_{0}.customers c \
           INNER JOIN results_{0}.critters cr \
           ON c.id=cr.name\
           INNER JOIN (SELECT s.customer_id, SUM(s.price) AS sales FROM data_{0}.sales AS s WHERE YEAR(s.date)>={1} GROUP BY s.customer_id) AS s\
           ON c.id=s.customer_id\
           ".format(dbname, year)
        cur.execute(sql)
        value = float(cur.fetchall()[0][0])

        # return json.dumps(rows[0])
        # return json.dumps(value)
        try:
            return 1 / value
        except:
            if value == 0:
                return 1
            else:
                return 0

    except Exception as e:
        print(e)
        raise


def _pipelines(dbname, cur=None):
    # dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')

    try:
        sql = "SELECT round(sum(cr.ccbm*cr.sales)/(select sum(goal) as pipelines from data_{0}.plans)) as pipeline from data_{0}.customers c inner join results_{0}.critters cr on c.name=cr.name;".format(
                dbname
            )
        cur.execute(sql)
        rows = cur.fetchall()

        return json.dumps(rows[0])

    except Exception as e:
        # import traceback
        print(e)
        # return cur.fetchone()[0]
        return -1
