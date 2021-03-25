import datetime
import json

from api.infrastructure.mysql import connection


def top_products(dbname, year=None, account="all"):
    try:
        if year == None:
            year = (datetime.datetime.now().year) - 1
            year = (datetime.datetime.now().year)
        year = str(year)

        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cursor = con.cursor()

        '''
        try:
            account = account.decode('utf-8')
        except:
            pass
        account = account.encode('latin-1')
        '''

        if account == "all":
            sql = "\
            SELECT SUM(s.price) AS sales, SUM(s.margin) AS margin, p.name, p.id FROM {0}.sales s \
            INNER JOIN {0}.products p \
            ON s.product_id=p.id \
            WHERE YEAR(s.date)='{1}'\
            GROUP BY p.id ; \
            ".format(dbname, year, account)
        else:
            sql = "\
            SELECT SUM(s.price) AS sales,sum(s.margin) AS margin, p.name, p.id FROM {0}.sales s \
            INNER JOIN {0}.products p \
            ON s.product_id=p.id \
            INNER JOIN {0}.customers c \
            ON s.customer_id=c.id \
            WHERE YEAR(s.date)='{1}' And c.id='{2}' \
            GROUP BY p.id ; \
            ".format(dbname, year, account)

        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        result = []
        for row in cursor.fetchall():
            row = dict(zip(columns, row))
            result.append(row)

        return json.dumps(result)

    except Exception as e:
        print(e)
        raise
        # return -1

    con.close()
