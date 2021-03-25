import datetime
import logging

import numpy as np
from performance_analytics import kam
from performance_analytics import multiparam
from performance_analytics import sales

from api.infrastructure.mysql import connection

logger = logging.getLogger(__name__)


def getInsights(dbname, account='all', username='', passwd=''):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    dbname = 'data_{}'.format(dbname)
    dbname_results = dbname
    dbname_tasks = dbname.replace('tasks', 'data')

    # username = ''
    # passwd = ''

    data = dict()

    # try:
    # account = account.decode('utf-8')
    # except:
    # pass
    # account = account.encode('latin-1')

    try:

        logging.debug(dbname)

        mysql_connection = connection.MySQLConnection(dbname_results)
        con = mysql_connection.connect()
        cur = con.cursor()

        logging.debug(con)

        if account == 'all':
            data['plans per account'] = kam.plansPerAccount(cur)
            data['actions per account'] = kam.actionsPerAccount(cur)

        data['activity goals'] = kam.activityGoals(cur, account=account)
        data['total sales plans'] = kam.totalSalesPlans(cur, account=account)
        data['total plan goals'] = kam.totalPlanGoals(cur, account=account)

        data['actions per day'] = kam.actionsPerDay(cur, account=account)
        data['actions per month'] = kam.actionsPerMonth(cur, account=account)
        data['actions per year'] = kam.actionsPerYear(cur, account=account)

        data['goals per quarter'] = kam.goalsPerQuarter(cur, account=account)
        data['total calls goal'] = kam.totalCallsGoal(cur, account=account)
        data['total visits goal'] = kam.totalVisitsGoal(cur, account=account)
        data['total offers goal'] = kam.totalOffersGoal(cur, account=account)

        month = str(datetime.datetime.now().month)
        try:
            data['actions this month'] = data['actions per month'][month]
        except:
            data['actions this month'] = 0

        data['actions QTD'] = kam.actionsQTD(cur, account=account)
        data['actions MTD'] = kam.actionsMTD(cur, account=account)
        data['actions YTD'] = kam.actionsYTD(cur, account=account)

        today = str(datetime.datetime.now()).split(" ")[0]
        firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))
        wd = np.busday_count(firstday, today) * 1.0
        data['actions YTD date ratio'] = round(data['actions YTD'] / wd, 2)


    except Exception as e:
        # print("!!!!>>>>>")
        # print("Error {0}: {1}".format(e.args[0], e.args[1]))

        if account == 'all':
            data['plans per account'] = "{}"
            data['actions per account'] = "{}"

        data['activity goals'] = 0
        data['total sales plans'] = 0
        data['total plan goals'] = 0
        data['actions per day'] = 0
        data['actions per month'] = 0
        data['actions per year'] = 0
        data['goals per quarter'] = 0
        data['total calls goal'] = 0
        data['total visits goal'] = 0
        data['total offers goal'] = 0
        data['actions this month'] = 0
        data['actions QTD'] = 0
        data['actions MTD'] = 0
        data['actions YTD'] = 0
        data['actions YTD date ratio'] = 0

    finally:
        try:
            con.close()
        except:
            print('No Db connection possible')
            pass

    try:
        mysql_connection = connection.MySQLConnection(dbname_tasks)
        con = mysql_connection.connect()
        cur = con.cursor()

        today = datetime.datetime.now()

        # list of all accounts
        if account == 'all':
            data['accounts'] = kam.accounts(cur)
            # active accounts and sales in the las 3 months
            data['active accounts'] = kam.activeAccounts(cur)
            hoy = datetime.datetime.now()
            _tmb = datetime.datetime(year=hoy.year, month=hoy.month, day=hoy.day)
            try:
                data['active accounts growth'] = 100. * (
                            len(data['active accounts'].keys()) / len(kam.activeAccounts(cur, today=_tmb).keys()) - 1)
            except:
                data['active accounts growth'] = 0

            data['lost accounts'] = [a for a in data['accounts'] if a not in data['active accounts'].keys()]
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

        try:
            data['sales YTD'] = round(sales.salesYTD(cur, account=account), 2)
        except:
            data['sales YTD'] = 0.0
        try:
            data['margin YTD'] = round(sales.salesYTD(cur, param='margin', account=account), 2)
        except:
            data['margin YTD'] = 0.0
        try:
            data['sales QTD'] = round(sales.salesQTD(cur, year=today.year, account=account), 2)
        except:
            data['sales QTD'] = 0.0
        try:
            data['margin QTD'] = round(sales.salesQTD(cur, param='margin', year=today.year, account=account), 2)
        except:
            data['margin QTD'] = 0.0
        try:
            data['sales MTD'] = round(sales.salesMTD(cur, account=account), 2)
        except:
            data['sales MTD'] = 0.0
        data['sales per quarter'] = sales.salesPerQuarter(cur, param='price', year=today.year, account=account)
        data['margin per quarter'] = sales.salesPerQuarter(cur, param='margin', year=today.year, account=account)

        data['monthly sales'] = multiparam.monthlyParam(cur, param='price', year=today.year, account=account)
        data['monthly sales last year'] = multiparam.monthlyParam(cur, param='price', year=today.year - 1,
                                                                  account=account)

        data['monthly margin'] = multiparam.monthlyParam(cur, param='margin', year=today.year, account=account)
        data['monthly margin last year'] = multiparam.monthlyParam(cur, param='margin', year=today.year - 1,
                                                                   account=account)

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
            salesLastQuarter = round(sales.salesPerQuarter(cur, year=today.year - 1, param='price', account=account)[4],
                                     2)
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
            marginLastQuarter = round(
                sales.salesPerQuarter(cur, year=today.year - 1, param='margin', account=account)[4], 2)
        else:
            marginLastQuarter = round(data['margin per quarter'][currentQuarter - 1], 2)

        try:
            data['margin growth QTD'] = round(100 * marginCurrentQuarter / marginLastQuarter, 2)
        except:
            data['margin growth QTD'] = 0.0

        # PIPELINE

        data['pipelines'] = sales._pipelines()

    except Exception as e:
        raise
        # print("Error {0}: {1}".format(e.args[0], e.args[1]))
        # data = {}
        data['sales YTD'] = 0
        data['margin YTD'] = 0
        data['sales QTD'] = 0
        data['margin QTD'] = 0
        data['sales MTD'] = 0
        data['sales per quarter'] = 0
        data['margin per quarter'] = 0
        data['monthly sales'] = 0
        data['monthly sales last year'] = 0
        data['monthly margin'] = 0
        data['monthly margin last year'] = 0
        data['sales last year'] = 0
        data['sales growth YTD'] = 0.0
        data['sales growth month'] = 0.0
        data['margin last year'] = 0.0
        data['margin growth YTD'] = 0.0
        data['margin growth month'] = 0.0
        data['sales growth QTD'] = 0.0
        data['margin growth QTD'] = 0.0
        data['pipelines'] = 0.0

    finally:
        try:
            con.close()
        except:
            print('No Db connection possible')
            pass

    return data


