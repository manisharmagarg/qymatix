import datetime
import logging

import numpy as np

from api.infrastructure.mysql import connection

logger = logging.getLogger(__name__)


def getInsights(username='username', account='all'):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    # username = 'username'
    dbname = 'data_{}'.format(username)

    data = dict()

    try:
        logger.debug(dbname)

        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        logger.debug(con)

        if account == 'all':
            data['plans per account'] = plansPerAccount(cur)
            data['actions per account'] = actionsPerAccount(cur)

        data['activity goals'] = activityGoals(cur, account=account)
        data['total sales plans'] = totalSalesPlans(cur, account=account)
        data['total plan goals'] = totalPlanGoals(cur, account=account)

        data['actions per day'] = actionsPerDay(cur, account=account)
        data['actions per month'] = actionsPerMonth(cur, account=account)
        data['actions per year'] = actionsPerYear(cur, account=account)

        data['goals per quarter'] = goalsPerQuarter(cur, account=account)
        data['total calls goal'] = totalCallsGoal(cur, account=account)
        data['total visits goal'] = totalVisitsGoal(cur, account=account)
        data['total offers goal'] = totalOffersGoal(cur, account=account)

        month = str(datetime.datetime.now().month)
        try:
            data['actions this month'] = data['actions per month'][month]
        except:
            data['actions this month'] = 0

        data['actions QTD'] = actionsQTD(cur, account=account)
        data['actions MTD'] = actionsMTD(cur, account=account)
        data['actions YTD'] = actionsYTD(cur, account=account)

        today = str(datetime.datetime.now()).split(" ")[0]
        firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))
        wd = np.busday_count(firstday, today) * 1.0
        data['actions YTD date ratio'] = round(data['actions YTD'] / wd, 2)

        # data['actions YTD accounts ratio'] = data['actions YTD'] / data['number of accounts']

        '''
        script_nop = "\
            SELECT FORMAT(SUM(buyprice),2) FROM\
            (SELECT buyprice\
            FROM products\
            ORDER BY buyprice DESC\
            LIMIT 10) price;\
            "
        '''

        '''
        SELECT orderNumber,
               FORMAT(SUM(quantityOrdered * priceEach),2) total
               FROM orderdetails
               GROUP BY orderNumber
               ORDER BY SUM(quantityOrdered * priceEach) DESC;
        '''

        '''
        param = 'action'
        customer = 'EGF'
        yearMin = 2015
        yearMax = 2015
        script_nop = "\
            SELECT tasks.account, MONTH(tasks.due),\
            SUM(tasks.{}) AS NumberOfProducts FROM tasks\
            LEFT JOIN account\
            ON sales.customer_id=customers.id\
            WHERE tasks.account = '{}' AND YEAR(tasks.due) BETWEEN {} AND {}\
            GROUP BY MONTH(tasks.due);\
            ".format(param, customer, yearMin, yearMax)
        '''

        # script_nop = "\
        # SELECT customers.name, sales.month,\
        # SUM(sales.{}) AS NumberOfProducts FROM sales\
        # LEFT JOIN customers\
        # ON sales.customer_id=customers.id\
        # WHERE customers.name = '{}' AND sales.year BETWEEN {} AND {}\
        # GROUP BY sales.month;\
        # ".format(param, customer, yearMin, yearMax)

        # script_nop = "\
        # SELECT `COLUMN_NAME`\
        # FROM `INFORMATION_SCHEMA`.`COLUMNS`\
        # WHERE `TABLE_SCHEMA`='results_userID_{}'\
        # AND `TABLE_NAME`='customers';\
        # ".format(username)

        '''
        script_nop = "\
            SELECT `COLUMN_NAME`\
            FROM `INFORMATION_SCHEMA`.`COLUMNS`\
            WHERE `TABLE_SCHEMA`='results_{}'\
            AND `TABLE_NAME`='critters';\
            ".format(username)
            #show columns from customers;\

        cur.execute(script_nop)
        cols = np.ravel(np.asarray(cur.fetchall()))

        results = dict()
        for c in cols:
            values = np.ravel(data[:, np.where(cols==c)])
            if not raw:
                if c != 'name':
                    values = values.astype(np.float)
                    values = np.around(np.nan_to_num(values), 2)
                #if c == 'ccbm':
                if c == 'risk':
                    results['rawRisk'] = values.tolist()
                    #values = colortables.convertToColor(values)
                    values = colortables.colorK1(values, 'json')

            results[c] = values.tolist()
        '''

    except Exception as e:
        # raise
        # print("Error {0}: {1}".format(e.args[0], e.args[1]))
        print(e)
        # sys.exit(1)
    finally:
        try:
            if con:
                con.close()
        except:
            print('No Db connection possible')

    dbname = 'data_{}'.format(username)

    # data = dict()

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        today = datetime.datetime.now()

        # list of all accounts
        if account == 'all':
            data['accounts'] = accounts(cur)
            # active accounts and sales in the las 3 months
            data['active accounts'] = activeAccounts(cur)
            hoy = datetime.datetime.now()
            _tmb = datetime.datetime(year=hoy.year, month=hoy.month, day=hoy.day)
            try:
                data['active accounts growth'] = 100. * (
                            len(data['active accounts'].keys()) / len(activeAccounts(cur, today=_tmb).keys()) - 1)
            except:
                data['active accounts growth'] = 0

            # for aa in data['active accounts'].keys():
            data['lost accounts'] = [a for a in data['accounts'] if a not in data['active accounts'].keys()]
            # data['actions-accounts ratio'] = round(float(data['actions YTD']) / len(data['accounts']), 2)
            # data['actions-active accounts ratio'] = round(float(data['actions YTD']) / len(data['active accounts'].keys()), 2)
            # data['penetration ratio'] = round(100 * float(len(data['active accounts'].keys())) / len(data['accounts']), 2)
            try:
                data['actions-accounts ratio'] = round(float(data['actions YTD']) / len(data['accounts']), 2)
            except:
                data['actions-accounts ratio'] = 0.0
            try:
                data['actions-active accounts ratio'] = round(
                    float(data['actions YTD']) / len(data['active accounts'].keys()), 2)
            except:
                data['actions-active accounts ratio'] = 0.0
            try:
                data['penetration ratio'] = round(
                    100 * float(len(data['active accounts'].keys())) / len(data['accounts']), 2)
            except:
                data['penetration ratio'] = 0.0

        data['sales YTD'] = round(salesYTD(cur, account=account), 2)
        data['margin YTD'] = round(salesYTD(cur, param='margin', account=account), 2)
        data['sales QTD'] = round(salesQTD(cur, year=today.year, account=account), 2)
        data['margin QTD'] = round(salesQTD(cur, param='margin', year=today.year, account=account), 2)
        data['sales MTD'] = round(salesMTD(cur, account=account), 2)
        data['sales per quarter'] = salesPerQuarter(cur, param='price', year=today.year, account=account)
        data['margin per quarter'] = salesPerQuarter(cur, param='margin', year=today.year, account=account)

        data['monthly sales'] = monthlyParam(cur, param='price', year=today.year, account=account)
        data['monthly sales last year'] = monthlyParam(cur, param='price', year=today.year - 1, account=account)

        data['monthly margin'] = monthlyParam(cur, param='margin', year=today.year, account=account)
        data['monthly margin last year'] = monthlyParam(cur, param='margin', year=today.year - 1, account=account)

        s = 0
        for d in data['monthly sales last year']:
            s += d['sales']
        data['sales last year'] = round(s, 2)

        try:
            data['sales growth YTD'] = round(100 * data['sales YTD'] / data['sales last year'], 0)
        except:
            data['sales growth YTD'] = 0.0

        s = 0
        if today.month > 1:
            try:
                data['sales growth month'] = round(
                    data['monthly sales'][today.month] / data['monthly sales'][today.month - 1], 2)
            except:
                data['sales growth month'] = 0.0
        else:
            for l in data['monthly sales last year']:
                if l['month'] == 12:
                    sb = l['sales']
            for l in data['monthly sales']:
                if l['month'] == 12:
                    cs = l['sales']
            try:
                data['sales growth month'] = round(cs / sb, 2)
            except:
                data['sales growth month'] = 0.0

        s = 0
        for d in data['monthly margin last year']:
            s += d['margin']
        data['margin last year'] = round(s, 2)

        try:
            data['margin growth YTD'] = round(100 * data['margin YTD'] / data['margin last year'], 0)
        except:
            data['margin growth YTD'] = 0.0

        s = 0
        if today.month > 1:
            try:
                data['margin growth month'] = round(
                    data['monthly margin'][today.month] / data['monthly margin'][today.month - 1], 2)
            except:
                data['margin growth month'] = 0.0
        else:
            for l in data['monthly margin last year']:
                if l['month'] == 12:
                    sb = l['margin']
            for l in data['monthly margin']:
                if l['month'] == 12:
                    cs = l['margin']
            try:
                data['margin growth month'] = round(cs / sb, 2)
            except:
                data['margin growth month'] = 0.0

        # SALES
        currentQuarter = (today.month - 1) // 3 + 1
        salesCurrentQuarter = data['sales per quarter'][currentQuarter]
        if currentQuarter == 1:
            salesLastQuarter = round(salesPerQuarter(cur, year=today.year - 1, param='price', account=account)[4], 2)
        else:
            salesLastQuarter = round(data['sales per quarter'][currentQuarter - 1], 2)

        try:
            data['sales growth QTD'] = round(100 * salesCurrentQuarter / salesLastQuarter, 2)
        except:
            data['sales growth QTD'] = 0.0

        # MARGIN
        currentQuarter = (today.month - 1) // 3 + 1
        marginCurrentQuarter = data['margin per quarter'][currentQuarter]
        if currentQuarter == 1:
            marginLastQuarter = round(salesPerQuarter(cur, year=today.year - 1, param='margin', account=account)[4], 2)
        else:
            marginLastQuarter = round(data['margin per quarter'][currentQuarter - 1], 2)

        try:
            data['margin growth QTD'] = round(100 * marginCurrentQuarter / marginLastQuarter, 2)
        except:
            data['margin growth QTD'] = 0.0

    except Exception as e:
        # print("Error {0}: {1}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        data = {}
    finally:
        try:
            if con:
                con.close()
        except:
            print('No Db connection possible')
    # print(data)
    # for k, v in data.iteritems():
    # print("{}: {}".format(k, v))

    return data


