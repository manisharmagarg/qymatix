import numpy as np


def ppb(username='username', groupby='customer_id', raw=False, account='all', local=False):
    '''
    '''
    sys.stdout.write("Calculating ppb...\r")
    dbname = 'data_{}'.format(username)

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "\
			SELECT customer_id, product_id, COUNT(price) as prod_qty, sum(price) as price, sum(margin) as margin,\
            AVG(price) as mean_price, AVG(margin) as mean_margin,\
            STDDEV(price) as std_price, STDDEV(margin) as std_margin\
			FROM sales GROUP BY product_id, customer_id\
			"

        cur.execute(script)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=cols)

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

        ppb = calculate_ppb_command.execute()

        return ppb


    except:
        raise
        # pass