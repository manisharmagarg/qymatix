import datetime
import os
import sys

from api.infrastructure.mysql import connection

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


def monthdelta(date, delta):
    m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
    if not m: m = 12
    d = min(date.day,
            [31, 29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date.replace(day=d, month=m, year=y)


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


def accounts_name(cur, username=''):
    '''
    '''
    if username in ['', 'admin']:
        script_nop = "\
            SELECT customers.name\
            FROM customers;\
            "
    else:
        cust = getCustomersList(cur, username)
        script_nop = "\
            SELECT customers.name\
            FROM customers\
            WHERE customers.id IN {0};\
            ".format(cust)

    cur.execute(script_nop)
    _data = cur.fetchall()

    d = [i[0] for i in _data]

    return d


def accountsThreeYD(cur, account='all', username=''):
    '''
    '''

    today = str(datetime.datetime.now()).split(" ")[0]
    today = datetime.datetime.now()
    tyb = datetime.datetime(year=today.year - 3, month=1, day=1)

    if username in ['', 'admin']:
        script_nop = "\
            SELECT customers.id, SUM(sales.{})\
            FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE sales.date BETWEEN DATE('{}') AND DATE('{}')\
            GROUP BY customers.id;\
            ".format('price', tyb, today)
    else:
        # cust = getCustomersList(cur, username)
        cust = tuple(accounts(cur, username))
        script_nop = "\
            SELECT customers.id, SUM(sales.{})\
            FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE sales.date BETWEEN DATE('{}') AND DATE('{}') AND customers.id IN {}\
            GROUP BY customers.id;\
            ".format('price', tyb, today, cust)

    cur.execute(script_nop)
    _data = cur.fetchall()
    d = dict()
    for i in range(len(_data)):
        d[_data[i][0]] = round(_data[i][1], 2)

    return d


def activeAccounts(cur, param='price', today=None, username=''):
    '''
    '''
    if today != None:
        y = today.year
        m = today.month
        d = today.day
        today = datetime.datetime(year=y, month=m, day=d)
        tmb = datetime.datetime(year=y, month=m, day=d)
    else:
        today = str(datetime.datetime.now()).split(" ")[0]
        today = datetime.datetime.now()
        tmb = datetime.datetime.now()

    '''
    dif = today.month - 3
    if dif <= 0:
        m = 12 + dif
        y = today.year - 1
        tmb = datetime.datetime(year=y, month=m, day=today.day)
    else:
        #tmb = datetime.datetime(year=today.year, month=dif, day=today.day)
    '''
    tmb = monthdelta(today, -3)

    if username in ['', 'admin']:
        script_nop = "\
            SELECT customers.id, SUM(sales.{})\
            FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE sales.date BETWEEN DATE('{}') AND DATE('{}')\
            GROUP BY customers.id;\
            ".format(param, tmb, today)
    else:
        cust = getCustomersList(cur, username)
        script_nop = "\
            SELECT customers.id, SUM(sales.{})\
            FROM sales\
            LEFT JOIN customers\
            ON sales.customer_id=customers.id\
            WHERE sales.date BETWEEN DATE('{}') AND DATE('{}') AND customers.id IN {}\
            GROUP BY customers.id;\
            ".format(param, tmb, today, cust)

    cur.execute(script_nop)
    _data = cur.fetchall()
    active_accounts = dict()
    for i in range(len(_data)):
        active_accounts[_data[i][0]] = round(_data[i][1], 2)

    return active_accounts


def activeAccountsCRM(cur, param='price', when=None, username=''):
    '''
    '''

    if when == None:
        today = str(datetime.datetime.now()).split(" ")[0]
        today = datetime.datetime.now()
        # tmb = datetime.datetime.now()
    else:
        y = when.year
        m = when.month
        d = when.day
        today = datetime.datetime(year=y, month=m, day=d)
        # tmb = datetime.datetime(year=y, month=m, day=d)

    tmb = monthdelta(today, -3)

    script_nop = "\
        SELECT plans.account, SUM(plans.goal)\
        FROM plans\
        WHERE plans.due BETWEEN DATE('{0}') AND DATE('{1}') OR plans.created >= DATE('{0}')\
        GROUP BY plans.account;\
        ".format(tmb, today)

    if username in ['', 'admin']:
        script_nop = "\
            SELECT tasks.account, COUNT(tasks.due)\
            FROM tasks\
            WHERE tasks.due BETWEEN DATE('{0}') AND DATE('{1}') OR tasks.created >= DATE('{0}')\
            GROUP BY tasks.account;\
            ".format(tmb, today)
    else:
        cust = getCustomersList(cur, username)
        script_nop = "\
            SELECT tasks.account, COUNT(tasks.due)\
            FROM tasks\
            WHERE tasks.due BETWEEN DATE('{0}') AND DATE('{1}') OR tasks.created >= DATE('{0}') AND tasks.id IN {2}\
            GROUP BY tasks.account;\
            ".format(tmb, today, cust)

    # print(script_nop)

    try:
        cur.execute(script_nop)
        _data = cur.fetchall()
        d = dict()
        for i in range(len(_data)):
            d[_data[i][0]] = round(_data[i][1], 2)
    except Exception as e:
        # raise
        print(e)
        d = {}

    return d


def goalsPerQuarter(cur, minYear=None, maxYear=None, account='all', username=''):
    '''
    '''
    if minYear == None:
        minYear = str(datetime.datetime.now().year)
        # minYear = 2016

    if maxYear == None:
        maxYear = minYear

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
                SELECT QUARTER(due), SUM(goal) from plans\
                WHERE YEAR(due) BETWEEN {} AND {}\
                GROUP BY QUARTER(due);\
                ".format(minYear, maxYear)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT QUARTER(due), SUM(goal) from plans\
                WHERE YEAR(due) BETWEEN {} AND {} AND account IN {}\
                GROUP BY QUARTER(due);\
                ".format(minYear, maxYear, cust)
    else:
        script_nop = "\
            SELECT QUARTER(due), SUM(goal) from plans\
            WHERE YEAR(due) BETWEEN {} AND {} AND account='{}'\
            GROUP BY QUARTER(due);\
            ".format(minYear, maxYear, account)

        # GROUP BY YEAR(due), MONTH(due);\

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
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


def actionsPerYear(cur, account='all', username=None):
    '''
    '''

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
                SELECT YEAR(due), COUNT(action) from tasks\
                GROUP BY YEAR(due);\
                "
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT YEAR(due), COUNT(action) from tasks\
                WHERE account IN {}\
                GROUP BY YEAR(due);\
                ".format(cust)

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


def actionsQTD(cur, year=None, account='all', username=''):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

    today = str(datetime.datetime.now()).split(" ")[0]

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
                SELECT COUNT(action) from tasks\
                WHERE QUARTER(tasks.due)=QUARTER('{0}') AND DATE(tasks.due)<='{0}' AND YEAR(tasks.due)='{1}';\
                ".format(today, year)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT COUNT(action) from tasks\
                WHERE QUARTER(tasks.due)=QUARTER('{0}') AND DATE(tasks.due)<='{0}' AND YEAR(tasks.due)='{1}' AND account IN {2};\
                ".format(today, year, cust)

    else:
        script_nop = "\
            SELECT COUNT(action) from tasks\
            WHERE QUARTER(tasks.due)=QUARTER('{0}') AND DATE(tasks.due)<='{0}' AND YEAR(tasks.due)='{1}' AND account='{2}';\
            ".format(today, year, account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    return int(_data[0][0])


def actionsMTD(cur, year=None, account='all', username=''):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)

    '''
    try:
        account = account.decode('utf-8')
    except:
        pass
    account = account.encode('latin-1')
    '''

    if account == 'all':
        # WHERE due BETWEEN DATE_SUB(CURDATE(), INTERVAL {3} DAY) AND CURDATE();\
        if username in ['', 'admin']:
            script_nop = "\
                SELECT COUNT(id) from tasks\
                WHERE MONTH(tasks.due)={1} AND YEAR(tasks.due)={0} AND DAY(tasks.due)<={2};\
                ".format(year, month, int(day))
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT COUNT(id) from tasks\
                WHERE MONTH(tasks.due)={1} AND YEAR(tasks.due)={0} AND DAY(tasks.due)<={2} AND account IN {3};\
                ".format(year, month, day, cust)

    else:
        # WHERE due BETWEEN DATE_SUB(CURDATE(), INTERVAL 31 DAY) AND CURDATE() AND account='{3}';\
        script_nop = "\
            SELECT COUNT(id) from tasks\
            WHERE MONTH(tasks.due)={1} AND YEAR(tasks.due)={0} AND DAY(tasks.due)<={2} AND account='{3}';\
            ".format(year, month, day, account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        return int(_data[0][0])
    except:
        return 0


def actionsYTD(cur, account='all', username=''):
    '''
    '''
    today = str(datetime.datetime.now()).split(" ")[0]
    firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))

    if account == 'all':
        if username in ['', 'admin']:
            script_nop = "\
                SELECT COUNT(id) from tasks\
                WHERE DATE(tasks.due) BETWEEN '{}' AND '{}';\
                ".format(firstday, today)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT COUNT(id) from tasks\
                WHERE DATE(tasks.due) BETWEEN '{}' AND '{}' AND account IN {};\
                ".format(firstday, today, cust)

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


def actionsPerMonth(cur, year=None, account='all', username=''):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

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
                SELECT MONTH(due), COUNT(action) from tasks\
                WHERE YEAR(tasks.due) BETWEEN {} AND {}\
                GROUP BY MONTH(due);\
                ".format(year, year)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT MONTH(due), COUNT(action) from tasks\
                WHERE YEAR(tasks.due) BETWEEN {} AND {} AND account IN {}\
                GROUP BY MONTH(due);\
                ".format(year, year, cust)

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


def actionsPerDay(cur, year=None, yearMax=None, account='all', username=''):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)
    if yearMax == None:
        yearMax = year

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
                SELECT DATE(due), COUNT(action) from tasks\
                WHERE YEAR(tasks.due) BETWEEN {} AND {}\
                GROUP BY DATE(due);\
                ".format(year, yearMax)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT DATE(due), COUNT(action) from tasks\
                WHERE YEAR(tasks.due) BETWEEN {} AND {} AND account IN {}\
                GROUP BY DATE(due);\
                ".format(year, yearMax, cust)

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


