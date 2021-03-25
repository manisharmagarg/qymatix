'''
Read databases for insghits results
'''
# pylint: disable=invalid-name
# pylint: disable=bare-except
# pylint: disable=broad-except
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
# pylint: disable=unused-argument
# pylint: disable=singleton-comparison
# pylint: disable=redundant-keyword-arg
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=no-value-for-parameter
# pylint: disable=too-many-function-args
# pylint: disable=too-many-nested-blocks
# pylint: disable=unused-variable
# pylint: disable=import-error
# pylint: disable=too-many-lines
# pylint: disable=unreachable
import datetime
import logging
import traceback
import numpy as np
import MySQLdb as mysql
from ..qymatix import results
from ..qymatix.analytics.performance_analytics import goals, kam, multiparam
from ..qymatix.analytics.sales_analytics import sales
from ..infrastructure.mysql import  connection

logger = logging.getLogger(__name__)


def getInsights(dbname, account='all', raw=False,
                local=False, dbusername='', passwd='', username=''):
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

        # logging.debug(dbname)

        datadb = dbname_results
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if account == 'all':
            data['plans per account'] = kam.plansPerAccount(cur, username=username)
            data['actions per account'] = kam.actionsPerAccount(cur, username=username)

        data['activity goals'] = kam.activityGoals(cur, account=account, username=username)
        data['total sales plans'] = kam.totalSalesPlans(cur, account=account, username=username)
        data['total plan goals'] = kam.totalPlanGoals(cur, account=account, username=username)

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

    except (
            NameError, TypeError,
            KeyError, ValueError,
            AttributeError, IndexError
    ) as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )

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

        raise

    finally:
        try:
            con.close()
        except Exception as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )
    try:
        mysql_connection = connection.MySQLConnection(dbname_tasks)
        con = mysql_connection.connect()
        cur = con.cursor()

        today = datetime.datetime.now()

        # list of all accounts
        if account == 'all':
            data['accounts'] = kam.accounts(cur, username)
            # active accounts and sales in the las 3 months
            data['active accounts'] = kam.activeAccounts(cur, username=username)
            hoy = datetime.datetime.now()
            _tmb = datetime.datetime(year=hoy.year, month=hoy.month, day=hoy.day)
            try:
                data['active accounts growth'] = 100. * (len(
                    data['active accounts'].keys()
                ) / len(kam.activeAccounts(
                    cur, account, username, today=_tmb
                ).keys()) - 1)
            except:
                data['active accounts growth'] = 0

            data['lost accounts'] = [
                a for a in data['accounts'] if a not in data['active accounts'].keys()
            ]
            try:
                data['actions-accounts ratio'] = round(
                    float(data['actions YTD']) / len(data['accounts']), 2
                )
            except:
                data['actions-accounts ratio'] = 0.0
            try:
                data['actions-active accounts ratio'] = round(
                    float(data['actions YTD']) / len(
                        data['active accounts'].keys()
                    ), 2
                )
            except:
                data['actions-active accounts ratio'] = 0.0
            try:
                data['penetration ratio'] = round(
                    100 * float(len(
                        data['active accounts'].keys()
                    )) / len(data['accounts']), 2
                )
            except:
                data['penetration ratio'] = 0.0

        try:
            data['sales YTD'] = round(
                sales.salesYTD(
                    cur, account=account, username=username
                ), 2
            )
        except:
            data['sales YTD'] = 0.0
        try:
            data['margin YTD'] = round(
                sales.salesYTD(
                    cur, param='margin', account=account,
                    username=username), 2
            )
        except:
            data['margin YTD'] = 0.0
        try:
            data['sales QTD'] = round(
                sales.salesQTD(
                    cur, year=today.year, account=account,
                    username=username), 2
            )
        except:
            data['sales QTD'] = 0.0
        try:
            data['margin QTD'] = round(
                sales.salesQTD(
                    cur, param='margin', year=today.year,
                    account=account, username=username
                ), 2
            )
        except:
            data['margin QTD'] = 0.0
        try:
            data['sales MTD'] = round(
                sales.salesMTD(
                    cur, account=account, username=username
                ), 2
            )
        except:
            data['sales MTD'] = 0.0
        data['sales per quarter'] = sales.salesPerQuarter(
            cur, param='price', year=today.year,
            account=account, username=username
        )
        data['margin per quarter'] = sales.salesPerQuarter(
            cur, param='margin', year=today.year,
            account=account, username=username
        )

        data['monthly sales'] = multiparam.monthlyParam(
            cur, param='price', year=today.year,
            account=account, username=username
        )
        data['monthly sales last year'] = multiparam.monthlyParam(
            cur, param='price', year=today.year - 1,
            account=account, username=username
        )

        data['monthly margin'] = multiparam.monthlyParam(
            cur, param='margin', year=today.year,
            account=account, username=username
        )
        data['monthly margin last year'] = multiparam.monthlyParam(
            cur, param='margin', year=today.year - 1,
            account=account, username=username
        )

        s = 0
        for d in data['monthly sales last year']:
            s += d['sales']
        data['sales last year'] = round(s, 2)

        try:
            data['sales growth YTD'] = round(
                100 * data['sales YTD'] / data['sales last year'], 0
            )
        except:
            data['sales growth YTD'] = 0.0

        s = 0
        if today.month > 1:
            try:
                data['sales growth month'] = round(
                    data['monthly sales'][today.month] /
                    data['monthly sales'][today.month - 1], 2
                )
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
            data['margin growth YTD'] = round(
                100 * data['margin YTD'] / data['margin last year'], 0
            )
        except:
            data['margin growth YTD'] = 0.0

        s = 0
        if today.month > 1:
            try:
                data['margin growth month'] = round(
                    data['monthly margin'][today.month] /
                    data['monthly margin'][today.month - 1], 2
                )
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
            salesLastQuarter = round(
                sales.salesPerQuarter(
                    cur, year=today.year - 1, param='price',
                    account=account, username=username)[4], 2
            )
        else:
            salesLastQuarter = round(
                data['sales per quarter'][currentQuarter - 1], 2
            )

        try:
            data['sales growth QTD'] = round(
                100 * salesCurrentQuarter / salesLastQuarter, 2
            )
        except:
            data['sales growth QTD'] = 0.0

        # MARGIN
        currentQuarter = (today.month - 1) // 3 + 1
        marginCurrentQuarter = data['margin per quarter'][currentQuarter]
        if currentQuarter == 1:
            marginLastQuarter = round(
                sales.salesPerQuarter(cur, year=today.year - 1,
                                      param='margin', account=account,
                                      username=username)[4], 2
            )
        else:
            marginLastQuarter = round(
                data['margin per quarter'][currentQuarter - 1], 2
            )

        try:
            data['margin growth QTD'] = round(
                100 * marginCurrentQuarter / marginLastQuarter, 2
            )
        except:
            data['margin growth QTD'] = 0.0

        # PIPELINE

        data['pipelines'] = sales.pipelines()

    except mysql.Error as e:
        raise
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
        except Exception as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )

    return data


