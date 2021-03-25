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
    from api.infrastructure.mysql import connection

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

    import datetime
    from api.infrastructure.mysql import connection

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
            # data['name'] = unquote_plus(data['name'])
            # try:
            #     data['name'] = data['name'].decode('utf-8').encode('cp1252')
            # except:
            #     data['name'] = data['name'].encode('cp1252')

            account = data['name']

            if account != "":
                script = "\
                    SELECT id FROM {}.customers WHERE name = '{}'\
                    ".format('data_' + dbname, account)

            cur.execute(script)
            # con.commit()
            try:
                account_id = np.ravel(np.asarray(cur.fetchall()))[0]
                data['customer_id'] = account_id
            except:
                pass

        if type(data['product_type_cross_selling']) == bytes:
            data['product_type_cross_selling'] = str(data['product_type_cross_selling'], 'utf-8')
        else:
            data['product_type_cross_selling'] = str(data['product_type_cross_selling'])


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

        # print(script)
        cur.execute(script)
        con.commit()

        script = "\
            SELECT MAX(row_names) from critters;\
            "
        cur.execute(script)
        # con.commit()

        # customer_id = np.ravel(np.asarray(cur.fetchall()))[0]
        customer_id = cur.fetchall()[0][0]


        return customer_id

    # except mysql.Error as e:
    #     print("Error {}: {}".format(e.args[0], e.args[1]))
    except Exception as e:
        print(e)
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


# pd.set_option('display.expand_frame_repr', False)
from api.qymatix import config

# print("Deleting old results db...")
# config.dropDatabase(dbname='results_' + dbname, local=local)
# print("Deleting old results db...Done")
# print("Creating new db...")
# config.createDatabase(dbname='results_' + dbname, local=local)
# print("Creating new db...Done")
# print("Creating new results table...")
# addCrittersTable(dbname, local=local)
# print("Creating new results table...Done")


# dbname = 'pfisterer_de'
# dbname = 'clarus___films_com'

dbname = 'granzow_de'
dbname = 'hartl___online_de'

clearCrittersTable(dbname)

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