def getInsightsPerCustomer(username='username', account='all'):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    # username = 'username'
    dbname = 'data_{}'.format(username)

    data = dict()

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        # data['plans per account'] = plansPerAccount(cur)
        # data['actions per account'] = actionsPerAccount(cur)

        data['activity goals'] = activityGoals(cur, account=account)
        data['total sales plans'] = totalSalesPlans(cur, account=account)
        data['total plan goals'] = totalPlanGoals(cur, account=account)

        data['actions per day'] = actionsPerDay(cur, account=account)
        data['actions per month'] = actionsPerMonth(cur, account=account)
        data['actions per year'] = actionsPerYear(cur, account=account)

        data['goals per quarter'] = goalsPerQuarter(cur, account=account)
        data['total calls goal'] = totalCallsGoal(cur, account=account)
        data['total visits goal'] = totalVisitsGoal(cur, account=account)
        data['total offers goal'] = totalOffersGoal(cur, account=account)

        month = str(datetime.datetime.now().month)
        try:
            data['actions this month'] = data['actions per month'][month]
        except:
            data['actions this month'] = 0

        data['actions QTD'] = actionsQTD(cur, account=account)
        data['actions MTD'] = actionsMTD(cur, account=account)
        data['actions YTD'] = actionsYTD(cur, account=account)

        today = str(datetime.datetime.now()).split(" ")[0]
        firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))
        wd = np.busday_count(firstday, today) * 1.0
        data['actions YTD date ratio'] = round(data['actions YTD'] / wd, 2)

        # data['actions YTD accounts ratio'] = data['actions YTD'] / data['number of accounts']

    except Exception as e:
        raise
        # print("Error {0}: {1}".format(e.args[0], e.args[1]))
        # sys.exit(1)
    finally:
        try:
            if con:
                con.close()
        except:
            print('No Db connection possible')

    dbname = 'data_{}'.format(username)

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        today = datetime.datetime.now()

        ## list of all accounts
        # data['accounts'] = accounts(cur)
        ## active accounts and sales in the las 3 months
        # data['active accounts'] = activeAccounts(cur)
        # data['lost accounts'] = [a for a in data['accounts'] if a not in data['active accounts'].keys()]
        # data['actions-accounts ratio'] = float(data['actions YTD']) / len(data['accounts'])
        # data['actions-active accounts ratio'] = float(data['actions YTD']) / len(data['active accounts'].keys())
        # data['penetration ratio'] = 100 * float(len(data['active accounts'].keys())) / len(data['accounts'])

        data['sales per quarter'] = salesPerQuarter(cur, param='price', year=today.year, account=account)
        data['margin per quarter'] = salesPerQuarter(cur, param='margin', year=today.year, account=account)
        data['sales YTD'] = salesYTD(cur, account=account)
        data['margin YTD'] = salesYTD(cur, param='margin', account=account)
        data['sales QTD'] = salesQTD(cur, year=today.year, account=account)
        data['margin QTD'] = salesQTD(cur, param='margin', year=today.year, account=account)
        data['sales MTD'] = salesMTD(cur, account=account)

        data['monthly sales'] = monthlyParam(cur, param='price', year=today.year, account=account)
        data['monthly sales last year'] = monthlyParam(cur, param='price', year=today.year - 1, account=account)

        s = 0
        for d in data['monthly sales last year']:
            s += d['sales']
        data['sales last year'] = round(s, 2)

        data['sales growth YTD'] = round(100 * data['sales YTD'] / data['sales last year'], 2)

        print(data['monthly sales'][today.month]['sales'])
        s = 0
        if today.month > 1:
            try:
                data['sales growth month'] = data['monthly sales'][today.month]['sales'] / \
                                             data['monthly sales'][today.month - 1]['sales']
            except:
                data['sales growth month'] = 0.0
        else:
            for l in data['monthly sales last year']:
                if l['month'] == 12:
                    sb = l['sales']
            for l in data['monthly sales']:
                if l['month'] == 12:
                    cs = l['sales']
            data['sales growth month'] = round(cs / sb, 2)

        currentQuarter = (today.month - 1) // 3 + 1
        salesCurrentQuarter = data['sales per quarter'][currentQuarter]
        if currentQuarter == 1:
            salesLastQuarter = salesPerQuarter(cur, year=today.year - 1, param='price', account=account)[4]
        else:
            salesLastQuarter = data['sales per quarter'][currentQuarter - 1]

        try:
            data['sales growth QTD'] = round(100. * salesCurrentQuarter / salesLastQuarter, 2)
        except:
            data['sales growth QTD'] = 0.0

    except Exception as e:
        # print("Error {0}: {1}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        # raise
        data = {}
    finally:
        try:
            if con:
                con.close()
        except:
            print('No Db connection possible')

    # print(data)
    # for k, v in data.iteritems():
    # print("{}: {}".format(k, v))

    return data