def get_insights_crm(dbname, account='all', raw=False, local=False,
                     dbusername='', passwd='', username='', user=''):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    dbname = 'data_{}'.format(dbname)
    dbname_results = dbname
    dbname_tasks = dbname.replace('tasks', 'data')

    data = dict()

    try:
        mysql_connection = connection.MySQLConnection(dbname_results)
        con = mysql_connection.connect()
        cur = con.cursor()

        if account == 'all':
            data['plans_per_account'] = kam.plansPerAccount(
                cur, username=username
            )
            data['actions_per_account'] = kam.actionsPerAccount(
                cur, username=username
            )

        data['activity_goals'] = kam.activityGoals(
            cur, account=account, username=username
        )
        data['total_sales_plans'] = kam.totalSalesPlans(
            cur, account=account, username=username
        )
        data['total_plan_goals'] = kam.totalPlanGoals(
            cur, account=account, username=username
        )

        data['actions_per_day'] = kam.actionsPerDay(
            cur, account=account, username=username
        )
        data['actions_per_month'] = kam.actionsPerMonth(
            cur, account=account, username=username
        )
        data['actions_per_year'] = kam.actionsPerYear(
            cur, account=account, username=username
        )

        data['goals_per_quarter'] = kam.goalsPerQuarter(
            cur, account=account, username=username
        )
        data['total_calls_goal'] = kam.totalCallsGoal(
            cur, account=account, username=username
        )
        data['total_visits_goal'] = kam.totalVisitsGoal(
            cur, account=account, username=username
        )
        data['total_offers_goal'] = kam.totalOffersGoal(
            cur, account=account, username=username
        )

        month = str(datetime.datetime.now().month)
        try:
            data['actions_this_month'] = data['actions_per_month'][month]
        except:
            data['actions_this_month'] = 0

        data['actions_QTD'] = kam.actionsQTD(
            cur, account=account, username=username
        )
        data['actions_MTD'] = kam.actionsMTD(
            cur, account=account, username=username
        )
        data['actions_YTD'] = kam.actionsYTD(
            cur, account=account, username=username
        )

        today = str(datetime.datetime.now()).split(" ")[0]
        firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))
        wd = np.busday_count(firstday, today) * 1.0
        data['actions_YTD_date_ratio'] = round(data['actions_YTD'] / wd, 2)

    except Exception as exception:

        if account == 'all':
            data['plans_per_account'] = "{}"
            data['actions_per_account'] = "{}"

        data['activity_goals'] = 0
        data['total_sales_plans'] = 0
        data['total_plan_goals'] = 0
        data['actions_per_day'] = 0
        data['actions_per_month'] = 0
        data['actions_perQyear'] = 0
        data['goals_per_quarter'] = 0
        data['total_calls_goal'] = 0
        data['total_visits_goal'] = 0
        data['total_offers_goal'] = 0
        data['actions_this_month'] = 0
        data['actions_QTD'] = 0
        data['actions_MTD'] = 0
        data['actions_YTD'] = 0
        data['actions_YTD_date_ratio'] = 0

        raise

    finally:
        try:
            con.close()
        except Exception as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )

    try:
        mysql_connection = connection.MySQLConnection(dbname_tasks)
        con = mysql_connection.connect()
        cur = con.cursor()

        today = datetime.datetime.now()

        # list of all accounts
        if account == 'all':
            data['accounts'] = kam.accounts(cur, username)
            data['accounts_name'] = kam.accounts_name(cur, username)
            # active accounts and sales in the las 3 months
            data['active_accounts'] = kam.activeAccountsCRM(cur, username=username)
            hoy = datetime.datetime.now()
            _tmb = datetime.datetime(year=hoy.year, month=hoy.month, day=hoy.day)
            try:
                data['active_accounts_growth'] = 100. * (len(data['active_accounts'].keys()) / len(
                    kam.activeAccounts(cur, account, username, today=_tmb).keys()) - 1)
            except:
                data['active_accounts_growth'] = 0

            data['lost_accounts'] = [
                a for a in data['accounts'] if a not in data['active_accounts'].keys()
            ]
            try:
                data['actions_accounts_ratio'] = round(
                    float(data['actions_YTD']) / len(data['accounts']), 2
                )
            except:
                data['actions_accounts_ratio'] = 0.0
            try:
                data['actions_active_accounts_ratio'] = round(
                    float(data['actions_YTD']) / len(
                        data['active_accounts'].keys()
                    ), 2
                )
            except:
                data['actions_active_accounts_ratio'] = 0.0
            try:
                data['penetration_ratio'] = round(
                    100 * float(len(data['active_accounts'].keys())) / len(
                        data['accounts']), 2
                )
            except:
                data['penetration_ratio'] = 0.0

        # PIPELINE

        # pp = round(sales.pipelines(cur), 2)
        # try:
        # pp = sales.pipelines(cur)
        # except:
        # pp = 0
        data['pipelines'] = data['actions_YTD_date_ratio']

        months = (
            'january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december'
        )

        data['goals'] = goals.get_goals(con, groupby='year', orient='list')
        cur = con.cursor()
        if today.year - 1 not in data['goals'].keys():
            goals.create_goal(cur, {'year': today.year - 1}, user=user)
        if today.year not in data['goals'].keys():
            goals.create_goal(cur, {'year': today.year}, user=user)
        if today.year + 1 not in data['goals'].keys():
            goals.create_goal(cur, {'year': today.year + 1}, user=user)
        if today.year + 2 not in data['goals'].keys():
            goals.create_goal(cur, {'year': today.year + 2}, user=user)

        data['goals'] = goals.get_goals(con, groupby='year', orient='list')

        data['total_goals'] = {}
        for k in data['goals'].keys():
            data['total_goals'][k] = {}
            for l in months:
                data['total_goals'][k][l] = np.sum(data['goals'][k][l])
            data['total_goals'][k]['id'] = data['goals'][k]['id'][0]

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
        raise

    finally:
        try:
            con.close()
        except Exception as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )

    return data