def totalPlanGoals(cur, account='all', username=''):
    '''
    '''

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
                SELECT SUM(goal) FROM plans;\
                "
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT SUM(goal) FROM plans\
                WHERE account IN {};\
                ".format(cust)

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


def totalVisitsGoal(cur, year=None, account='all', username=''):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

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
                SELECT SUM(visits) FROM plans\
                WHERE YEAR(due) BETWEEN {} AND {};\
                ".format(year, year)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT SUM(visits) FROM plans\
                WHERE YEAR(due) BETWEEN {} AND {} AND account IN {};\
                ".format(year, year, cust)

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


def totalCallsGoal(cur, year=None, account='all', username=''):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

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
                SELECT SUM(calls) FROM plans\
                WHERE YEAR(due) BETWEEN {} AND {};\
                ".format(year, year)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT SUM(calls) FROM plans\
                WHERE YEAR(due) BETWEEN {} AND {} AND account IN {};\
                ".format(year, year, cust)

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


def totalOffersGoal(cur, year=None, account='all', username=''):
    '''
    '''
    if year == None:
        year = str(datetime.datetime.now().year)

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
                SELECT SUM(offers) FROM plans\
                WHERE YEAR(due) BETWEEN {} AND {};\
                ".format(year, year)
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT SUM(offers) FROM plans\
                WHERE YEAR(due) BETWEEN {} AND {} AND account IN {};\
                ".format(year, year, cust)
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