def accounts(cur):
    '''
    '''
    script_nop = "\
        SELECT customers.name\
        FROM customers;\
        "

    cur.execute(script_nop)
    _data = cur.fetchall()

    # d = dict()
    # for i in range(len(_data)):
    # d[_data[i][0]] = round(_data[i][1], 2)

    # if d == {}:
    # d  = 0

    d = [i[0] for i in _data]
    # d = np.asarray(_data)

    return d


def accountsThreeYD(cur):
    '''
    '''

    today = str(datetime.datetime.now()).split(" ")[0]
    today = datetime.datetime.now()
    tyb = datetime.datetime(year=today.year - 3, month=1, day=1)

    script_nop = "\
        SELECT customers.name, SUM(sales.{})\
        FROM sales\
        LEFT JOIN customers\
        ON sales.customer_id=customers.id\
        WHERE sales.date BETWEEN DATE('{}') AND DATE('{}')\
        GROUP BY customers.name;\
        ".format('price', tyb, today)

    cur.execute(script_nop)
    _data = cur.fetchall()
    d = dict()
    for i in range(len(_data)):
        d[_data[i][0]] = round(_data[i][1], 2)

    return d


def monthlyParam(cur, param='price', yearMin=2008, year=2015, account='all'):
    '''
    '''

    yearMin = year

    if account != 'all':
        script_sales = "\
            SELECT MONTH(sales.date), SUM(sales.{0}) AS NumberOfProducts FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.id = '{1}' AND YEAR(sales.date) BETWEEN {2} AND {3}\
            GROUP BY sales.month;\
            ".format(param, account, yearMin, year)
    else:
        script_sales = "\
            SELECT MONTH(sales.date), SUM(sales.{}) AS NumberOfProducts FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE YEAR(sales.date) BETWEEN {} AND {}\
            GROUP BY sales.month;\
            ".format(param, yearMin, year)

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