def get_insights(dbname, account='all', raw=False, local=False,
                 dbusername='', passwd='', username='', user=''):
    ''' Reads result's database, manipulate the data and returns it.
    '''
    dbname = 'data_{}'.format(dbname)
    dbname_results = dbname
    dbname_tasks = dbname.replace('tasks', 'data')

    # username = ''
    # passwd = ''

    data = dict()

    # try:
    #     account = account.decode('utf-8')
    # except:
    #     pass
    # account = account.encode('latin-1')

    try:
        mysql_connection = connection.MySQLConnection(dbname_results)
        con = mysql_connection.connect()
        cur = con.cursor()

        if account == 'all':
            data['plans_per_account'] = kam.plansPerAccount(
                cur, username=username
            )
            data['actions_per_account'] = kam.actionsPerAccount(
                cur, username=username
            )

        data['activity_goals'] = kam.activityGoals(
            cur, account=account, username=username
        )
        data['total_sales_plans'] = kam.totalSalesPlans(
            cur, account=account, username=username
        )
        data['total_plan_goals'] = kam.totalPlanGoals(
            cur, account=account, username=username
        )

        data['actions_per_day'] = kam.actionsPerDay(
            cur, account=account, username=username
        )
        data['actions_per_month'] = kam.actionsPerMonth(
            cur, account=account, username=username
        )
        data['actions_per_year'] = kam.actionsPerYear(
            cur, account=account, username=username
        )

        data['goals_per_quarter'] = kam.goalsPerQuarter(
            cur, account=account, username=username
        )
        data['total_calls_goal'] = kam.totalCallsGoal(
            cur, account=account, username=username
        )
        data['total_visits_goal'] = kam.totalVisitsGoal(
            cur, account=account, username=username
        )
        data['total_offers_goal'] = kam.totalOffersGoal(
            cur, account=account, username=username
        )

        month = str(datetime.datetime.now().month)
        try:
            # data['actions_this_month'] = data['actions_per_month'][month]
            data['actions_this_month'] = month
        except:
            data['actions_this_month'] = 0

        data['actions_QTD'] = kam.actionsQTD(
            cur, account=account, username=username
        )
        data['actions_MTD'] = kam.actionsMTD(
            cur, account=account, username=username
        )
        data['actions_YTD'] = kam.actionsYTD(
            cur, account=account, username=username
        )

        today = str(datetime.datetime.now()).split(" ")[0]
        firstday = str(datetime.date(datetime.datetime.now().year, 1, 1))
        wd = np.busday_count(firstday, today) * 1.0
        data['actions_YTD_date_ratio'] = round(data['actions_YTD'] / wd, 2)

    except Exception as e:
        # print("Error {0}: {1}".format(e.args[0], e.args[1]))

        if account == 'all':
            data['plans_per_account'] = "{}"
            data['actions_per_account'] = "{}"

        data['activity_goals'] = 0
        data['total_sales_plans'] = 0
        data['total_plan_goals'] = 0
        data['actions_per_day'] = 0
        data['actions_per_month'] = 0
        data['actions_perQyear'] = 0
        data['goals_per_quarter'] = 0
        data['total_calls_goal'] = 0
        data['total_visits_goal'] = 0
        data['total_offers_goal'] = 0
        data['actions_this_month'] = 0
        data['actions_QTD'] = 0
        data['actions_MTD'] = 0
        data['actions_YTD'] = 0
        data['actions_YTD_date_ratio'] = 0

        raise

    finally:
        try:
            con.close()
        except Exception as exception:
            logger.error(
                "message %s",
                exception,
                extra={
                    'type': 'Login'
                }
            )

    try:
        mysql_connection = connection.MySQLConnection(dbname_tasks)
        con = mysql_connection.connect()
        cur = con.cursor()

        today = datetime.datetime.now()


        # list of all accounts
        if account == 'all':
            data['accounts'] = kam.accounts(cur, username)
            data['accounts_name'] = kam.accounts_name(cur, username)
            # active accounts and sales in the las 3 months
            data['active_accounts'] = kam.activeAccounts(cur, username=username)
            hoy = datetime.datetime.now()
            _tmb = datetime.datetime(year=hoy.year, month=hoy.month, day=hoy.day)
            try:
                data['active_accounts_growth'] = 100. * (len(data['active_accounts'].keys()) / len(
                    kam.activeAccounts(cur, account, username, today=_tmb).keys()) - 1)
            except:
                data['active_accounts_growth'] = 0

            data['lost_accounts'] = [
                a for a in data['accounts'] if a not in data['active_accounts'].keys()
            ]
            try:
                data['actions_accounts_ratio'] = round(
                    float(data['actions_YTD']) / len(
                        data['accounts']), 2
                )
            except:
                data['actions_accounts_ratio'] = 0.0
            try:
                data['actions_active_accounts_ratio'] = round(
                    float(data['actions_YTD']) / len(
                        data['active_accounts'].keys()
                    ), 2
                )
            except:
                data['actions_active_accounts_ratio'] = 0.0
            try:
                data['penetration_ratio'] = round(
                    100 * float(len(
                        data['active_accounts'].keys()
                    )) / len(data['accounts']), 2
                )
            except:
                data['penetration_ratio'] = 0.0

        try:
            data['sales_YTD'] = sales.salesYTD(
                cur, account=account, username=username
            )
            if data['sales_YTD'] == None:
                data['sales_YTD'] = 0.0
        except:
            data['sales_YTD'] = 0.0

        # print(data['sales_YTD'])

        try:
            data['margin_YTD'] = sales.salesYTD(
                cur, param='margin', account=account, username=username
            )
            if data['margin_YTD'] == None:
                data['margin_YTD'] = 0.0
        except:
            data['margin_YTD'] = 0.0


        try:
            data['sales_QTD'] = round(
                sales.salesQTD(
                    cur, year=today.year, account=account, username=username
                ), 2
            )
        except:
            data['sales_QTD'] = 0.0
        try:
            data['margin_QTD'] = round(
                sales.salesQTD(
                    cur, param='margin', year=today.year, account=account,
                    username=username
                ), 2
            )
        except:
            data['margin_QTD'] = 0.0
        try:
            data['sales_MTD'] = round(
                sales.salesMTD(cur, account=account, username=username), 2
            )
        except:
            data['sales_MTD'] = 0.0

        # data['sales per quarter'] = sales.salesPerQuarter(
        #     cur, param='price', year=today.year,
        #     account=account, username=username
        # )
        # data['margin per quarter'] = sales.salesPerQuarter(
        # cur, param='margin', year=today.year,
        # account=account, username=username
        # )
        #
        # data['monthly sales'] = multiparam.monthlyParam(
        # cur, param='price', year=today.year,
        # account=account, username=username
        # )
        # data['monthly sales last year'] = multiparam.monthlyParam(
        # cur, param='price', year=today.year-1,
        # account=account, username=username
        # )
        #
        # data['monthly margin'] = multiparam.monthlyParam(
        # cur, param='margin', year=today.year,
        # account=account, username=username
        # )
        # data['monthly margin last year'] = multiparam.monthlyParam(
        # cur, param='margin', year=today.year-1,
        # account=account, username=username
        # )

        data['values_per_month'] = multiparam.values_per_month(
            cur, param='margin', year=today.year,
            account=account, username=username
        )
        data['values_per_quarter'] = sales.values_per_quarter(
            cur, param='price', year=today.year,
            account=account, username=username
        )

        s = 0
        for d in data['values_per_month'][today.year - 1]['sales']:
            s += d
        data['sales_last_year'] = round(s, 2)

        s = 0
        for d in data['values_per_month'][today.year]['sales']:
            s += d
        data['sales_current_year'] = round(s, 2)

        try:
            data['sales_growth_YTD'] = round(
                100 * data['sales_current_year'] /
                data['sales_last_year'], 0
            )
        except:
            data['sales_growth_YTD'] = 0.0
            # raise

        s = 0
        if today.month > 1:
            try:
                data['sales growth month'] = (
                    data['monthly sales'][today.month] /
                    data['monthly sales'][today.month - 1], 2
                )
            except:
                data['sales growth month'] = 0.0
        else:
            try:
                for l in data['monthly sales last year']:
                    if l['month'] == 12:
                        sb = l['sales']
                for l in data['monthly sales']:
                    if l['month'] == 12:
                        cs = l['sales']
                data['sales growth month'] = round(cs / sb, 2)
            except:
                data['sales growth month'] = 0.0

        data['sales per quarter'] = sales.salesPerQuarter(
            cur, param='price', year=today.year,
            account=account, username=username
        )

        data['sales per quarter last year'] = sales.salesPerQuarter(
            cur, param='price', year=today.year-1,
            account=account, username=username
        )

        data['margin per quarter'] = sales.salesPerQuarter(
            cur, param='margin', year=today.year,
            account=account, username=username
        )

        data['margin per quarter last year'] = sales.salesPerQuarter(
            cur, param='margin', year=today.year-1,
            account=account, username=username
        )

        data['monthly sales'] = multiparam.monthlyParam(
            cur, param='price', year=today.year,
            account=account, username=username
        )

        data['monthly sales last year'] = multiparam.monthlyParam(
            cur, param='price', year=today.year - 1,
            account=account, username=username
        )

        data['monthly margin'] = multiparam.monthlyParam(
            cur, param='margin', year=today.year,
            account=account, username=username
        )

        data['monthly margin last year'] = multiparam.monthlyParam(
            cur, param='margin', year=today.year - 1,
            account=account, username=username
        )

        s = 0
        for d in data['monthly margin last year']:
            s += d['margin']
        data['margin last year'] = round(s, 2)

        s = 0
        for d in data['values_per_month'][today.year - 1]['margin']:
            # s += d['sales']
            s += d
        data['margin_last_year'] = round(s, 2)

        # try:
        #     data['margin_growth_YTD'] = 100 * data['margin_YTD'] / data['margin_last_year']
        # except:
        #     data['margin_growth_YTD'] = 0.0
        # raise

        s = 0
        if today.month > 1:
            try:
                data['margin_growth_month'] = round(
                    data['monthly margin'][today.month] /
                    data['monthly margin'][today.month - 1], 2
                )
            except:
                data['margin_growth_month'] = 0.0
        else:
            for l in data['monthly margin last year']:
                if l['month'] == 12:
                    sb = l['margin']
            for l in data['monthly margin']:
                if l['month'] == 12:
                    cs = l['margin']
            try:
                data['margin_growth_month'] = round(cs / sb, 2)
            except:
                data['margin_growth_month'] = 0.0

        # SALES
        currentQuarter = (today.month - 1) // 3 + 1
        data['sales_current_quarter'] = data[
            'values_per_quarter'][today.year]['sales'][currentQuarter - 1]
        if currentQuarter == 1:
            data['sales_last_quarter'] = data[
                'values_per_quarter'
            ][today.year - 1]['sales'][3]
        else:
            data['sales_last_quarter'] = data[
                'values_per_quarter'
            ][today.year]['sales'][currentQuarter - 2]

        try:
            data['sales_growth_QTD'] = round(
                100 * data['sales_current_quarter'] / data['sales_last_quarter'], 2
            )
        except:
            data['sales_growth_QTD'] = 0.0

        # MARGIN
        data['margin_current_quarter'] = data[
            'values_per_quarter'][today.year]['margin'][currentQuarter - 1]
        if currentQuarter == 1:
            data['margin_last_quarter'] = data['values_per_quarter'][today.year - 1]['margin'][3]
        else:
            data['margin_last_quarter'] = data[
                'values_per_quarter'
            ][today.year]['margin'][currentQuarter - 2]

        try:
            data['margin_growth_QTD'] = round(
                100 * data['margin_current_quarter'] /
                data['margin_last_quarter'], 2
            )
        except:
            data['margin_growth_QTD'] = 0.0

        # PIPELINE

        # pp = round(sales.pipelines(cur), 2)
        try:
            pp = sales.pipelines(cur)
        except:
            pp = 0
        data['pipelines'] = pp
        data['kpi'] = {}
        data['kpi']['pipelines'] = pp

        if account == 'all':
            min_sales = sales.min_values(cur, username=username)
            max_sales = sales.max_values(cur, username=username)
            average_sales = sales.average_values(cur, username=username)

            min_results = results.min_values(cur, username=username)
            max_results = results.max_values(cur, username=username)

            average_results = results.average_values(cur, username=username)
            counts_ppb, counts_risk = results.count_ppb_risk(con, username=username)

            data['counts_ppb'] = counts_ppb
            data['counts_risk'] = counts_risk

            data['max_values'] = {}
            data['max_values'].update(max_sales)
            data['max_values'].update(max_results)

            data['min_values'] = {}
            data['min_values'].update(min_sales)
            data['min_values'].update(min_results)

            data['average_values'] = {}
            data['average_values'].update(average_sales)
            data['average_values'].update(average_results)

            data['normalized_average_values'] = {}
            # ********* Fix Me ***********
            # for k in data['max_values'].keys():
            #     data['normalized_average_values'][k] = data['average_values'][k] /
            #     data['max_values'][k]

        months = (
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december'
        )

        data['goals'] = goals.get_goals(con, groupby='year', orient='list')

        if today.year - 1 not in data['goals'].keys():
            try:
                goals.create_goal(con, {'year': today.year - 1}, user=user)
            except:
                pass
        if today.year not in data['goals'].keys():
            try:
                goals.create_goal(con, {'year': today.year}, user=user)
            except:
                pass
        if today.year + 1 not in data['goals'].keys():
            try:
                goals.create_goal(con, {'year': today.year + 1}, user=user)
            except:
                pass
        if today.year + 2 not in data['goals'].keys():
            try:
                goals.create_goal(con, {'year': today.year + 2}, user=user)
            except:
                pass

        data['goals'] = goals.get_goals(con, groupby='year', orient='list')

        data['total_goals'] = {}
        for k in data['goals'].keys():
            data['total_goals'][k] = {}
            for l in months:
                data['total_goals'][k][l] = np.sum(data['goals'][k][l])
            data['total_goals'][k]['id'] = data['goals'][k]['id'][0]

    except Exception as exception:
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
        raise
        data["message"] = exception
        data['traceback'] = traceback.format_exc()

    finally:
        try:
            con.close()
        except Exception as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )

    return data


