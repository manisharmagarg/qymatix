# import MySQLdb as mysql
import datetime
import os

import numpy as np

from api.qymatix import customers
from api.qymatix import kam
from api.qymatix import products
from api.infrastructure.mysql import connection
import traceback

_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path, '../../..'))
_basepath = '/home/webuser'


def insertSalesRecord(data, dbname, local=False):
    # created = str(datetime.datetime.now())
    if 'customer_id' not in data.keys():
        customer_id = customers.insertCustomer({"name": data.get('customer')}, dbname, local=local)
    else:
        customer_id = data.get('customer_id')
    if 'product_id' not in data.keys():
        product_id = products.insertProduct({"name": data.get('product')}, dbname, local=local)
    else:
        product_id = data.get('product_id')

    try:
        try:
            date = datetime.datetime.strptime(data.get('date'), "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            date = datetime.datetime.strptime(data.get('date'), "%Y-%m-%d")
    except Exception as e:
        return str(traceback.format_exc())
        return "Wrong date format."

    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if 'kam' not in data.keys():
            data['kam'] = ''
        else:
            kamdata = dict()
            kamdata['name'] = data.get('kam')
            user_id = kam.insertKam(dbname, kamdata, local=local)

        user_id = 1
        script = "INSERT INTO `sales` (customer_id, product_id, quantity, price, cost, margin, year, month, date, invoice, kam) "\
            "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
                customer_id, 
                product_id, 
                data.get('quantity'), 
                data.get('price'), 
                data.get('cost'), 
                data.get('margin'), 
                date.year, 
                date.month, 
                data.get('date'), 
                data.get('invoice'), 
                # data['kam'],
                user_id, 
            )

        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from sales;"
        cur.execute(script)
        # con.commit()
        sale_id = np.ravel(np.asarray(cur.fetchall()))[0]
        return str(sale_id)

    except Exception as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        if int(e.args[0]) == 1062:
            return 'Customer already exists'
        # sys.exit(1)
        raise


def insert_sales_record(con, data, local=False):
    '''
    '''
    # created = str(datetime.datetime.now())

    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    _dbname = 'data_' + dbname
    cur.execute("USE {}".format(_dbname))

    try:
        try:
            date = datetime.datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S")
        except:
            date = datetime.datetime.strptime(data['date'], "%Y-%m-%d")
    except:
        return "Wrong date format."

    try:
        cur = con.cursor()

        script = "\
            SELECT u.id FROM {0}.users AS u\
            LEFT JOIN {0}.Users_Customers AS uc\
            ON uc.user_id=u.id\
            WHERE uc.customer_id={1}\
            ".format('data_' + dbname, data['customer_id'])

        # print(script)
        cur.execute(script)
        # con.commit()
        user_id = np.ravel(np.asarray(cur.fetchall()))[0]
        # print(user_id)
        # user_id = data['user_id']
    except Exception as e:
        print(e)
        user_id = 4

    try:
        script = "\
            INSERT INTO sales\
            (customer_id, product_id, quantity, price, cost, margin, year, month, date, invoice, kam)\
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');\
            ".format( \
            data['customer_id'], \
            data['product_id'], \
            data['quantity'], \
            data['price'], \
            data['cost'], \
            data['margin'], \
            date.year, \
            date.month, \
            data['date'], \
            data['invoice'], \
            # data['kam'],\
            user_id, \
            )

        # print(script)
        # print(">>>>")
        cur.execute(script)
        con.commit()

        script = "\
            SELECT MAX(id) from sales;\
            "
        cur.execute(script)
        # con.commit()

        sale_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return sale_id
        '''
        return
        '''

    except Exception as e:
        print(script)
        print(e)
        print("XXXX")
    # except mysql.Error as e:
    # print("Error {}: {}".format(e.args[0], e.args[1]))
    # if int(e.args[0]) == 1062:
    # return 'Customer already exists'
    # sys.exit(1)
    # raise