def salesYTD(cur, param='price', account=None):
    '''
    '''
    today = str(datetime.datetime.now()).split(" ")[0]
    # today = str(datetime.datetime.now())
    firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))
    # firstday = str(datetime.datetime(datetime.datetime.now().year, 1, 1))

    if account == 'all':
        script_nop = "\
            SELECT SUM(sales.{})\
            FROM sales\
            WHERE DATE(sales.date) BETWEEN '{}' AND '{}'\
            ".format(param, firstday, today)
    else:
        script_nop = "\
            SELECT customers.name, SUM(sales.{})\
            FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.name = '{}' AND DATE(sales.date) BETWEEN '{}' AND '{}';\
            ".format(param, account, firstday, today)
        # GROUP BY customers.name;\

    cur.execute(script_nop)
    _data = cur.fetchall()

    d = dict()
    try:
        if _data[0][0] == None:
            d = 0
        else:
            for i in range(len(_data)):
                d[_data[i][0]] = round(_data[i][1], 2)
    except:
        d = 0

    return d


def salesMTD(cur, param='price', account='all'):
    '''
    '''
    month = str(datetime.datetime.now().month)
    year = str(datetime.datetime.now().year)

    if account == 'all':
        script_nop = "\
            SELECT SUM(sales.{}) from sales\
            WHERE MONTH(sales.date)={} AND YEAR(sales.date)={};\
            ".format(param, month, year)
    else:
        script_nop = "\
            SELECT SUM(sales.{}) FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.name = '{}' AND MONTH(sales.date)={} AND YEAR(sales.date)={};\
            ".format(param, account, month, year)
        # GROUP BY customers.name;\

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        if _data[0][0] == None:
            return 0
        else:
            return round(_data[0][0], 2)
    except:
        return 0