def getPerformance(username, account='all', raw=False, local=False, dbusername='', passwd=''):
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
        mysql_connection = connection.MySQLConnection(dbname_results)
        con = mysql_connection.connect()
        cur = con.cursor()

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

    except:

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
        except Exception as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )

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
                data['active accounts growth'] = 100. * (len(
                    data['active accounts'].keys()
                ) / len(
                    kam.activeAccounts(cur, today=_tmb).keys()
                ) - 1)
            except:
                data['active accounts growth'] = 0

            data['lost accounts'] = [
                a for a in data['accounts'] if a not in data['active accounts'].keys()
            ]
            try:
                data['actions-accounts ratio'] = round(
                    float(data['actions YTD']) / len(
                        data['accounts']
                    ), 2
                )
            except:
                data['actions-accounts ratio'] = 0.0
            try:
                data['actions-active accounts ratio'] = round(
                    float(data['actions YTD']) / len(
                        data['active accounts'].keys()
                    ), 2
                )
            except:
                data['actions-active accounts ratio'] = 0.0
            try:
                data['penetration ratio'] = round(
                    100 * float(
                        len(
                            data['active accounts'].keys())
                    ) / len(data['accounts']), 2
                )
            except:
                data['penetration ratio'] = 0.0

        data['sales YTD'] = round(sales.salesYTD(cur, account=account), 2)
        data['margin YTD'] = round(
            sales.salesYTD(
                cur, param='margin', account=account
            ), 2
        )
        data['sales QTD'] = round(
            sales.salesQTD(
                cur, year=today.year, account=account
            ), 2
        )
        data['margin QTD'] = round(
            sales.salesQTD(
                cur, param='margin', year=today.year, account=account
            ), 2
        )
        data['sales MTD'] = round(sales.salesMTD(cur, account=account), 2)
        data['sales per quarter'] = sales.salesPerQuarter(
            cur, param='price', year=today.year, account=account
        )
        data['margin per quarter'] = sales.salesPerQuarter(
            cur, param='margin', year=today.year, account=account
        )

        data['monthly sales'] = multiparam.monthlyParam(
            cur, param='price', year=today.year, account=account
        )
        data['monthly sales last year'] = multiparam.monthlyParam(
            cur, param='price', year=today.year - 1, account=account
        )

        data['monthly margin'] = multiparam.monthlyParam(
            cur, param='margin', year=today.year, account=account
        )
        data['monthly margin last year'] = multiparam.monthlyParam(
            cur, param='margin', year=today.year - 1, account=account
        )

        s = 0
        for d in data['monthly sales last year']:
            s += d['sales']
        data['sales last year'] = round(s, 2)

        try:
            data['sales growth YTD'] = round(
                100 * data['sales YTD'] / data['sales last year'], 0
            )
        except:
            data['sales growth YTD'] = 0.0

        s = 0
        if today.month > 1:
            try:
                data['sales growth month'] = round(
                    data['monthly sales'][today.month] /
                    data['monthly sales'][today.month - 1], 2
                )
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
            data['margin growth YTD'] = round(
                100 * data['margin YTD'] / data['margin last year'], 0
            )
        except:
            data['margin growth YTD'] = 0.0

        s = 0
        if today.month > 1:
            try:
                data['margin growth month'] = round(
                    data['monthly margin'][today.month] /
                    data['monthly margin'][today.month - 1], 2
                )
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
            salesLastQuarter = round(
                sales.salesPerQuarter(
                    cur, year=today.year - 1, param='price', account=account
                )[4], 2
            )
        else:
            salesLastQuarter = round(
                data['sales per quarter'][currentQuarter - 1], 2
            )

        try:
            data['sales growth QTD'] = round(
                100 * salesCurrentQuarter / salesLastQuarter, 2
            )
        except:
            data['sales growth QTD'] = 0.0

        # MARGIN
        currentQuarter = (today.month - 1) // 3 + 1
        marginCurrentQuarter = data['margin per quarter'][currentQuarter]
        if currentQuarter == 1:
            marginLastQuarter = round(
                sales.salesPerQuarter(
                    cur, year=today.year - 1, param='margin',
                    account=account)[4], 2
            )
        else:
            marginLastQuarter = round(
                data['margin per quarter'][currentQuarter - 1], 2
            )

        try:
            data['margin growth QTD'] = round(
                100 * marginCurrentQuarter / marginLastQuarter, 2
            )
        except:
            data['margin growth QTD'] = 0.0

        # PIPELINE

        # data['pipelines'] = sales._pipelines()
        data['pipelines'] = sales.pipelines(cur, username)

    except:
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
        except Exception as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )

    return data


