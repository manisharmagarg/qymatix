import datetime
import logging

import numpy as np
import pandas as pd

from api.qymatix.analytics.performance_analytics import kam
from api.qymatix import products
from api import industryapi
from api.infrastructure.mysql import connection
import traceback

logger = logging.getLogger(__name__)

def getPerformanceCRM(dbname, account='all', raw=False, local=False, dbusername='', passwd='', username=''):
    ''' Reads result's database, manipulate the data and returns it.
    '''
    data = dict()

    if local:
        dbusername = 'webadmin'
    else:
        dbusername = 'webuser'
    passwd = 'Qymatix!!!'

    dbname = 'data_{}'.format(dbname)
    dbname_results = dbname
    dbname_tasks = dbname.replace('tasks', 'data')

    # This is for the CRM version
    # dbname_tasks = dbname

    # username = ''
    # passwd = ''

    try:

        logger.debug(dbname)

        mysql_connection = connection.MySQLConnection(dbname_results)
        con = mysql_connection.connect()
        cur = con.cursor()

        # account = account.decode('utf-8')
        # account = account.encode('latin-1')

        if account == 'all':
            data['plans per account'] = kam.plansPerAccount(cur, username=username)
            data['actions per account'] = kam.actionsPerAccount(cur, username=username)

        data['activity goals'] = kam.activityGoals(cur, account=account, username=username)
        data['total sales plans'] = kam.totalSalesPlans(cur, account=account, username=username)
        data['total plan goals'] = kam.totalPlanGoals(cur, account=account, username=username)
        try:
            data['average deal size'] = round(data['total plan goals'] / data['total sales plans'], 2)
        except:
            data['average deal size'] = 0

        data['average deal time'] = kam.averageDealTime(cur, account=account, username=username)
        data['closed plans'] = kam.closedPlans(cur, status='Closed Won', username=username)
        data['closed plans lost'] = kam.closedPlans(cur, status='Closed Lost', username=username)

        try:
            data['closed ratio'] = round(float(data['closed plans']) / data['total sales plans'], 2)
        except:
            data['closed ratio'] = 0

        data['actions per day'] = kam.actionsPerDay(cur, account=account, username=username)
        data['actions per month'] = kam.actionsPerMonth(cur, account=account, username=username)
        data['actions per year'] = kam.actionsPerYear(cur, account=account, username=username)

        data['goals per quarter'] = kam.goalsPerQuarter(cur, account=account, username=username)
        data['total calls goal'] = kam.totalCallsGoal(cur, account=account, username=username)
        data['total visits goal'] = kam.totalVisitsGoal(cur, account=account, username=username)
        data['total offers goal'] = kam.totalOffersGoal(cur, account=account, username=username)

        month = str(datetime.datetime.now().month)
        try:
            data['actions this month'] = data['actions per month'][month]
        except:
            data['actions this month'] = 0

        data['actions QTD'] = kam.actionsQTD(cur, account=account, username=username)
        data['actions MTD'] = kam.actionsMTD(cur, account=account, username=username)
        data['actions YTD'] = kam.actionsYTD(cur, account=account, username=username)

        today = str(datetime.datetime.now()).split(" ")[0]
        firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))
        wd = np.busday_count(firstday, today) * 1.0
        data['actions YTD date ratio'] = round(data['actions YTD'] / wd, 2)

        data['active accounts'] = kam.activeAccountsCRM(cur, username=username)
        hoy = datetime.datetime.now()
        _tmb = kam.monthdelta(hoy, -3)
        # print(hoy)
        # print(_tmb)
        data['active accounts TMB'] = kam.activeAccountsCRM(cur, when=_tmb, username=username)
        # print(data['active accounts TMB'])

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
            data['accounts'] = kam.accounts(cur, username=username)
            # active accounts and sales in the las 3 months

            try:
                # data['active accounts growth'] = 100. * (len(data['active accounts'].keys()) / len(kam.activeAccounts(cur, today=_tmb).keys()) - 1)
                data['active accounts growth'] = 100. * (
                            len(data['active accounts'].keys()) / len(data['active accounts TMB'].keys()) - 1)
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

        '''
        data['sales YTD'] = round(sales.salesYTD(cur, account=account), 2)
        data['margin YTD'] = round(sales.salesYTD(cur, param='margin', account=account), 2)
        data['sales QTD'] = round(sales.salesQTD(cur, year=today.year, account=account), 2)
        data['margin QTD'] = round(sales.salesQTD(cur, param='margin', year=today.year, account=account), 2)
        data['sales MTD'] = round(sales.salesMTD(cur, account=account), 2)
        data['sales per quarter'] = sales.salesPerQuarter(cur, param='price', year=today.year, account=account)
        data['margin per quarter'] = sales.salesPerQuarter(cur, param='margin', year=today.year, account=account)
        
        data['monthly sales'] = multiparam.monthlyParam(cur, param='price', year=today.year, account=account)
        data['monthly sales last year'] = multiparam.monthlyParam(cur, param='price', year=today.year-1, account=account)

        data['monthly margin'] = multiparam.monthlyParam(cur, param='margin', year=today.year, account=account)
        data['monthly margin last year'] = multiparam.monthlyParam(cur, param='margin', year=today.year-1, account=account)

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
                data['sales growth month'] = round(data['monthly sales'][today.month] / data['monthly sales'][today.month-1], 2)
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
                data['margin growth month'] = round(data['monthly margin'][today.month] / data['monthly margin'][today.month-1], 2)
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
        '''

        '''
        # SALES
        currentQuarter = (today.month - 1) // 3 + 1
        salesCurrentQuarter = data['sales per quarter'][currentQuarter]
        if currentQuarter == 1:
            salesLastQuarter = round(sales.salesPerQuarter(cur, year=today.year-1, param='price', account=account)[4], 2)
        else:
            salesLastQuarter = round(data['sales per quarter'][currentQuarter-1], 2)

        try:
            data['sales growth QTD'] = round(100 * salesCurrentQuarter / salesLastQuarter, 2)
        except:
            data['sales growth QTD'] = 0.0

        # MARGIN
        currentQuarter = (today.month - 1) // 3 + 1
        marginCurrentQuarter = data['margin per quarter'][currentQuarter]
        if currentQuarter == 1:
            marginLastQuarter = round(sales.salesPerQuarter(cur, year=today.year-1, param='margin', account=account)[4], 2)
        else:
            marginLastQuarter = round(data['margin per quarter'][currentQuarter-1], 2)

        try:
            data['margin growth QTD'] = round(100 * marginCurrentQuarter / marginLastQuarter, 2)
        except:
            data['margin growth QTD'] = 0.0
        '''

        # PIPELINE
        # data['pipelines'] = sales._pipelines()
        # data['pipelines'] = sales.pipelines(cur, username)
        # print(data['pipeline'])

    except Exception as e:
        # print("Error {0}: {1}".format(e.args[0], e.args[1]))
        # data = {}
        '''
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
        '''

    finally:
        try:
            con.close()
        except:
            print('No Db connection possible')
            pass

    return data