def getPerformance(username, account='all', dbusername='', passwd=''):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    dbname = 'data_{}'.format(username)
    dbname_results = dbname
    dbname_tasks = dbname.replace('tasks', 'data')

    # username = ''
    # passwd = ''

    data = dict()

    try:
        account = account.decode('utf-8')
    except:
        pass
    account = account.encode('latin-1')

    try:
        logging.debug(dbname)

        mysql_connection = connection.MySQLConnection(dbname_results)
        con = mysql_connection.connect()
        cur = con.cursor()

        logging.debug(con)

        if account == 'all':
            data['plans per account'] = kam.plansPerAccount(cur)
            data['actions per account'] = kam.actionsPerAccount(cur)

        data['activity goals'] = kam.activityGoals(cur, account=account)
        data['total sales plans'] = kam.totalSalesPlans(cur, account=account)
        data['total plan goals'] = kam.totalPlanGoals(cur, account=account)

        data['actions per day'] = kam.actionsPerDay(cur, account=account)
        data['actions per month'] = kam.actionsPerMonth(cur, account=account)
        data['actions per year'] = kam.actionsPerYear(cur, account=account)

        data['goals per quarter'] = kam.goalsPerQuarter(cur, account=account)
        data['total calls goal'] = kam.totalCallsGoal(cur, account=account)
        data['total visits goal'] = kam.totalVisitsGoal(cur, account=account)
        data['total offers goal'] = kam.totalOffersGoal(cur, account=account)

        month = str(datetime.datetime.now().month)
        try:
            data['actions this month'] = data['actions per month'][month]
        except:
            data['actions this month'] = 0

        data['actions QTD'] = kam.actionsQTD(cur, account=account)
        data['actions MTD'] = kam.actionsMTD(cur, account=account)
        data['actions YTD'] = kam.actionsYTD(cur, account=account)

        today = str(datetime.datetime.now()).split(" ")[0]
        firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))
        wd = np.busday_count(firstday, today) * 1.0
        data['actions YTD date ratio'] = round(data['actions YTD'] / wd, 2)

    except Exception as e:
        # print("Error {0}: {1}".format(e.args[0], e.args[1]))

        if account == 'all':
            data['plans per account'] = "{}"
            data['actions per account'] = "{}"

        data['activity goals'] = 0
        data['total sales plans'] = 0
        data['total plan goals'] = 0
        data['actions per day'] = 0
        data['actions per month'] = 0
        data['actions per year'] = 0
        data['goals per quarter'] = 0
        data['total calls goal'] = 0
        data['total visits goal'] = 0
        data['total offers goal'] = 0
        data['actions this month'] = 0
        data['actions QTD'] = 0
        data['actions MTD'] = 0
        data['actions YTD'] = 0
        data['actions YTD date ratio'] = 0

    finally:
        try:
            con.close()
        except:
            print('No Db connection possible')
            pass

    try:
        mysql_connection = connection.MySQLConnection(dbname_tasks)
        con = mysql_connection.connect()
        cur = con.cursor()

        today = datetime.datetime.now()

        # list of all accounts
        if account == 'all':
            data['accounts'] = kam.accounts(cur)
            # active accounts and sales in the las 3 months
            data['active accounts'] = kam.activeAccounts(cur)
            hoy = datetime.datetime.now()
            _tmb = datetime.datetime(year=hoy.year, month=hoy.month, day=hoy.day)
            try:
                data['active accounts growth'] = 100. * (
                            len(data['active accounts'].keys()) / len(kam.activeAccounts(cur, today=_tmb).keys()) - 1)
            except:
                data['active accounts growth'] = 0

            data['lost accounts'] = [a for a in data['accounts'] if a not in data['active accounts'].keys()]
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

        data['sales YTD'] = round(sales.salesYTD(cur, account=account), 2)
        data['margin YTD'] = round(sales.salesYTD(cur, param='margin', account=account), 2)
        data['sales QTD'] = round(sales.salesQTD(cur, year=today.year, account=account), 2)
        data['margin QTD'] = round(sales.salesQTD(cur, param='margin', year=today.year, account=account), 2)
        data['sales MTD'] = round(sales.salesMTD(cur, account=account), 2)
        data['sales per quarter'] = sales.salesPerQuarter(cur, param='price', year=today.year, account=account)
        data['margin per quarter'] = sales.salesPerQuarter(cur, param='margin', year=today.year, account=account)

        data['monthly sales'] = multiparam.monthlyParam(cur, param='price', year=today.year, account=account)
        data['monthly sales last year'] = multiparam.monthlyParam(cur, param='price', year=today.year - 1,
                                                                  account=account)

        data['monthly margin'] = multiparam.monthlyParam(cur, param='margin', year=today.year, account=account)
        data['monthly margin last year'] = multiparam.monthlyParam(cur, param='margin', year=today.year - 1,
                                                                   account=account)

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
            salesLastQuarter = round(sales.salesPerQuarter(cur, year=today.year - 1, param='price', account=account)[4],
                                     2)
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
            marginLastQuarter = round(
                sales.salesPerQuarter(cur, year=today.year - 1, param='margin', account=account)[4], 2)
        else:
            marginLastQuarter = round(data['margin per quarter'][currentQuarter - 1], 2)

        try:
            data['margin growth QTD'] = round(100 * marginCurrentQuarter / marginLastQuarter, 2)
        except:
            data['margin growth QTD'] = 0.0

        # PIPELINE

        # data['pipelines'] = sales._pipelines()
        data['pipelines'] = sales.pipelines(cur, username)

    except Exception as e:
        # print("Error {0}: {1}".format(e.args[0], e.args[1]))
        # data = {}
        data['sales YTD'] = 0
        data['margin YTD'] = 0
        data['sales QTD'] = 0
        data['margin QTD'] = 0
        data['sales MTD'] = 0
        data['sales per quarter'] = 0
        data['margin per quarter'] = 0
        data['monthly sales'] = 0
        data['monthly sales last year'] = 0
        data['monthly margin'] = 0
        data['monthly margin last year'] = 0
        data['sales last year'] = 0
        data['sales growth YTD'] = 0.0
        data['sales growth month'] = 0.0
        data['margin last year'] = 0.0
        data['margin growth YTD'] = 0.0
        data['margin growth month'] = 0.0
        data['sales growth QTD'] = 0.0
        data['margin growth QTD'] = 0.0
        data['pipelines'] = 0.0

    finally:
        try:
            con.close()
        except:
            print('No Db connection possible')
            pass

    return data