def salesQTD(cur, param='price', year=None, account='all'):
    '''
    '''
    if year == None:
        year = datetime.datetime.now().year

    year = str(year)

    today = str(datetime.datetime.now()).split(" ")[0]

    if account == 'all':
        script_nop = "\
        SELECT SUM(sales.{}) from sales\
        WHERE QUARTER(sales.date)<=QUARTER('{}') AND YEAR(sales.date)='{}';\
        ".format(param, today, year)
    else:
        script_nop = "\
            SELECT customers.name, SUM(sales.{}) FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.name = '{}' AND QUARTER(sales.date)<=QUARTER('{}') AND YEAR(sales.date)='{}'\
            GROUP BY customers.name;\
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


def salesPerQuarter(cur, param='price', year=None, account='all'):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

    if account == 'all':
        script_nop = "\
            SELECT QUARTER(sales.date), SUM(sales.{}) from sales\
            WHERE YEAR(sales.date)='{}'\
            GROUP BY QUARTER(sales.date);\
            ".format(param, year)
    else:
        # SELECT customers.name, QUARTER(sales.date), SUM(sales.{}) FROM sales\
        script_nop = "\
            SELECT QUARTER(sales.date), SUM(sales.{}) FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE customers.name = '{}' AND YEAR(sales.date)='{}'\
            GROUP BY QUARTER(sales.date);\
            ".format(param, account, year)
        # GROUP BY customers.name;\

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
        return 0

    if 1 not in d.keys():
        d[1] = 0.0
    if 2 not in d.keys():
        d[2] = 0.0
    if 3 not in d.keys():
        d[3] = 0.0
    if 4 not in d.keys():
        d[4] = 0.0

    return d


