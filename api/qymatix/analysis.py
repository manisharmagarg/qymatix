import datetime
import logging
from urllib.parse import unquote_plus

import MySQLdb as mysql
import numpy as np

from api.qymatix import config
from api.qymatix.analytics import analytics
from api.infrastructure.mysql import connection

logger = logging.getLogger('django.request')


def clearCrittersTable(username, con=None):
    '''
    '''
    dbname = "results_" + username

    if con == None:
        CLOSE_CON = True
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()

    else:
        CLOSE_CON = False

    cur = con.cursor()

    try:
        # SET foreign_key_checks=0;TRUNCATE TABLE products; SET foreign_key_checks=1;
        query = "\
            TRUNCATE TABLE critters;\
        ".format(username)

        cur.execute(query)
        con.commit()

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def addCrittersTable(username, con=None):
    '''
    '''

    dbname = "results_" + username

    if con == None:
        CLOSE_CON = True
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
    else:
        CLOSE_CON = False

    cur = con.cursor()

    try:
        query = "\
           CREATE TABLE `critters` (\
              `row_names` text NOT NULL,\
              `name` text NOT NULL,\
              `sales` text NOT NULL,\
              `size` text NOT NULL,\
              `risk` text NOT NULL,\
              `margin` text NOT NULL,\
              `ppb` text NOT NULL,\
              `ccbm` text NOT NULL,\
              `product_cross_selling` text NOT NULL,\
              `product_type_cross_selling` text NOT NULL\
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;\
        ".format(username)

        cur.execute(query)
        con.commit()

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def addResultsTable(username, con=None):
    '''
    '''

    dbname = "results_" + username

    if con == None:
        CLOSE_CON = True
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
    else:
        CLOSE_CON = False

    cur = con.cursor()

    try:
        # script = "CREATE TABLE Users_Customers (user_id INT NOT NULL,\
        # customer_id INT NOT NULL,PRIMARY KEY\
        # (user_id,customer_id),FOREIGN KEY (user_id) REFERENCES\
        # users(id) ON UPDATE CASCADE,FOREIGN KEY (customer_id)\
        # REFERENCES {}.customers(id) ON UPDATE CASCADE);".format(dbname.replace("data_", "data_"))
        query = "\
           CREATE TABLE `analysis` (\
              `id` int(11) NOT NULL AUTO_INCREMENT,\
              `customer_id` int(11) NOT NULL,\
              `ccbm` varchar(255) NOT NULL,\
              `risk` double NOT NULL,\
              `ccpm` double NOT NULL,\
              `created` datetime NOT NULL,\
              PRIMARY KEY (`id`),\
              UNIQUE KEY `customer_id` (`customer_id`),\
              KEY `analysis_customer_id` (`customer_id`),\
              CONSTRAINT `analysis_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `data_{}`.`customers` (`id`)\
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;\
        ".format(username)
        # CONSTRAINT `analysis_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `data_{}.customers` (`id`)\

        cur.execute(query)
        con.commit()

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # raise

    finally:
        if CLOSE_CON:
            if con:
                con.close()


def insertResult(dbname, data):
    '''
    Inserts results of the analysis into the results.analysis table
    '''

    created = str(datetime.datetime.now())

    # if 'customer_id' not in data.keys():
    # data = 'Name missing. Cannot insert unknown contact.'
    # return data
    if 'ccbm' not in data.keys():
        data['ccbm'] = 0
    if 'ccpm' not in data.keys():
        data['ccpm'] = None
    if 'ppb' not in data.keys():
        data['ppb'] = None
    if 'size' not in data.keys():
        data['size'] = None
    if 'sales' not in data.keys():
        data['sales'] = None
    if 'margin' not in data.keys():
        data['margin'] = None
    if 'risk' not in data.keys():
        data['risk'] = None
    if 'product_cross_selling' not in data.keys():
        data['product_cross_selling'] = ""
    if 'product_type_cross_selling' not in data.keys():
        data['product_type_cross_selling'] = ""
    if 'product_type_cross_selling' in ('nan', '()'):
        data['product_type_cross_selling'] = ""

    data['created'] = created

    try:
        data['product_type_cross_selling'] = data['product_type_cross_selling'].decode('utf-8').encode('cp1252')
    except:
        data['product_type_cross_selling'] = data['product_type_cross_selling'].encode('cp1252')

    try:
        datadb = 'results_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()

        cur = con.cursor()

        if 'name' in data.keys():
            data['name'] = unquote_plus(data['name'])
            try:
                data['name'] = data['name'].decode('utf-8').encode('cp1252')
            except:
                data['name'] = data['name'].encode('cp1252')

            account = data['name']

            if account != "":
                script = "\
                    SELECT id FROM {}.customers WHERE name = '{}'\
                    ".format('data_' + dbname, account)

            cur.execute(script)
            con.commit()
            try:
                account_id = np.ravel(np.asarray(cur.fetchall()))[0]
                data['customer_id'] = account_id
            except:
                pass

        script = "\
            INSERT INTO `critters`\
            (row_names, name, sales, size, risk, margin, ppb, ccbm, product_cross_selling, product_type_cross_selling)\
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');\
            ".format( \
            # data['customer_id'],\
            # data['customer_name'],\
            data['row_names'], \
            data['customer_id'], \
            data['sales'], \
            data['size'], \
            data['risk'], \
            data['margin'], \
            data['ppb'], \
            data['ccbm'], \
            data['product_cross_selling'], \
            data['product_type_cross_selling'] \
            )

        cur.execute(script)
        con.commit()

        script = "\
            SELECT MAX(row_names) from critters;\
            "
        cur.execute(script)
        con.commit()

        customer_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return customer_id

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        raise