if __name__ == "__main__":
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

    # data = getInsights(dbname=dbname, local=local, account='Acrion',
    # username=dbusername, passwd=passwd
    # )

    account = u'Krankenhaus Hetzelstift Neustadt/Weinstrasse'
    account = 'St\xe4dtisches Klinikum Karlsruhe gGmbH'.decode('latin-1')
    account = 'St\xe4dtisches Klinikum Karlsruhe gGmbH'
    account = 'Klinikum Wolfsburg'
    account = 'all'

    # dbname = 'coldjet_qy'
    # username = 'robert_gruen'
    dbname = 'qy___test_com'

    username = 'ep__mtm___ne_de'
    # dbname = 'mtm___ne_de'
    dbname = 'qymatix_best'
    # username = 'chancho_babe__qymatix_best'
    username = 'qymatix__aet_at'
    account = 'all'
    account = 852
    # account = 1
    username = 'martin_masip__qymatix_de'
    dbname = 'qymatix_de'
    username = 'admin'
    dbname = 'aet_at'

    # data = getInsights(dbname=dbname, local=False, account=account,
    # username=dbusername, passwd=passwd
    # )
    # data = getInsights(dbname=dbname, local=False, account=account,
    # dbusername='webuser', username=username, passwd=passwd
    # )

    data = get_insights(
        dbname=dbname, local=False, account=account,
        dbusername='webuser', username=username,
        passwd=passwd
    )
    # data = get_insights_crm(dbname=dbname, local=False, account=account,
    # dbusername='webuser', username=username, passwd=passwd
    # )
    # print(data['monthly sales'])
    # print(json.dumps(data))
    # data = json.dumps(data, encoding='latin-1')
    # print(data['sales per quarter'])
    # print(data['monthly sales'])
    # print(data['values_per_month'])
    # print(data['values_per_quarter'])
    # print(data['sales YTD'])
    # print(data['pipelines'])

    # data = json.dumps(data, encoding='latin-1')
    # print(data)

    # dbname = 'demo'
    # data = getPerformance(username=dbname, local=local, account='all',
    # dbusername=dbusername, passwd=passwd
    # )
    # print(data)
    # print(json.dumps(data))