def get_performance_crm(dbname, account='all', raw=False, local=False, dbusername='', passwd='', username=''):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    if local:
        dbusername = 'webadmin'
    else:
        dbusername = 'webuser'
    passwd = 'Qymatix!!!'

    dbname = 'data_{}'.format(dbname)
    dbname_results = dbname
    dbname_tasks = dbname.replace('tasks', 'data')

    data = dict()

    try:

        logger.debug(dbname)

        mysql_connection = connection.MySQLConnection(dbname_results)
        con = mysql_connection.connect()
        cur = con.cursor()

        account = account.decode('utf-8')
        account = account.encode('latin-1')

        if account == 'all':
            data['plans per account'] = kam.plansPerAccount(cur, username=username)
            data['actions per account'] = kam.actionsPerAccount(cur, username=username)

        data['activity goals'] = kam.activityGoals(cur, account=account, username=username)
        data['total sales plans'] = kam.totalSalesPlans(cur, account=account, username=username)
        data['total plan goals'] = kam.totalPlanGoals(cur, account=account, username=username)
        try:
            data['average deal size'] = round(data['total plan goals'] / data['total sales plans'], 2)
        except:
            data['average deal size'] = 0

        data['average deal time'] = kam.averageDealTime(cur, account=account, username=username)
        data['closed plans'] = kam.closedPlans(cur, status='Closed Won', username=username)
        data['closed plans lost'] = kam.closedPlans(cur, status='Closed Lost', username=username)

        try:
            data['closed ratio'] = round(float(data['closed plans']) / data['total sales plans'], 2)
        except:
            data['closed ratio'] = 0

        data['actions per day'] = kam.actionsPerDay(cur, account=account, username=username)
        data['actions per month'] = kam.actionsPerMonth(cur, account=account, username=username)
        data['actions per year'] = kam.actionsPerYear(cur, account=account, username=username)

        data['goals per quarter'] = kam.goalsPerQuarter(cur, account=account, username=username)
        data['total calls goal'] = kam.totalCallsGoal(cur, account=account, username=username)
        data['total visits goal'] = kam.totalVisitsGoal(cur, account=account, username=username)
        data['total offers goal'] = kam.totalOffersGoal(cur, account=account, username=username)

        month = str(datetime.datetime.now().month)
        try:
            data['actions this month'] = data['actions per month'][month]
        except:
            data['actions this month'] = 0

        data['actions QTD'] = kam.actionsQTD(cur, account=account, username=username)
        data['actions MTD'] = kam.actionsMTD(cur, account=account, username=username)
        data['actions YTD'] = kam.actionsYTD(cur, account=account, username=username)

        today = str(datetime.datetime.now()).split(" ")[0]
        firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))
        wd = np.busday_count(firstday, today) * 1.0
        data['actions YTD date ratio'] = round(data['actions YTD'] / wd, 2)

        data['active accounts'] = kam.activeAccountsCRM(cur, username=username)
        hoy = datetime.datetime.now()
        _tmb = kam.monthdelta(hoy, -3)
        # print(hoy)
        # print(_tmb)
        data['active accounts TMB'] = kam.activeAccountsCRM(cur, when=_tmb, username=username)
        # print(data['active accounts TMB'])

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
            data['accounts'] = kam.accounts(cur, username=username)
            # active accounts and sales in the las 3 months

            try:
                # data['active accounts growth'] = 100. * (len(data['active accounts'].keys()) / len(kam.activeAccounts(cur, today=_tmb).keys()) - 1)
                data['active accounts growth'] = 100. * (
                            len(data['active accounts'].keys()) / len(data['active accounts TMB'].keys()) - 1)
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

        # PIPELINE
        # data['pipelines'] = sales._pipelines()
        # data['pipelines'] = sales.pipelines(cur, username)
        # print(data['pipeline'])

    except Exception as e:
        print("Error {0}: {1}".format(e.args[0], e.args[1]))
        data = {}

    finally:
        try:
            con.close()
        except:
            print('No Db connection possible')
            pass

    return data