def insertAnalysis(data, dbname):
    '''
    Inserts results of the analysis into the results.analysis table
    '''

    created = str(datetime.datetime.now())

    if 'customer_id' not in data.keys():
        data = 'Name missing. Cannot insert unknown contact.'
        return data
    if 'ccbm' not in data.keys():
        data['ccbm'] = 0
    if 'ccpm' not in data.keys():
        data['ccpm'] = 0

    data['created'] = created

    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()

        cur = con.cursor()

        if data['account'] != '':
            script = "\
                SELECT id from customers WHERE customers.name='{}';\
                ".format(data['account'])
            cur.execute(script)
            con.commit()
            data['account_id'] = np.ravel(np.asarray(cur.fetchall()))[0]

            # (name, address, postcode, city, country, webpage, description, contact)\
        script = "\
            INSERT INTO `contacts`\
            (name, title, description, customer_id, function, phone, email, linkedin, xing, created)\
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');\
            ".format(data['name'], data['title'], data['description'], \
                     data['account_id'], \
                     data['function'], \
                     data['phone'], \
                     data['email'], \
                     data['linkedin'], \
                     data['xing'], \
                     data['created'] \
                     )

        cur.execute(script)
        con.commit()

        script = "\
            SELECT MAX(id) from contacts;\
            "
        cur.execute(script)
        con.commit()

        contact_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return contact_id

    except mysql.Error as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        if int(e.args[0]) == 1062:
            script = "\
                SELECT id FROM contacts WHERE name='{}';\
                ".format(data['name'])

            cur.execute(script)
            con.commit()

            contact_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return contact_id

            # return 'Contact already exists'
        # sys.exit(1)
        raise


def getResults(username='username', raw=False, account='all'):
    ''' Reads result's database, manipulate the data and returns it.
    '''

    resultsdb = 'results_{}'.format(username)

    try:
        mysql_connection = connection.MySQLConnection(resultsdb)
        con = mysql_connection.connect()

        cur = con.cursor()

        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')

        # script_nop = "\
        # SELECT * from customers;\
        # "
        if account == 'all':
            script_nop = "\
                SELECT * from critters;\
                "
        else:
            script_nop = "\
                SELECT * from critters\
                WHERE name='{}';\
                ".format(account)

        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())
        # print(data)

        # script_nop = "\
        # SELECT `COLUMN_NAME`\
        # FROM `INFORMATION_SCHEMA`.`COLUMNS`\
        # WHERE `TABLE_SCHEMA`='results_{}'\
        # AND `TABLE_NAME`='customers';\
        # ".format(username)

        script_nop = "\
            SELECT `COLUMN_NAME`\
            FROM `INFORMATION_SCHEMA`.`COLUMNS`\
            WHERE `TABLE_SCHEMA`='results_{}'\
            AND `TABLE_NAME`='critters';\
            ".format(username)
        # show columns from customers;\

        cur.execute(script_nop)
        cols = np.ravel(np.asarray(cur.fetchall()))

        results = dict()
        for c in cols:
            values = np.ravel(data[:, np.where(cols == c)])
            if not raw:
                if c != 'name':
                    values = values.astype(np.float)
                    values = np.around(np.nan_to_num(values), 2)
                # if c == 'ccbm':
                if c == 'risk':
                    results['rawRisk'] = values.tolist()
                    # values = colortables.convertToColor(values)
                    # values = colortables.colorK1(values, 'json')

            results[c] = values.tolist()

    except mysql.Error as e:
        print("Error {0}: {1}".format(e.args[0], e.args[1]))
        print("XXXX")
        # sys.exit(1)
        results = {}
    finally:
        try:
            con.close()
        except:
            pass

    return results


def results(dbname, groupby='customer_id', raw=False, account='all', local=False):
    '''
    '''
    # pd.set_option('display.expand_frame_repr', False)

    print("Deleting old results db...")
    config.dropDatabase(dbname='results_' + dbname, local=local)
    print("Deleting old results db...Done")
    print("Creating new db...")
    config.createDatabase(dbname='results_' + dbname, local=local)
    print("Creating new db...Done")
    print("Creating new results table...")
    addCrittersTable(dbname, local=local)
    print("Creating new results table...Done")

    results = analytics.results(dbname)
    # print(results)
    # dd

    print("Storing results...")
    for i in range(len(results.index)):
        r = results.loc[i, ['row_names', 'customer_id', 'sales', 'size', 'risk', 'margin', 'ppb', 'ccbm', \
                            'product_cross_selling', 'product_type_cross_selling']].to_dict()
        try:
            insertResult(dbname=dbname, data=r)
        except:
            raise
            # pass

    print("Storing results...Done")


if __name__ == "__main__":
    username = 'martinmasip'
    local = True
    local = False
    # dbname = 'qymatix___solutions_com'
    # username = 'coldjet_qy'
    # addResultsTable(username, local=local)
    # dbname = 'qymatix___solutions_com'
    # dbname = 'qymatix_best'
    # dbname = 'qymatix___aet_com'
    # dbname = 'orbusneich_com'
    # dbname = 'qy___test_com'
    dbname = 'qy___wine_con'
    # dbname = 'manhand___test_de'
    dbname = 'aet_at'

    # config.dropDatabase(dbname='results_' + dbname, local=local)
    # config.createDatabase(dbname='results_' + dbname, local=local)
    # addCrittersTable(dbname, local=local)

    # results = getResults(username=username, local=local)
    # print(results)
    results(dbname)
