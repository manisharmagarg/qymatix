import sys

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import OnehotTransactions

from api.infrastructure.mysql import connection


def car(username='username', groupby='customer_id', raw=False, account='all', local=False):
    '''
    '''
    sys.stdout.write("Calculating car...\r")
    dbname = 'data_{}'.format(username)

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script_nop = "\
            SELECT c1.customer_id, c1.name, IF(avgPriceYear IS NULL, 0, avgPriceYear) as avgPriceYTD, IF(avgPriceHalfYear IS NULL, 0, avgPriceHalfYear) as avgPriceHYTD, avgPrice2Year,\
            IF(avgPriceHalfYear=0, -1, IF(avgPriceHalfYear IS NULL, -1, IF(avgPriceYear=NULL, 1, ATAN2(avgPriceHalfYear-avgPriceYear, 185)/(PI()/2)))) as risk\
            FROM\
            (SELECT id as customer_id, name FROM customers) c1\
            LEFT JOIN\
            (SELECT customer_id, AVG(sales.price) as avgPrice2Year FROM sales\
            WHERE DATE_SUB(CURDATE(),INTERVAL 2 YEAR) <= date\
            GROUP BY customer_id) a3\
            ON a3.customer_id=c1.customer_id\
            LEFT JOIN\
            (SELECT customer_id, AVG(price) as avgPriceYear FROM sales\
            WHERE DATE_SUB(CURDATE(),INTERVAL 365 DAY) <= date\
            GROUP BY customer_id) a1\
            ON a1.customer_id=c1.customer_id\
            LEFT JOIN\
            (SELECT customer_id, AVG(sales.price) as avgPriceHalfYear FROM sales\
            WHERE DATE_SUB(CURDATE(),INTERVAL 180 DAY) <= date\
            GROUP BY customer_id) a2\
            ON a2.customer_id=c1.customer_id\
            ;\
            "

        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=cols)
        df['customer_id'] = df['customer_id'].astype(int)

        sys.stdout.write("Calculating car...Done\n")
        return df
    except:
        # return None
        # raise
        pass


def ppb(username='username', groupby='customer_id', raw=False, account='all', local=False):
    '''
    '''
    sys.stdout.write("Calculating ppb...\r")
    dbname = 'data_{}'.format(username)

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "SELECT distinct customer_id FROM sales"

        cur.execute(script)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]
        customer_ids = pd.DataFrame(data, columns=cols)

        script = "\
            SELECT product_id, COUNT(price) as prod_qty, sum(price) as price, sum(margin) as margin,\
            AVG(price) as mean_price, AVG(margin) as mean_margin,\
            STDDEV(price) as std_price, STDDEV(margin) as std_margin\
            FROM sales GROUP BY product_id\
            "
        cur.execute(script)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]
        prods = pd.DataFrame(data, columns=cols)

        _ppbs = pd.DataFrame()

        for id in customer_ids['customer_id'].values:
            script = "\
                SELECT customer_id, product_id, COUNT(price) as prod_qty, sum(price) as price, sum(margin) as margin,\
                AVG(price) as mean_price, AVG(margin) as mean_margin,\
                STDDEV(price) as std_price, STDDEV(margin) as std_margin\
                FROM sales WHERE customer_id={} GROUP BY product_id, customer_id\
                ".format(id)

            cur.execute(script)
            data = np.asarray(cur.fetchall())
            cols = [desc[0] for desc in cur.description]
            df = pd.DataFrame(data, columns=cols)

            if groupby == None:
                return df.to_json()
            else:
                for p in df['product_id'].unique():
                    df.loc[df['product_id'] == p, 'mean_prod_price'] = prods[prods['product_id'] == p]['mean_price'].values

                df.loc[df['mean_prod_price'] > df['mean_price'] * 1.15, 'ppb'] = 1
                df.loc[df['mean_prod_price'] < df['mean_price'] * 0.85, 'ppb'] = -1
                df.loc[(df['mean_price'] * 0.85 < df['mean_prod_price']) & (
                            df['mean_prod_price'] < df['mean_price'] * 1.15), 'ppb'] = 0

                ppbs = df.groupby(['customer_id'])[['prod_qty', 'price', 'margin', 'ppb']].sum().reset_index()
                ppb_count = df.groupby(['customer_id'])['ppb'].count().reset_index()
                ppbs['ppb_value'] = ppbs['ppb'] / ppb_count['ppb']
                ppbs.loc[ppbs['ppb_value'] > 0.1, 'ppb'] = 2
                ppbs.loc[ppbs['ppb_value'] < -0.1, 'ppb'] = 1
                ppbs.loc[(ppbs['ppb_value'] <= 0.1) & (ppbs['ppb_value'] >= -0.1), 'ppb'] = 0
                ppbs.loc[ppbs['ppb_value'].isnull(), 'ppb'] = 4

                ppbs['ppb'] = ppbs['ppb'].astype(int)

                ppbs['customer_id'] = ppbs['customer_id'].astype(int)

                try:
                    ppbs['size'] = np.log(ppbs['price'])
                except:
                    ppbs['size'] = 0

            _ppbs = _ppbs.append(ppbs)

        sys.stdout.write("Calculating ppb...Done\n")
        return _ppbs
    except:
        raise
        # pass