def get_sales_year(dbname, local=False):
    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "SELECT DISTINCT year FROM `sales`ORDER BY year ASC"
        cur.execute(script)
        data = np.asarray(cur.fetchall())
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)
        return df['year'].values.tolist()
    except Exception as e:
        return "null"

def get_performance_products(dbname):
    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "SELECT id, name as product_type_name "\
            "FROM {db_}.product_type".format(
                db_=datadb
            )
        cur.execute(script)
        data = np.asarray(cur.fetchall())
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)
        return df.to_dict(orient='records')
    except Exception as e:
        return "null"


def performance_search_db(request, data, dbname, local=False):
    """
        {'year': '2019', 'month': '4', 'product_type': 'asdf', 'product': '5'}
    """

    resp = dict()
    customer_id = data.get("customer_id")

    if 'year' not in data.keys():
        resp['year'] = 'Year missing.'
        return resp
    if 'month' not in data.keys():
        resp['month'] = 'month missing'
        data['postcode'] = ''
        return resp
    if 'product_type' not in data.keys():
        resp['product_type'] = 'product type is missing'
    if 'product' not in data.keys():
        resp['product'] = 'product is missing'
        return resp
    if 'industry' not in data.keys():
        resp['industry'] = 'industry is missing'
        return resp

    datadb = 'data_' + dbname

    query = "SELECT sum(s.margin), sum(s.price), customers.name "\
            "From {db_}.sales as s LEFT JOIN {db_}.products  ON "\
            "s.product_id = products.id LEFT JOIN {db_}.product_type ON "\
            "products.product_type_id = product_type.id LEFT JOIN "\
            "{db_}.customers ON s.customer_id = customers.id WHERE 1=1 ".format(db_=datadb)

    if data.get("customer_id"):
        query +="AND customers.id = {customer_id} ".format(
                customer_id=data.get("customer_id")
            )

    if(data.get('industry') != "selected_all_industry") and not data.get("customer_id"):
        query +="AND customers.industry IN {industry} ".format(
            industry=convert_list_tuple(str(data.get('industry')))
            ) 

    if(data.get('year') != "selected_all_year"):
        query +="AND s.year IN {year} ".format(
            year=convert_list_tuple(str(data.get('year')))
            )

    if(data.get('month') != "selected_all_month"):
        query +="AND s.month IN {month} ".format(
            month=convert_list_tuple(str(data.get('month')))
            )

    if (data.get('kam') != "selected_all_kam"):
        query +="AND s.kam IN {kam} ".format(
            kam=convert_list_tuple(str(data.get('kam')))
            )

    if (data.get('product_type') != "selected_all_productType"):
        query +="AND product_type.id IN {product_type} ".format(
            product_type=convert_list_tuple(str(data.get('product_type')))
            )

    if (data.get('product') != "selected_all_product"):
        query +="AND s.product_id IN {product} ".format(
            product=convert_list_tuple(str(data.get('product')))
            )

    query+= "GROUP BY customers.id;"

    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()
        cur.execute(query)
        data = np.asarray(cur.fetchall())
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)
        df.columns = ['margin', "price", "name"]
        return df.to_dict(orient='records')
    except Exception as e:
        return "null"


def convert_list_tuple(list_data):
    print(type(list_data))
    return list_data.replace('[', '(').replace(']', ')')


if __name__ == "__main__":

    local = True
    local = False

    if local:
        dbusername = 'webadmin'
    else:
        dbusername = 'webuser'
    passwd = 'Qymatix!!!'

    username = 'martinmasip'
    # username = 'crmtest1'
    username = 'lucaspedretti'
    username = 'crmtest2'
    username = 'qymatix_de'
    username = 'qymatix_best'
    username = 'martin_masip__qymatix_de'

    username = 'admin'
    dbname = 'qymatix_de'
    dbname = 'qymatix_best'
    # username = 'qymatix_com'

    data = getPerformanceCRM(dbname, local=local, account='all', dbusername=dbusername, passwd=passwd,
                             username=username)
    # print(data['actions MTD'])
    # print(data['total sales plans'])
    print(data)
    # print(len(data['active accounts']))
    # print(data['actions per account'])
    # print(json.dumps(data, indent=4, sort_keys=True))
