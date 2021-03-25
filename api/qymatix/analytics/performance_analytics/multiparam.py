import datetime
import os
import sys

import numpy as np
import pandas as pd

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
    cust = getCustomersPerUser(dbname=dbname, username=username)
    cust = cust[next(iter(cust))].replace('[', '(').replace(']', ')')
    return cust


def monthlyParam(cur, param='price', yearMin=2008, year=2015, account='all', username=''):
    '''
    '''

    yearMin = year

    '''
    try:
        account = account.decode('utf-8')
    except:
        pass
    account = account.encode('latin-1')
    '''

    if account == 'all':
        if username in ['', 'admin']:
            script_sales = "\
                SELECT MONTH(sales.date), SUM(sales.{}) AS NumberOfProducts FROM sales\
                LEFT JOIN customers\
                ON sales.customer_id=customers.id\
                WHERE YEAR(sales.date) BETWEEN {} AND {}\
                GROUP BY MONTH(sales.date)\
                ".format(param, yearMin, year)
            # GROUP BY sales.month;\
        else:
            cust = getCustomersList(cur, username)
            script_sales = "\
                SELECT MONTH(sales.date), SUM(sales.{0}) AS NumberOfProducts FROM sales\
                LEFT JOIN customers\
                ON sales.customer_id=customers.id\
                WHERE customers.id IN {1} AND YEAR(sales.date) BETWEEN {2} AND {3}\
                GROUP BY MONTH(sales.date)\
                ".format(param, cust, yearMin, year)

    else:
        script_sales = "\
            SELECT MONTH(sales.date), SUM(sales.{0}) AS NumberOfProducts FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.id= '{1}' AND YEAR(sales.date) BETWEEN {2} AND {3}\
            GROUP BY MONTH(sales.date)\
            ".format(param, account, yearMin, year)
        # WHERE YEAR(sales.date) BETWEEN {2} AND {3}\
        # GROUP BY sales.month\

    if param == 'price':
        param = 'sales'

    cur.execute(script_sales)

    cols = np.asarray(cur.fetchall())

    # month = ['Jan', 'Feb', 'Mar', 'Apr', 'Mar', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month = range(1, 13)
    _months = []

    results = []
    for i in range(12):
        results += [{param: 0.0, 'month': i + 1}]

    for c in cols:
        _results = dict()
        _results[param] = round(float(c[1]), 2)
        _results['month'] = int(c[0])
        _months.append(month[int(c[0]) - 1])

        results[int(c[0]) - 1] = _results

    return results


def values_per_month(cur, param='price', yearMin=2008, year=2015, account='all', username=''):
    '''
    '''

    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    cur.execute("USE {}".format('data_' + dbname))

    today = datetime.datetime.now()
    tyb = datetime.datetime(year=today.year - 3, month=1, day=1)

    year = today.year
    yearMin = year - 1

    if account == 'all':
        if username in ['', 'admin']:
            script = "\
                SELECT YEAR(s.date) AS year, MONTH(s.date) AS month, SUM(s.price) AS sales, SUM(s.margin) AS margin, SUM(s.cost) AS costs FROM sales AS s\
                LEFT JOIN customers AS c\
                ON s.customer_id=c.id\
                WHERE YEAR(s.date) BETWEEN {} AND {}\
                GROUP BY MONTH(s.date), YEAR(s.date)\
                ".format(yearMin, year)
            # GROUP BY sales.month;\
        else:
            cust = getCustomersList(cur, username)
            script = "\
                SELECT YEAR(s.date) AS year, MONTH(s.date) AS month, SUM(s.price) AS sales, SUM(s.margin) AS margin, SUM(s.cost) AS costs FROM sales AS s\
                LEFT JOIN customers AS c\
                ON s.customer_id=c.id\
                WHERE c.id IN {} AND YEAR(s.date) BETWEEN {} AND {}\
                GROUP BY MONTH(s.date), YEAR(s.date)\
                ".format(cust, yearMin, year)

    else:
        script = "\
                SELECT YEAR(s.date) AS year, MONTH(s.date) AS month, SUM(s.price) AS sales, SUM(s.margin) AS margin, SUM(s.cost) AS costs FROM sales AS s\
                LEFT JOIN customers AS c\
                ON s.customer_id=c.id\
                WHERE c.id={customer_id} AND YEAR(s.date) "\
                "BETWEEN {yearMin} AND {year}\
                GROUP BY MONTH(s.date), YEAR(s.date)\
            ".format(customer_id=account, yearMin=yearMin, year=year)

    cur.execute(script)
    data = np.asarray(cur.fetchall())
    cols = [desc[0] for desc in cur.description]

    try:
        df = pd.DataFrame(data, columns=cols)
        df = df.round({"sales":2})
        grouped = df.groupby('year')
        values = {}
        for name, group in grouped:
            values[int(name)] = group.to_dict('list')
            for m in range(1, 13):
                if m not in values[int(name)]['month']:
                    values[int(name)]['month'].insert(m, m)
                    values[int(name)]['sales'].insert(m, 0.0)
                    values[int(name)]['margin'].insert(m, 0.0)
                    values[int(name)]['costs'].insert(m, 0.0)

        if yearMin not in values.keys():
            values[yearMin] = {}
            values[yearMin]['month'] = str(range(1, 13))
            values[yearMin]['sales'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            values[yearMin]['margin'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            values[yearMin]['costs'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if year not in values.keys():
            values[year] = {}
            values[year]['month'] = str(range(1, 13))
            values[year]['sales'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            values[year]['margin'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            values[year]['costs'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    except:
        values = {}

        values[yearMin] = {}
        values[yearMin]['month'] = str(range(1, 13))
        values[yearMin]['sales'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        values[yearMin]['margin'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        values[yearMin]['costs'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        values[year] = {}
        values[year]['month'] = str(range(1, 13))
        values[year]['sales'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        values[year]['margin'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        values[year]['costs'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # raise
        # pass

    return values