def getItemSuggestions(dbname='username', item='product', groupby='customer_id', raw=False, account='all', local=False):
    '''
    '''
    try:
        datadb = "data_" + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        sys.stdout.write("Calculating {} suggestions...\r".format(item))

        if item == 'product':
            item = 'item_name'
            script = "SELECT customers.id as customer_id, customers.name, products.name as item_name, sales.quantity as quantity FROM sales LEFT JOIN products ON\
            products.id=sales.product_id LEFT JOIN product_type ON product_type.id=products.product_type_id\
                    LEFT JOIN customers ON customers.id=sales.customer_id\
                    "
        if item == 'product_type':
            item = 'item_name'
            script = "SELECT customers.id as customer_id, customers.name, product_type.name as item_name, sales.quantity as quantity FROM sales LEFT JOIN products ON\
            products.id=sales.product_id LEFT JOIN product_type ON product_type.id=products.product_type_id\
                    LEFT JOIN customers ON customers.id=sales.customer_id\
                    "
        cur.execute(script)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]
        data = pd.DataFrame(data, columns=cols)

        g1 = data.groupby(['customer_id', item])['quantity'].sum().reset_index()
        items = []
        names = []
        for c in data['customer_id'].unique():
            names.append(c)
            items.append(g1[g1['customer_id'] == c][item].tolist())

        oht = OnehotTransactions()
        oht_ary = oht.fit(items).transform(items)
        df = pd.DataFrame(oht_ary, columns=oht.columns_)

        for s in (0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.29, 0.28, 0.27, 0.26, 0.25, 0.24, 0.22, 0.2, 0.18, 0.16, 0.14, 0.12, 0.1, 0.095, 0.09, 0.085, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.029, 0.028, 0.027, 0.026, 0.025, 0.024, 0.023, 0.022, 0.021, 0.02, 0.015, 0.01):
            # for s in (0.01, 0.03, 0.08, 0.15, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
            print(s)
            frequent_itemsets = apriori(df, min_support=s, use_colnames=True)
            frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
            try:
                rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.5)
                print(len(rules.index))
                if len(rules.index) >= 10:
                # if len(rules.index) < 20:
                    print("Frequent item sets stopped...")
                    print(s)
                    print(len(rules.index))
                    break
            except:
                pass

        scoring = g1.groupby(['customer_id'])[item].count().reset_index()
        scoring['potential_items'] = ""
        scoring['potential'] = 0.
        maxItems = float(len(set(g1[item])))
        g3 = g1.groupby(['customer_id'])
        for n, g in g3:
            potential_items = []
            for i in rules.index:
                r1 = set(rules['antecedents'][i]).issubset(g[item])
                r2 = set(rules['consequents'][i]).issubset(g[item])
                if r1 and ~r2:
                    potential_items += tuple(rules['consequents'][i])

                scoring.loc[scoring['customer_id'] == n, ['potential_items']] = " ".join(tuple(set(potential_items)))
                scoring.loc[scoring['customer_id'] == n, ['potential']] = len(set(potential_items)) / maxItems

        sys.stdout.write("Calculating {} suggestions...Done\n".format(item))
        return scoring
    except:
        raise


def customer_risk(username='username', groupby='customer_id', raw=False, account='all', local=False):
    '''
    '''
    df = car(username, groupby, raw, account, local)

    try:
        if groupby == None:
            return df.to_json()
        else:
            grouped = df.groupby(groupby)
            car_ = []
            for name, group in grouped:
                car_.append(group.to_json(orient='records'))
            return car_
    except:
        raise