def totalSalesPlans(cur, account='all', username=''):
    '''
    '''

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
                SELECT COUNT(*) FROM plans;\
                "
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT COUNT(*) FROM plans\
                WHERE account IN {};\
                ".format(cust)

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


def plansPerAccount(cur, username=''):
    '''
    '''
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '')

    if username in ['', 'admin']:
        # SELECT account, COUNT(*) FROM plans GROUP BY account;\
        # "
        script_nop = "\
            SELECT c.id, COUNT(*) FROM plans AS p\
            LEFT JOIN {0}.customers AS c ON p.account = c.id\
            GROUP BY account;\
            ".format('data_' + dbname)
    else:
        print('else wali query')
        cust = getCustomersList(cur, username)
        script_nop = "\
            SELECT c.id, COUNT(*) FROM plans AS p\
            LEFT JOIN {0}.customers AS c ON p.account = c.id\
            WHERE account IN {1}\
            GROUP BY account;\
            ".format('data_' + dbname, cust)

    cur.execute(script_nop)

    _data = cur.fetchall()
    plan_per_account = dict()
    for i in range(len(_data)):
        # plan_per_account[_data[i][0]] = int(_data[i][1])
        plan_per_account["{}".format(_data[i][0])] = int(_data[i][1])

    # data['actions per account'] = np.asarray(cur.fetchall()[0])
    # data['actions per account'] = np.asarray[cur.fetchall()]
    return plan_per_account