def activeAccounts(cur, param='price', today=None):
    '''
    '''
    if today == None:
        today = str(datetime.datetime.now()).split(" ")[0]
        today = datetime.datetime.now()
        tmb = datetime.datetime.now()
    else:
        y = today.year
        m = today.month
        d = today.day
        today = datetime.datetime(year=y, month=m, day=d)
        tmb = datetime.datetime(year=y, month=m, day=d)

    dif = today.month - 3
    if dif <= 0:
        m = 12 + dif
        y = today.year - 1
        tmb = datetime.datetime(year=y, month=m, day=today.day)
    else:
        tmb = datetime.datetime(year=today.year, month=dif, day=today.day)

    script_nop = "\
        SELECT customers.name, SUM(sales.{})\
        FROM sales\
        LEFT JOIN customers\
        ON sales.customer_id=customers.id\
        WHERE sales.date BETWEEN DATE('{}') AND DATE('{}')\
        GROUP BY customers.name;\
        ".format(param, tmb, today)

    cur.execute(script_nop)
    _data = cur.fetchall()
    d = dict()
    for i in range(len(_data)):
        d[_data[i][0]] = round(_data[i][1], 2)

    return d


def goalsPerQuarter(cur, minYear=None, maxYear=None, account='all'):
    '''
    '''
    if minYear == None:
        minYear = str(datetime.datetime.now().year)
        # minYear = 2016

    if maxYear == None:
        maxYear = minYear

    if account == 'all':
        script_nop = "\
            SELECT QUARTER(due), SUM(goal) from plans\
            WHERE YEAR(due) BETWEEN {} AND {}\
            GROUP BY QUARTER(due);\
            ".format(minYear, maxYear)
    else:
        script_nop = "\
            SELECT QUARTER(due), SUM(goal) from plans\
            WHERE YEAR(due) BETWEEN {} AND {} AND account='{}'\
            GROUP BY QUARTER(due);\
            ".format(minYear, maxYear, account)

        # GROUP BY YEAR(due), MONTH(due);\

    cur.execute(script_nop)
    _data = cur.fetchall()
    # d = dict()
    # for i in range(len(_data)):
    # d[_data[i][0]] = int(_data[i][1])
    #
    # return d
    try:
        # return int(_data[0][0])
        d = dict()
        print(_data)
        for i in range(len(_data)):
            d[int(_data[i][0])] = int(_data[i][1])

        if d == {}:
            today = datetime.datetime.now()
            quarter = (today.month - 1) // 3 + 1
            for q in range(1, quarter + 1):
                d[q] = 0
    except:
        return 0

    if 1 not in d.keys():
        d[1] = 0.0
    if 2 not in d.keys():
        d[2] = 0.0
    if 3 not in d.keys():
        d[3] = 0.0
    if 4 not in d.keys():
        d[4] = 0.0

    return d