def product_risk(username='username', groupby='name', raw=False, account='all', local=False):
    ''' Reads result's database, manipulate the data and returns it.
    '''
    dbname = 'data_{}'.format(username)

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script_cols = "\
            SELECT `COLUMN_NAME`\
            FROM `INFORMATION_SCHEMA`.`COLUMNS`\
            WHERE `TABLE_SCHEMA`='{}'\
            AND `TABLE_NAME`='{}';\
            ".format(dbname, 'sales')

        cur.execute(script_cols)
        cols = np.ravel(np.asarray(cur.fetchall()))
        cols = ['product_id', 'name', 'product_type', 'avgPriceYTD', 'avgPriceHYTD', 'risk']
        script_nop = "\
            SELECT a1.product_id, b1.name, b1.product_type, avgPriceYear, avgPriceHalfYear,\
            IF(avgPriceHalfYear=0, -1, IF(avgPriceHalfYear IS NULL, -1, ATAN2(avgPriceHalfYear-avgPriceYear, 185)/(PI()/2)))\
            FROM\
            (SELECT product_id, AVG(price) as avgPriceYear FROM sales\
            WHERE DATE_SUB(CURDATE(),INTERVAL 365 DAY) <= date\
            GROUP BY product_id) a1\
            LEFT JOIN\
            (SELECT product_id, AVG(price) as avgPriceHalfYear FROM sales\
            WHERE DATE_SUB(CURDATE(),INTERVAL 60 DAY) <= date\
            GROUP BY product_id) a2\
            ON a1.product_id=a2.product_id\
            LEFT JOIN\
            (SELECT p.id, p.name, pt.name AS 'product_type' FROM products AS p\
            LEFT JOIN product_type AS pt ON p.product_type_id = pt.id) b1\
            ON a1.product_id=b1.id\
            ;\
            "
        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())

        df = pd.DataFrame(data, columns=cols)
        grouped = df.groupby(groupby)
        prods = {}
        prods = []
        for name, group in grouped:
            # prods[name] = group.to_json(orient='records')
            prods.append(group.to_json(orient='records'))

        return prods

    except:
        raise


def product_type_risk(username='username', groupby='product_type', raw=False, account='all', local=False):
    ''' Reads result's database, manipulate the data and returns it.
    '''
    dbname = 'data_{}'.format(username)

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script_cols = "\
            SELECT `COLUMN_NAME`\
            FROM `INFORMATION_SCHEMA`.`COLUMNS`\
            WHERE `TABLE_SCHEMA`='{}'\
            AND `TABLE_NAME`='{}';\
            ".format(dbname, 'sales')

        cur.execute(script_cols)
        cols = np.ravel(np.asarray(cur.fetchall()))
        cols = ['product_id', 'name', 'product_type', 'avgPriceYTD', 'avgPriceHYTD', 'risk']
        # avgPriceYear/avgPriceHalfYear
        script_nop = "\
            SELECT a1.product_id, b1.name, b1.product_type, avgPriceYear, avgPriceHalfYear,\
            IF(avgPriceHalfYear=0, -1, IF(avgPriceHalfYear IS NULL, -1, ATAN2(avgPriceHalfYear-avgPriceYear, 185)/(PI()/2)))\
            FROM\
            (SELECT product_id, IF(AVG(price)=NULL, 0, AVG(price)) as avgPriceYear FROM sales\
            WHERE DATE_SUB(CURDATE(),INTERVAL 365 DAY) <= date\
            GROUP BY product_id) a1\
            LEFT JOIN\
            (SELECT product_id, IF(AVG(price)=NULL, 0, AVG(price)) as avgPriceHalfYear FROM sales\
            WHERE DATE_SUB(CURDATE(),INTERVAL 180 DAY) <= date\
            GROUP BY product_id) a2\
            ON a1.product_id=a2.product_id\
            LEFT JOIN\
            (SELECT p.id, p.name, pt.name AS 'product_type' FROM products AS p\
            LEFT JOIN product_type AS pt ON p.product_type_id = pt.id) b1\
            ON a1.product_id=b1.id\
            ;\
            "
        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())
        df = pd.DataFrame(data, columns=cols)
        # return df.groupby(by=[groupby])['avgPriceYTD', 'avgPriceHYTD', 'risk'].sum().reset_index().to_json(orient='records')
        df = df.groupby(by=[groupby])['avgPriceYTD', 'avgPriceHYTD'].sum().reset_index()
        df['risk'] = np.arctan2(df['avgPriceHYTD'] - df['avgPriceYTD'], 185) * 0.5 / np.pi
        return df.to_json(orient='records')

    except:
        # raise
        pass


if __name__ == "__main__":
    username = 'martinmasip'
    local = True
    local = False
    dbname = 'qymatix___solutions_com'
    # username = 'coldjet_qy'
    dbname = 'qymatix___solutions_com'
    dbname = 'qy___test_com'
    dbname = 'qymatix_best'
    dbname = 'aet_at'
    # dbname = 'orbusneich_com'

    # res = getItemSuggestions(dbname, item='product')
    # res = getItemSuggestions(dbname, item='product_type')
    res = ppb(dbname)
    # res = ccbm(dbname)
    print(res[:90])
    print(res.columns)