if __name__ == "__main__":
    import json

    local = True

    # Tasks database name
    dbname = ''
    username = 'martinmasip'
    dbname = 'data_{}_data_test_2015_2016_copy_4_xlsx'.format(username)
    dbname = '{}_data_test_2015_2016_copy_4_xlsx'.format(username)

    passwd = 'Qymatix!!!'
    dbusername = 'webadmin'
    dbusername = 'webuser'

    username = 'martin_masip'
    username = 'qymatix_best'
    dbname = username

    # data = getInsights(dbname=dbname, local=local, account='Acrion', username=dbusername, passwd=passwd)
    # print(json.dumps(data))

    account = u'Krankenhaus Hetzelstift Neustadt/Weinstrasse'
    account = 'St\xe4dtisches Klinikum Karlsruhe gGmbH'.decode('latin-1')
    account = 'St\xe4dtisches Klinikum Karlsruhe gGmbH'
    account = 'Klinikum Wolfsburg'
    account = 'all'
    print(account)
    # dbname = 'coldjet_qy'
    # username = 'robert_gruen'
    dbname = 'qy___test_com'

    username = 'ep__mtm___ne_de'
    dbname = 'mtm___ne_de'

    data = getInsights(dbname=dbname, local=False, account=account, username=dbusername, passwd=passwd)
    print(data['monthly sales'])
    # print(json.dumps(data))
    data = json.dumps(data, encoding='latin-1')

    # dbname = 'demo'
    # data = getPerformance(username=dbname, local=local, account='all', dbusername=dbusername, passwd=passwd)
    # print(data)
    # print(json.dumps(data))
