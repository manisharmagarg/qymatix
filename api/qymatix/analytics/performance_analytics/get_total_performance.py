import datetime
import logging
import os

from django.conf import settings

# import goals
from api.qymatix.analytics.performance_analytics import goals
from api.infrastructure.mysql import connection


logger = logging.getLogger(__name__)

# TODO: delete the arbitrary date. It's just temporary necessary, as data for current quarter is unavailable in the database
date = datetime.date.today()


# date = datetime.date(2016,01,05)


def get_total_performance(dbname, local=False):
    '''
    '''

    result = {}
    # result["goals_per_quarter"] = goals.getGoalsPerQuarter(dbname= "data_" + dbname)[date.year]
    result["goals_per_quarter"] = goals.getGoalsPerQuarter(dbname)
    # print(result["goals_per_quarter"])

    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        sql = """ select  
                        cast(sum(sales.price) AS DECIMAL(0)) as sales, 
                        year(sales.date) as year,
                        month(sales.date) as month
                    from 
                        sales
                    group by year(sales.date), month(sales.date);"""

        cur.execute(sql)
        dicts = get_named_json(cur)
        result["monthly_sales"] = get_monthly_aggregated_data(dicts, date.year)
        result["sales_per_quarter"] = get_quaterly_aggregated_data(dicts, date.year)
        result["sales_MTD"] = get_MTD_data(result["monthly_sales"], 0)
        result["sales_QTD"] = get_QTD_data(result["sales_per_quarter"], 0)
        result["sales_YTD"] = get_YTD_data(result["sales_per_quarter"])
        prevMTD = get_MTD_data(dicts, 1)
        result["sales_growth_MTD"] = calc_diff_in_percent(result["sales_MTD"], prevMTD)
        aggr_QTD_prev_year = get_quaterly_aggregated_data(dicts, date.year - 1)
        prevQTD = get_QTD_data(result["sales_per_quarter"], 1, aggr_QTD_prev_year)
        result["sales_growth_QTD"] = calc_diff_in_percent(result["sales_QTD"], prevQTD)
        prevYTD = get_YTD_data(aggr_QTD_prev_year)
        result["sales_growth_YTD"] = calc_diff_in_percent(result["sales_YTD"], prevYTD)

        return result

    except Exception as e:
        return -1
        # raise

    con.close()


def get_named_json(cursor):
    '''
    Creates json from tuples
    '''
    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
    return result


def get_monthly_aggregated_data(dicts, *args):
    # aggregates data monthly - for a certain year extra argument (*args)
    resultList = []
    for i in dicts:
        newDict = {}
        sales = round(i["sales"], 2)
        month = int(i["month"])
        year = int(i["year"])
        newDict = {"sales": sales, "month": month, "year": year}
        resultList.append(newDict)
    # deletes certain items based on the value of a parameter (here: value: e.g. 2016, parameter: "year")
    filter_list(resultList, "year", args[0])
    return resultList


def filter_list(myList, parameter, value):
    # deletes certain items from a list of dictionaries based on the value of a parameter (e.g.: value: 2016, parameter: "year")
    for i in reversed(myList):
        if i[parameter] != value:
            myList.remove(i)
    return myList


def get_quaterly_aggregated_data(dicts, y):
    # filters for actual year and aggregates data quaterly
    resultList = []
    salesList = [0, 0, 0, 0]
    for i in dicts:
        if i["year"] == y:
            sales = round(i["sales"], 2)
            month = int(i["month"])
            if month < 4:
                salesList[0] += sales
            elif month < 7:
                salesList[1] += sales
            elif month < 10:
                salesList[2] += sales
            else:
                salesList[3] += sales
    resultList = [{x: salesList[x - 1]} for x in range(1, 5)]
    return resultList


def get_MTD_data(dicts, helper):
    ##returns actual data - one single data - if helper = 1 then previous month
    m = date.month - helper
    y = date.year
    if m <= 0:
        m = m + 12
        y = y - 1

    for i in dicts:
        if i["year"] == y and i["month"] == m:
            return i["sales"]
    return 0


def get_QTD_data(dicts, helper, *prev_dicts):
    q = (date.month - 1) / 3 + 1 - helper
    y = date.year

    ##adjustment: in case we go back to the previous year
    if q <= 0:
        q += 4
        dicts = prev_dicts[0]

    for i in dicts:
        for key in i:
            if key == q:
                return i[key]
            else:
                continue
    return 0


def get_YTD_data(dicts):
    sumData = 0
    for i in dicts:
        for key in i:
            sumData += i[key]
    return sumData


def calc_diff_in_percent(curr, prev):
    curr = float(curr)
    prev = float(prev)
    if prev == 0:
        prev += 0.0000000000001
    result = (curr - prev) / prev
    return result


def test_total_performance():
    '''
    '''
    dbname = "martinmasip_data_test_2015_2016_copy_super_reduced_xlsx"
    dbname = "demo"
    dbname = "martinmasip"
    dbname = 'qymatix_de'
    dbname = 'qymatix_best'
    local = False
    # local = True
    results = get_total_performance(dbname=dbname, local=local)
    return results


if __name__ == "__main__":
    results = test_total_performance()
    print(results)