def actionsPerAccount(cur, username):
    '''
    '''

    if username in ['', 'admin']:
        script_nop = "\
            SELECT account, COUNT(*) FROM tasks GROUP BY account;\
            "
    else:
        cust = getCustomersList(cur, username)
        script_nop = "\
            SELECT account, COUNT(*) FROM tasks WHERE account IN {} GROUP BY account;\
            ".format(cust)
    cur.execute(script_nop)

    _data = cur.fetchall()
    actions_per_account = dict()
    for i in range(len(_data)):
        actions_per_account[_data[i][0]] = int(_data[i][1])

    return actions_per_account


def activityGoals(cur, account='all', username=''):
    '''
    '''

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
                SELECT action, COUNT(*) FROM tasks GROUP BY action;\
                "
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT action, COUNT(*) FROM tasks\
                WHERE account IN {}\
                GROUP BY action;\
                ".format(cust)

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


def averageDealTime(cur, account='all', username=''):
    '''
    '''
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
                SELECT plans.created, plans.due FROM plans;\
                "
        else:
            cust = getCustomersList(cur, username)
            script_nop = "\
                SELECT plans.created, plans.due FROM plans\
                WHERE account IN {};\
                ".format(cust)

    else:
        script_nop = "\
            SELECT plans.created, plans.due FROM plans\
            WHERE account='{}';\
            ".format(account)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        _diff = [d[1] - d[0] for d in _data]
        avgLifetime = sum([d.days for d in _diff]) / len(_diff)
        return avgLifetime
        # return _data
    except:
        return 0


def closedPlans(cur, account='all', status='all', username=''):
    '''
    '''
    '''
    try:
        account = account.decode('utf-8')
    except:
        pass
    account = account.encode('latin-1')
    '''

    if account == 'all':
        if username in ['', 'admin']:
            if status == 'all':
                script_nop = "\
                    SELECT COUNT(plans.id) FROM plans WHERE plans.status='Closed Lost' OR plans.status='Closed Won';\
                    "
            else:
                script_nop = "\
                    SELECT COUNT(plans.id) FROM plans WHERE plans.status='{}';\
                    ".format(status)
        else:
            cust = getCustomersList(cur, username)
            if status == 'all':
                script_nop = "\
                    SELECT plans.id FROM plans\
                    WHERE (plans.status='Closed Lost' OR plans.status='Closed Won') AND account IN {};\
                    ".format(cust)
            else:
                script_nop = "\
                    SELECT plans.id FROM plans\
                    WHERE plans.status='{1}' AND account IN {0};\
                    ".format(cust, status)
    else:
        if status == 'all':
            script_nop = "\
                SELECT plans.id FROM plans\
                WHERE (plans.status='Closed Lost' OR plans.status='Closed Won') AND account='{}';\
                ".format(account)
        else:
            script_nop = "\
                SELECT plans.id FROM plans\
                WHERE plans.status='{1}' AND account='{0}';\
                ".format(account, status)

    cur.execute(script_nop)
    _data = cur.fetchall()

    try:
        closed = int(_data[0][0])
        return closed
        # return _data
    except:
        return 0


if __name__ == "__main__":
    dbname = 'data_crmtest1'
    dbname = 'data_martinmasip'
    dbname = 'data_demo'
    dbname = 'data_qymatix_best'
    dbname = 'data_qymatix_de'
    dbname = 'data_qymatix_de'

    mysql_connection = connection.MySQLConnection(dbname)
    con = mysql_connection.connect()
    cur = con.cursor()

    # today = datetime.datetime.now()
    # account = 'Acrion'
    # ans = averageDealTime(cur)
    # print(ans)
    ##ans = actionsPerDay(cur)
    # print(ans)
    # status = 'Closed Won'
    # status = 'Closed Lost'
    # status = 'all'
    # ans = closedPlans(cur, status=status)
    # print(ans)
    # ans = activeAccountsCRM(cur)
    # ans = activeAccounts(cur)
    ans = accounts(cur, username='lucas_pedretti__qymatix_de')
    # ans = accounts(cur, username='admin')
    print("<<<")
    print(ans)
    # print(str(tuple(ans)))
    # ans = goalsPerQuarter(cur, account='all', username='lucas_pedretti__qymatix_de')
    # print(ans)
    # ans = actionsPerYear(cur, account='all', username='lucas_pedretti__qymatix_de')
    # ans = actionsPerYear(cur, account='all', username='admin')
    # print(ans)