def actionsPerYear(cur, account='all'):
    '''
    '''

    if account == 'all':
        script_nop = "\
            SELECT YEAR(due), COUNT(action) from tasks\
            GROUP BY YEAR(due);\
            "
    else:
        script_nop = "\
            SELECT YEAR(due), COUNT(action) from tasks\
            WHERE account = '{}'\
            GROUP BY YEAR(due);\
            ".format(account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        d = dict()
        for i in range(len(_data)):
            d[int(_data[i][0])] = int(_data[i][1])
    except:
        return 0

    return d


def actionsQTD(cur, year=None, account='all'):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

    today = str(datetime.datetime.now()).split(" ")[0]

    if account == 'all':
        script_nop = "\
            SELECT COUNT(action) from tasks\
            WHERE QUARTER(tasks.due)=QUARTER('{0}') AND DATE(tasks.due)<='{0}' AND YEAR(tasks.due)='{1}';\
            ".format(today, year)
    else:
        script_nop = "\
            SELECT COUNT(action) from tasks\
            WHERE QUARTER(tasks.due)=QUARTER('{0}') AND DATE(tasks.due)<='{0}' AND YEAR(tasks.due)='{1}' AND account='{2}';\
            ".format(today, year, account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    return int(_data[0][0])


def actionsMTD(cur, year=None, account='all'):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)

    if account == 'all':
        script_nop = "\
            SELECT COUNT(action) from tasks\
            WHERE MONTH(tasks.due)<={} AND YEAR(tasks.due) BETWEEN {} AND {}\
            ".format(month, year, year)
    else:
        script_nop = "\
            SELECT COUNT(action) from tasks\
            WHERE MONTH(tasks.due)<={} AND YEAR(tasks.due) BETWEEN {} AND {} AND account='{}';\
            ".format(month, year, year, account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        return int(_data[0][0])
    except:
        return 0


def actionsYTD(cur, account='all'):
    '''
    '''
    today = str(datetime.datetime.now()).split(" ")[0]
    firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))

    if account == 'all':
        script_nop = "\
            SELECT COUNT(id) from tasks\
            WHERE DATE(tasks.due) BETWEEN '{}' AND '{}';\
            ".format(firstday, today)
    else:
        script_nop = "\
            SELECT COUNT(id) from tasks\
            WHERE DATE(tasks.due) BETWEEN '{}' AND '{}' AND account='{}';\
            ".format(firstday, today, account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        return int(_data[0][0])
    except:
        return 0


def actionsPerMonth(cur, year=None, account='all'):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

    if account == 'all':
        script_nop = "\
            SELECT MONTH(due), COUNT(action) from tasks\
            WHERE YEAR(tasks.due) BETWEEN {} AND {}\
            GROUP BY MONTH(due);\
            ".format(year, year)
    else:
        script_nop = "\
            SELECT MONTH(due), COUNT(action) from tasks\
            WHERE YEAR(tasks.due) BETWEEN {} AND {} AND account='{}'\
            GROUP BY MONTH(due);\
            ".format(year, year, account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        d = dict()
        for i in range(len(_data)):
            d[int(_data[i][0])] = int(_data[i][1])
        return d
    except:
        return 0


def actionsPerDay(cur, year=None, yearMax=None, account='all'):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)
    if yearMax == None:
        yearMax = year

    if account == 'all':
        script_nop = "\
            SELECT DATE(due), COUNT(action) from tasks\
            WHERE YEAR(tasks.due) BETWEEN {} AND {}\
            GROUP BY DATE(due);\
            ".format(year, yearMax)
    else:
        script_nop = "\
            SELECT DATE(due), COUNT(action) from tasks\
            WHERE YEAR(tasks.due) BETWEEN {} AND {} AND account='{}'\
            GROUP BY DATE(due);\
            ".format(year, yearMax, account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        d = dict()
        for i in range(len(_data)):
            d[str(_data[i][0])] = int(_data[i][1])
        return d
    except:
        return 0


def totalPlanGoals(cur, account='all'):
    '''
    '''

    if account == 'all':
        script_nop = "\
            SELECT SUM(goal) FROM plans;\
            "
    else:
        script_nop = "\
            SELECT SUM(goal) FROM plans\
            WHERE account='{}';\
            ".format(account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        return float(_data[0][0])
    except:
        return 0


def totalVisitsGoal(cur, year=None, account='all'):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

    if account == 'all':
        script_nop = "\
            SELECT SUM(visits) FROM plans\
            WHERE YEAR(due) BETWEEN {} AND {};\
            ".format(year, year)
    else:
        script_nop = "\
            SELECT SUM(visits) FROM plans\
            WHERE YEAR(due) BETWEEN {} AND {} AND account='{}';\
            ".format(year, year, account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        return int(_data[0][0])
    except:
        return 0


def totalCallsGoal(cur, year=None, account='all'):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

    if account == 'all':
        script_nop = "\
            SELECT SUM(calls) FROM plans\
            WHERE YEAR(due) BETWEEN {} AND {};\
            ".format(year, year)
    else:
        script_nop = "\
            SELECT SUM(calls) FROM plans\
            WHERE YEAR(due) BETWEEN {} AND {} AND account='{}';\
            ".format(year, year, account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        return int(_data[0][0])
    except:
        return 0


def totalOffersGoal(cur, year=None, account='all'):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

    if account == 'all':
        script_nop = "\
            SELECT SUM(offers) FROM plans\
            WHERE YEAR(due) BETWEEN {} AND {};\
            ".format(year, year)
    else:
        script_nop = "\
            SELECT SUM(offers) FROM plans\
            WHERE YEAR(due) BETWEEN {} AND {} AND account='{}';\
            ".format(year, year, account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        return int(_data[0][0])
    except:
        return 0


def totalSalesPlans(cur, account='all'):
    '''
    '''

    if account == 'all':
        script_nop = "\
            SELECT COUNT(*) FROM plans;\
            "
    else:
        script_nop = "\
            SELECT COUNT(*) FROM plans\
            WHERE account='{}';\
            ".format(account)

    cur.execute(script_nop)

    try:
        return int(cur.fetchall()[0][0])
    except:
        return 0


def plansPerAccount(cur):
    '''
    '''
    script_nop = "\
        SELECT account, COUNT(*) FROM plans GROUP BY account;\
        "
    cur.execute(script_nop)

    _data = cur.fetchall()
    d = dict()
    for i in range(len(_data)):
        d[_data[i][0]] = int(_data[i][1])

    # data['actions per account'] = np.asarray(cur.fetchall()[0])
    # data['actions per account'] = np.asarray[cur.fetchall()]
    return d


def actionsPerAccount(cur):
    '''
    '''
    script_nop = "\
        SELECT account, COUNT(*) FROM tasks GROUP BY account;\
        "
    cur.execute(script_nop)

    _data = cur.fetchall()
    d = dict()
    for i in range(len(_data)):
        d[_data[i][0]] = int(_data[i][1])

    # data['actions per account'] = np.asarray(cur.fetchall()[0])
    # data['actions per account'] = np.asarray[cur.fetchall()]
    return d


def activityGoals(cur, account='all'):
    '''
    '''

    if account == 'all':
        script_nop = "\
            SELECT action, COUNT(*) FROM tasks GROUP BY action;\
            "
    else:
        script_nop = "\
            SELECT action, COUNT(*) FROM tasks\
            WHERE account = '{}'\
            GROUP BY action;\
            ".format(account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        d = dict()
        for i in range(len(_data)):
            d[_data[i][0]] = int(_data[i][1])
        return d
    except:
        raise
        # return 0


if __name__ == "__main__":

    import json

    # data = getInsights(username='test', local=True)
    data = getInsights(username='test', local=True, account='Acrion')
    # print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    print(json.dumps(data))

    data = getInsights(username='test', local=True, account='all')
    # print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    print(json.dumps(data))

    username = 'martin_masip'
    dbname = 'data_userID_{}_data_test_super_reduced_8_xlsx'.format(username)
    mysql_connection = connection.MySQLConnection(dbname)
    con = mysql_connection.connect()
    cur = con.cursor()

    today = datetime.datetime.now()
    account = 'Acrion'
    salesLastQuarter = salesPerQuarter(cur, year=today.year - 1, param='price', account=account)[4]
    print(salesLastQuarter)
    salesLastQuarter = salesPerQuarter(cur, year=today.year, param='price', account=account)[4]
    print(salesLastQuarter)

    # data = getInsightsPerCustomer(username='test', local=True, account='all')
    # print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

    # data = getInsightsPerCustomer(username='test', local=True, account='Acrion')
    # print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

    if False:
        username = 'test'
        dbname = 'data_userID_{}'.format(username)
        con = mysql.connect('localhost', 'webadmin', 'Qymatix!!!', dbname);
        cur = con.cursor()

        d = monthlyParam(cur, param='price', yearMin=2008, year=2015, account='Metro')
        print(d)

        d = salesPerQuarter(cur, param='price', year=2015, account='Zama')
        print("///")
        print(d)
