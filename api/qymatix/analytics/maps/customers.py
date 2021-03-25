import datetime
import json

import MySQLdb as mysql

host = '80.147.39.6'
user = 'ahmed'
passwd = 'demha'


def get_customers():
    try:
        con = mysql.connect(host=host, user=user, passwd=passwd)
        cursor = con.cursor()
        sql = " select cu.*,ci.latitude,ci.longitude from ahmed_data.customers cu inner join ahmed_locations.cities ci on cu.city=ci.city;"
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        result = []
        for row in cursor.fetchall():
            row = dict(zip(columns, row))
            result.append(row)

        return json.dumps(result)

    except Exception as e:
        print(e)
        return -1

    con.close()


def get_allocation(year=None):
    try:
        if year == None:
            year = (datetime.datetime.now().year) - 1
        year = str(year)

        con = mysql.connect(host=host, user=user, passwd=passwd)
        cursor = con.cursor()
        sql = "\
           select  count(c.country) as count,c.country,sum(cr.sales) as sales,sum(cr.margin) as margin,avg(cr.ccbm) as avg_ccbm,sum(cr.ccbm*cr.sales) as weighted \
           from ahmed_data.customers c \
           INNER  join ahmed_results.critters cr \
           on c.name=cr.name \
           group by c.country;\
           "
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        result = []
        for row in cursor.fetchall():
            row = dict(zip(columns, row))
            result.append(row)

        return json.dumps(result)

    except Exception as e:
        print(e)
        return -1

    con.close()


if __name__ == "__main__":
    get_allocation()
