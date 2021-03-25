"""
Products script deals with the products databases queries
"""
# pylint: disable=invalid-name
# pylint: disable=import-error
# pylint: disable=broad-except
# pylint: disable=bare-except
# pylint: disable=redefined-outer-name
# pylint: disable=pointless-string-statement
# pylint: disable=unused-variable
# pylint: disable=unused-argument
# pylint: disable=too-many-locals
# pylint: disable=too-many-format-args
# pylint: disable=lost-exception
# pylint: disable=undefined-variable
# pylint: disable=too-many-nested-blocks
# pylint: disable=using-constant-test
# pylint: disable=no-name-in-module
# pylint: disable=too-many-arguments
# pylint: disable=too-many-lines
# pylint: disable=inconsistent-return-statements
# pylint: disable=too-many-branches
import datetime
import json
import os
import logging
import traceback
from urllib.parse import unquote_plus
import numpy as np
import pandas as pd
import MySQLdb as mysql
from ..infrastructure.mysql import  connection


logger = logging.getLogger(__name__)

_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path, '../../..'))
_basepath = '/home/webuser'


def insertProduct(data, dbname, local=False):
    """
    function: Query to create the products
    """
    data['created'] = str(datetime.datetime.now())

    if 'name' not in data.keys():
        data = 'Name missing. Cannot insert unknown customer.'
        return data
    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()

        if 'product_type_id' not in data.keys():
            data['product_type_id'] = 1
        if 'description' not in data.keys():
            data['description'] = ''
        if 'active' not in data.keys():
            data['active'] = 1
        if 'number' not in data.keys():
            data['number'] = 'NULL'
        if 'serial' not in data.keys():
            data['serial'] = 'NULL'

        # for k in ('name', 'description'):
        #     data[k] = unquote_plus(data[k])
        #     try:
        #         data[k] = data[k].strip().decode('utf-8').encode('cp1252')
        #     except:
        #         data[k] = data[k].encode('cp1252')

            # INSERT IGNORE INTO `products`\
        script = "INSERT INTO `products` " \
                 "(name, product_type_id, description, active, created, " \
                 "number, serial) VALUES " \
                 "('{}','{}','{}','{}','{}','{}','{}'" \
                 ");".format(data['name'], data['product_type_id'],
                             data['description'], data['active'],
                             data['created'], data['number'], data['serial'])

        cur.execute(script)
        con.commit()

        script = "\
            SELECT MAX(id) from products;\
            "
        cur.execute(script)
        con.commit()

        product_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return product_id

    except Exception as e:

        script = "\
            SELECT id FROM products WHERE name='{}';\
            ".format(data['name'])

        cur.execute(script)
        con.commit()

        product_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return product_id

        # return 'Product already exists'
        # sys.exit(1)
        # raise


def insert_product(con, data, local=False):
    """
    function: Query to create the products
    return : new product id
    """
    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    dbname = 'data_' + dbname
    cur.execute("USE {}".format(dbname))

    data['created'] = str(datetime.datetime.now())

    if 'name' not in data.keys():
        data = 'Name missing. Cannot insert unknown customer.'
        return data
    try:

        if 'product_type_id' not in data.keys():
            data['product_type_id'] = 1
        if 'description' not in data.keys():
            data['description'] = ''
        if 'active' not in data.keys():
            data['active'] = 1
        if 'number' not in data.keys():
            data['number'] = 'NULL'
        if 'serial' not in data.keys():
            data['serial'] = 'NULL'

        # for k in ('name', 'description'):
            # data[k] = unquote_plus(data[k])
            # try:
            #     data[k] = data[k].strip().decode('utf-8').encode('cp1252')
            # except:
            #     data[k] = data[k].encode('cp1252')

        script = "INSERT INTO `products` " \
                 "(name, product_type_id, description, " \
                 "active, created, number, serial) VALUES " \
                 "('{}','{}','{}','{}','{}','{}','{}')" \
                 ";".format(data['name'], data['product_type_id'],
                            data['description'], data['active'],
                            data['created'], data['number'],
                            data['serial'])

        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from products;"
        cur.execute(script)

        product_id = np.ravel(np.asarray(cur.fetchall()))[0]
        return product_id

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )


def get_product_line_id(con, name, local=False):
    """
    function: query to get the product line id
    """
    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    dbname = 'data_' + dbname
    cur.execute("USE {}".format(dbname))

    # data[k] = unquote_plus(data[k])
    # try:
    #     name = name.strip().decode('utf-8').encode('cp1252')
    # except:
    #     name = name.encode('cp1252')

    try:
        script = "SELECT id FROM product_line WHERE name='{}';".format(name)

        cur.execute(script)
        product_line_id = np.ravel(np.asarray(cur.fetchall()))[0]
        return product_line_id
    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        return ''


def get_product_type_id(con, name, local=False):
    """
    function: query for to get the product type id
    """
    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    dbname = 'data_' + dbname
    cur.execute("USE {}".format(dbname))

    # data[k] = unquote_plus(data[k])
    # try:
    #     name = name.strip().decode('utf-8').encode('cp1252')
    # except:
    #     name = name.encode('cp1252')

    try:
        script = "SELECT id FROM product_type WHERE name='{}';".format(name)
        cur.execute(script)

        try:
            product_type_id = np.ravel(np.asarray(cur.fetchall()))[0]
        except:
            product_type_id = 1
    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        return ''

    return product_type_id


def insert_product_type(con, data, local=False):
    """
    function: query to create the product type
    """
    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    dbname = 'data_' + dbname
    cur.execute("USE {}".format(dbname))

    data['created'] = str(datetime.datetime.now())

    if 'name' not in data.keys():
        data = 'Name missing. Cannot insert unknown customer.'
        return data

    try:
        if 'product_line_id' not in data.keys():
            data['product_line_id'] = 1
        if 'description' not in data.keys():
            data['description'] = ''
        if 'active' not in data.keys():
            data['active'] = 1
        if 'number' not in data.keys():
            data['number'] = 'NULL'

        # for k in ('name', 'description'):
            # data[k] = unquote_plus(data[k])
            # try:
            #     data[k] = data[k].strip().decode('utf-8').encode('cp1252')
            # except:
            #     data[k] = data[k].encode('cp1252')

        script = "SET foreign_key_checks=0"
        cur.execute(script)
        con.commit()

        script = "INSERT INTO `product_type` " \
                 "(name, product_line_id, description, " \
                 "active, created, number) VALUES " \
                 "('{}','{}','{}','{}','{}','{}')" \
                 ";".format(data['name'], data['product_line_id'],
                            data['description'], data['active'],
                            data['created'],
                            data['number'])

        cur.execute(script)
        con.commit()

        script = "SET foreign_key_checks=1"
        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from product_type;"
        cur.execute(script)

        product_type_id = np.ravel(np.asarray(cur.fetchall()))[0]
        return product_type_id

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        if int(exception.args[0]) == 1062:
            script = "SELECT id FROM product_type " \
                     "WHERE name='{}';".format(data['name'])

            cur.execute(script)
            con.commit()

            product_type_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return product_type_id


def insertProductType(data, dbname):
    """
    function: Query to create the product type record
    """
    data['created'] = str(datetime.datetime.now())

    if 'name' not in data.keys():
        data = 'Name missing. Cannot insert unknown customer.'
        return data
    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if 'product_line_id' not in data.keys():
            data['product_line_id'] = 1
        if 'description' not in data.keys():
            data['description'] = ''
        if 'active' not in data.keys():
            data['active'] = 1
        if 'number' not in data.keys():
            data['number'] = 'NULL'

        # for k in ('name', 'description'):
        #     data[k] = unquote_plus(data[k])
        #     try:
        #         data[k] = data[k].strip().decode('utf-8').encode('cp1252')
        #     except:
        #         data[k] = data[k].encode('cp1252')

        script = "SET foreign_key_checks=0"
        cur.execute(script)
        con.commit()

        script = "INSERT INTO `product_type` " \
                 "(name, product_line_id, description, active, created, " \
                 "number) VALUES " \
                 "('{}','{}','{}','{}','{}'," \
                 "'{}');".format(data['name'], data['product_line_id'],
                                 data['description'], data['active'],
                                 data['created'], data['number'])

        cur.execute(script)
        con.commit()

        script = "SET foreign_key_checks=1"
        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from product_type;"
        cur.execute(script)
        con.commit()

        product_type_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return product_type_id

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        if int(exception.args[0]) == 1062:
            script = "SELECT id FROM product_type " \
                     "WHERE name='{}';".format(data['name'])

            cur.execute(script)
            con.commit()

            product_type_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return product_type_id


def insert_product_line(con, data):
    """
    function: Query to insert product line record
    """
    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    dbname = 'data_' + dbname
    cur.execute("USE {}".format(dbname))

    data['created'] = str(datetime.datetime.now())

    if 'name' not in data.keys():
        data = 'Name missing. Cannot insert unknown product line.'
        return data
    try:
        if 'product_class_id' not in data.keys():
            data['product_class_id'] = 1
        if 'description' not in data.keys():
            data['description'] = ''
        if 'active' not in data.keys():
            data['active'] = 1
        if 'number' not in data.keys():
            data['number'] = 'NULL'

        # for k in ('name', 'description'):
        #     try:
        #         data[k] = data[k].strip().decode('utf-8').encode('cp1252')
        #     except:
        #         data[k] = data[k].encode('cp1252')

        script = "INSERT INTO `product_line` " \
                 "(name, product_class_id, description, " \
                 "active, created, number) VALUES ('{}','{}','{}','{}','{}'," \
                 "'{}');".format(data['name'], data['product_class_id'],
                                 data['description'], data['active'],
                                 data['created'], data['number'])

        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from product_line;"
        cur.execute(script)

        product_type_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return product_type_id

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        if int(exception.args[0]) == 1062:
            script = "SELECT id FROM product_line WHERE " \
                     "name='{}';".format(data['name'])

            cur.execute(script)
            con.commit()

            product_line_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return product_line_id


def insertProductLine(data, dbname):
    """
    function: Query to create the product line
    """
    data['created'] = str(datetime.datetime.now())

    if 'name' not in data.keys():
        data = 'Name missing. Cannot insert unknown product line.'
        return data
    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if 'product_class_id' not in data.keys():
            data['product_class_id'] = 1
        if 'description' not in data.keys():
            data['description'] = ''
        if 'active' not in data.keys():
            data['active'] = 1
        if 'number' not in data.keys():
            data['number'] = 'NULL'

        # for k in ('name', 'description'):
        #     data[k] = unquote_plus(data[k])
        #     try:
        #         data[k] = data[k].strip().decode('utf-8').encode('cp1252')
        #     except:
        #         data[k] = data[k].encode('cp1252')

        script = "\
            INSERT INTO `product_line` (name, product_class_id, " \
                 "description, active, created, number) VALUES ('{}','{}'," \
                 "'{}','{}','{}','{}');".format(data['name'],
                                                data['product_class_id'],
                                                data['description'],
                                                data['active'],
                                                data['created'],
                                                data['number'])

        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from product_line;"
        cur.execute(script)
        con.commit()

        product_type_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return product_type_id

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        if int(exception.args[0]) == 1062:
            script = "SELECT id FROM product_line " \
                     "WHERE name='{}';".format(data['name'])

            cur.execute(script)
            con.commit()

            product_line_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return product_line_id


def insert_product_class(con, data):
    """
    function: Query to create the product class
    """
    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    dbname = 'data_' + dbname
    cur.execute("USE {}".format(dbname))

    data['created'] = str(datetime.datetime.now())

    if 'name' not in data.keys():
        data = 'Name missing. Cannot insert unknown product class.'
        return data
    try:

        cur = con.cursor()

        if 'description' not in data.keys():
            data['description'] = ''
        if 'active' not in data.keys():
            data['active'] = 1
        if 'number' not in data.keys():
            data['number'] = 'NULL'

        if False:
            for k in ('name', 'description'):
                data[k] = unquote_plus(data[k])
                try:
                    data[k] = data[k].strip().decode('utf-8').encode('cp1252')
                except:
                    data[k] = data[k].encode('cp1252')

        script = "INSERT INTO `product_class` " \
                 "(name, description, active, created) " \
                 "VALUES ('{}','{}','{}','{}');".format(data['name'],
                                                        data['description'],
                                                        data['active'],
                                                        data['created'])

        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from product_class;"
        cur.execute(script)

        product_class_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return product_class_id

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        if int(exception.args[0]) == 1062:
            script = "SELECT id FROM product_class " \
                     "WHERE name='{}';".format(data['name'])

            cur.execute(script)
            con.commit()

            product_class_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return product_class_id


def insertProductClass(data, dbname):
    """
    function: Query to create the product class
    """
    data['created'] = str(datetime.datetime.now())

    if 'name' not in data.keys():
        data = 'Name missing. Cannot insert unknown product class.'
        return data
    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if 'description' not in data.keys():
            data['description'] = ''
        if 'active' not in data.keys():
            data['active'] = 1
        if 'number' not in data.keys():
            data['number'] = 'NULL'

        if False:
            for k in ('name', 'description'):
                data[k] = unquote_plus(data[k])
                try:
                    data[k] = data[k].strip().decode('utf-8').encode('cp1252')
                except:
                    data[k] = data[k].encode('cp1252')

        script = "INSERT INTO `product_class` " \
                 "(name, description, active, created, number) VALUES (" \
                 "'{}','{}','{}','{}','{}');".format(data['name'],
                                                     data['description'],
                                                     data['active'],
                                                     data['created'],
                                                     data['number'])

        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from product_class;"

        cur.execute(script)
        con.commit()

        product_class_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return product_class_id

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        if int(exception.args[0]) == 1062:
            script = "SELECT id FROM product_class " \
                     "WHERE name='{}';".format(data['name'])

            cur.execute(script)
            con.commit()

            product_class_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return product_class_id


def modifyProduct(dbname, product, table='products'):
    """
    function: Query to updat the product record
    """
    try:
        if table not in ['products', 'product_type', 'product_line', 'product_class']:
            return 'false'

        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        for col in product.keys():
            if col not in ('id', 'created'):
                value = product[col]
                if col in ('Comment', 'comment', 'description'):
                    col = 'description'
                    # value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                    value = unquote_plus(value)
                    try:
                        value = value.decode('utf-8').encode('cp1252')
                    except:
                        value = value.encode('cp1252')
                if col == 'name':
                    value = unquote_plus(value)
                    try:
                        value = value.decode('utf-8').encode('cp1252')
                    except:
                        value = value.encode('cp1252')
                prod_id = product['id']
                script = "UPDATE {} SET {}='{}' " \
                         "WHERE id={}".format(table, col, value, prod_id)
                cur.execute(script)
                con.commit()

            response = 'true'

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        if exception.args[0] == 1062:
            response = 'true'
        else:
            response = 'false'

    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. " \
                   "Contact your administrator."

    return response


def dropProduct(dbname, table, prod_id):
    """
    function: Query to drop(delete) the product
    """

    try:
        if table not in ['products', 'product_type', 'product_line', 'product_class']:
            return 'false'

        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "DELETE FROM {} WHERE id = {}".format(table, prod_id)
        cur.execute(script)
        con.commit()

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )


def getProducts(dbname, product='all', local=False):
    """
    function: Query to get the products record
    """
    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if product == 'all':
            script = "SELECT p.*, pt.name AS 'product_type' " \
                     "FROM products AS p LEFT JOIN product_type AS pt " \
                     "ON p.product_type_id = pt.id;"
        else:
            script = "SELECT p.*, pt.name AS 'product_type' " \
                     "FROM products AS p LEFT JOIN product_type AS pt " \
                     "ON p.product_type_id = pt.id " \
                     "WHERE p.name = '{}'".format(product)
        cur.execute(script)

        columns = [desc[0] for desc in cur.description]
        data = np.asarray(cur.fetchall())
        df = pd.DataFrame(data, columns=columns)
        s = lambda x: x.encode('latin-1').decode('cp1252')
        df['description'] = df['description'].apply(s)
        df['name'] = df['name'].apply(s)
        return df.to_json(orient='records')

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        if False:
            script = "SELECT id FROM products " \
                     "WHERE name='{}';".format(data['name'])

            cur.execute(script)
            con.commit()

            product_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return product_id


def getProductsList(dbname, groupby=None, local=False):
    """
    function: Query to get the product list record
    """

    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        script_nop = "SELECT `COLUMN_NAME` " \
                     "FROM `INFORMATION_SCHEMA`.`COLUMNS` " \
                     "WHERE `TABLE_SCHEMA`='data_{}' " \
                     "AND `TABLE_NAME`='products';".format(dbname)

        cur.execute(script_nop)
        cols = np.ravel(np.asarray(cur.fetchall()))

        script = "SELECT p.*, pt.name AS 'product_type' FROM products AS p " \
                 "LEFT JOIN product_type AS pt ON p.product_type_id = pt.id"
        cur.execute(script)
        con.commit()

        prod_list = np.asarray(cur.fetchall())
        cols = np.append(cols, ['product_type'])

        try:
            df = pd.DataFrame(prod_list, columns=cols)

            s = lambda x: x.encode('latin-1').decode('cp1252')
            df['description'] = df['description'].apply(s)
            df['name'] = df['name'].apply(s)
            df['product_type'] = df['product_type'].apply(s)

            f = lambda x: x.isoformat().replace("T", " ") if x is not None else None
            df['created'] = df['created'].apply(f)

            if groupby is None:
                grouped = df.groupby('name')
            else:
                grouped = df.groupby(groupby)

            products = {}
            for name, group in grouped:
                # group = group.rename(
                # columns={'due':'due', 'action':'type',
                # 'description':'comment', 'plan':'plan_id'})
                # group[['due', 'id', 'created', 'action',
                # 'title', 'description' ]]
                products[name] = group.to_json(orient='records')
        except Exception as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )
            products = []

        return products

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        if int(exception.args[0]) == 1062:
            script = "SELECT id FROM products " \
                     "WHERE name='{}';".format(data['name'])

            cur.execute(script)
            con.commit()

            product_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return product_id


def getProductInsights(dbname, year=None, groupby='id', account="all", local=False):
    """
    function: Query to get thge product insights
    """
    try:
        if year is None:
            year = (datetime.datetime.now().year) - 1
            year = (datetime.datetime.now().year)

        year = str(year)

        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cursor = con.cursor()

        _dbname = 'data_' + dbname

        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')

        if account == "all":
            sql = "select sum(s.quantity) as quantity, " \
                  "sum(s.price) as sales, sum(s.margin) as margin, " \
                  "p.name, p.id, p.description, p.product_type_id, " \
                  "p.number, p.serial from {0}.sales as s " \
                  "inner join {0}.products as p on s.product_id=p.id " \
                  "WHERE YEAR(s.date)='{1}' " \
                  "GROUP BY p.{3} ; ".format(_dbname, year, account, groupby)
        else:
            sql = "SELECT CAST(SUM(s.quantity) AS signed) AS quantity, " \
                  "SUM(s.price) AS sales, SUM(s.margin) AS margin, " \
                  "p.name, p.id, p.description, p.product_type_id, " \
                  "p.number, p.serial FROM {0}.sales AS s " \
                  "INNER JOIN {0}.products p ON s.product_id=p.id " \
                  "INNER JOIN {0}.customers c ON s.customer_id=c.id " \
                  "WHERE YEAR(s.date)='{1}' AND c.name='{2}' " \
                  "GROUP BY p.{3} ; ".format(_dbname, year, account, groupby)

        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        data = np.asarray(cursor.fetchall())
        df = pd.DataFrame(data, columns=columns)
        return df.to_json(orient='records')

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )


def get_product_insights(dbname, year=None, groupby='id', account="all", local=False):
    """
    function: query to get the product insights record
    """
    try:
        if year is None:
            year = (datetime.datetime.now().year) - 1
            year = (datetime.datetime.now().year)

        year = str(year)

        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cursor = con.cursor()

        _dbname = 'data_' + dbname

        if account == "all":
            sql = "select sum(s.quantity) as quantity, " \
                  "sum(s.price) as sales, sum(s.margin) as margin, " \
                  "AVG(s.margin) AS avg_margin, MAX(s.price) AS max_price, " \
                  "MIN(s.price) AS min_price, AVG(s.price) AS avg_price, " \
                  "AVG(s.cost) AS avg_cost, p.name, p.id, " \
                  "p.description, p.product_type_id, p.number, " \
                  "p.serial from {0}.sales as s " \
                  "inner join {0}.products as p on s.product_id=p.id " \
                  "WHERE YEAR(s.date)='{1}' " \
                  "GROUP BY p.{3} ;".format(_dbname, year, account, groupby)
        else:
            sql = "select sum(s.quantity) as quantity, " \
                  "sum(s.price) as sales, sum(s.margin) as margin, " \
                  "AVG(s.margin) AS avg_margin, " \
                  "MAX(s.price) AS max_price, MIN(s.price) AS min_price, " \
                  "AVG(s.price) AS avg_price, AVG(s.cost) AS avg_cost, " \
                  "p.name, p.id, p.description, " \
                  "p.product_type_id, p.number, p.serial " \
                  "FROM {0}.sales AS s " \
                  "INNER JOIN {0}.products p ON s.product_id=p.id " \
                  "INNER JOIN {0}.customers c ON s.customer_id=c.id " \
                  "WHERE YEAR(s.date)='{1}' AND c.id='{2}' " \
                  "GROUP BY p.{3} ;".format(_dbname, year, account, groupby)

        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]

        data = np.asarray(cursor.fetchall())
        df = pd.DataFrame(data, columns=columns)

        grouped = df.groupby('id')

        cbp = get_customers_by_product(dbname, year=year, account=account)

        products = {}
        for name, group in grouped:
            products[name] = {}
            products[name]['insights'] = json.loads(
                group.to_json(orient='records')
            )[0]
            products[name]['insights_per_account'] = cbp[name]

        return products

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )

    con.close()


def get_customers_by_product(dbname, year=None, groupby='id', account="all", local=False):
    """
    function: Query to get the customers by product
    """
    try:
        if year is None:
            year = (datetime.datetime.now().year) - 1
            year = (datetime.datetime.now().year)

        year = str(year)

        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cursor = con.cursor()

        _dbname = 'data_' + dbname

        if account == "all":
            sql = "SELECT  s.customer_id AS account_id, " \
                  "s.product_id AS product_id, s.price, " \
                  "s.margin, s.quantity " \
                  "FROM {0}.sales as s " \
                  "WHERE YEAR(s.date)='{1}';".format(_dbname, year,
                                                     account, groupby)
        else:
            sql = "SELECT  s.customer_id AS account_id, " \
                  "s.product_id AS product_id, s.price, " \
                  "s.margin, s.quantity FROM {0}.sales as s " \
                  "WHERE YEAR(s.date)='{1}';".format(_dbname, year,
                                                     account, groupby)

        cursor.execute(sql)
        data = np.asarray(cursor.fetchall())
        columns = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(data, columns=columns)
        df['account_id'] = df['account_id'].astype(int)
        df['product_id'] = df['product_id'].astype(int)

        grouped = df.groupby('product_id')

        products = {}
        for name, group in grouped:
            products[name] = {}
            g = group.groupby('account_id')['price', 'margin', 'quantity'].mean().reset_index()
            products[name]['avg_quantity'] = json.loads(
                g['quantity'].to_json(orient='split')
            )['data']
            products[name]['avg_price'] = json.loads(
                g['price'].to_json(orient='split')
            )['data']
            products[name]['avg_margin'] = json.loads(
                g['margin'].to_json(orient='split')
            )['data']
            products[name]['account'] = json.loads(
                g['account_id'].to_json(orient='split')
            )['data']

            g = group.groupby('account_id')['price', 'margin', 'quantity'].min().reset_index()
            products[name]['min_quantity'] = json.loads(
                g['quantity'].to_json(orient='split')
            )['data']
            products[name]['min_price'] = json.loads(
                g['price'].to_json(orient='split')
            )['data']
            products[name]['min_margin'] = json.loads(
                g['margin'].to_json(orient='split')
            )['data']

            g = group.groupby('account_id')['price', 'margin', 'quantity'].max().reset_index()
            products[name]['max_quantity'] = json.loads(
                g['quantity'].to_json(orient='split')
            )['data']
            products[name]['max_price'] = json.loads(
                g['price'].to_json(orient='split')
            )['data']
            products[name]['max_margin'] = json.loads(
                g['margin'].to_json(orient='split')
            )['data']

            g = group.groupby('account_id')['price', 'margin', 'quantity'].sum().reset_index()
            products[name]['total_quantity'] = json.loads(
                g['quantity'].to_json(orient='split')
            )['data']
            products[name]['total_price'] = json.loads(
                g['price'].to_json(orient='split')
            )['data']
            products[name]['total_margin'] = json.loads(
                g['margin'].to_json(orient='split')
            )['data']

        return products

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )

    con.close()


def getProductTypeInsights(dbname, year=None, groupby='id', account="all", local=False):
    """
    function: Query to get the product type insights
    """
    try:
        if year is None:
            year = (datetime.datetime.now().year) - 1
            year = (datetime.datetime.now().year)

        year = str(year)

        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cursor = con.cursor()

        _dbname = 'data_' + dbname

        """
        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')
        """

        if account == "all":
            sql = "select pt.id, pt.name, pt.description, pt.number, " \
                  "sum(s.price) as sales, sum(s.margin) as margin " \
                  "from {0}.sales as s " \
                  "inner join {0}.products as p on s.product_id=p.id " \
                  "inner join {0}.product_type as pt on " \
                  "p.product_type_id=pt.id " \
                  "WHERE YEAR(s.date)='{1}' " \
                  "GROUP BY pt.{3};".format(_dbname, year, account, groupby)
        else:
            sql = "select pt.id, pt.name, pt.description, " \
                  "pt.number, sum(s.price) as sales, " \
                  "sum(s.margin) as margin from {0}.sales as s " \
                  "inner join {0}.products p on s.product_id=p.id " \
                  "inner join {0}.product_type as pt " \
                  "on p.product_type_id=pt.id " \
                  "inner join {0}.customers c on s.customer_id=c.id " \
                  "WHERE YEAR(s.date)='{1}' And c.id='{2}' " \
                  "GROUP BY pt.{3} ;".format(_dbname, year, account, groupby)

        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        data = np.asarray(cursor.fetchall())
        df = pd.DataFrame(data, columns=columns)
        return df.to_json(orient='records')

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        return json.dumps([])

    con.close()


def getCrossSellingItems(dbname, item='products', year=None,
                         groupby='id', account="all", local=False):
    """
    function: Query to get the cross selling
    """
    try:
        if year is None:
            year = (datetime.datetime.now().year) - 1
            year = (datetime.datetime.now().year)

        year = str(year)

        datadb = 'results_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cursor = con.cursor()

        _dbname = 'data_' + dbname

        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')

        if item == 'products':
            item = 'product_cross_selling'
        if item == 'product_type':
            item = 'product_type_cross_selling'

        if account != 'all':
            """
            if account != "":
                script = "\
                    SELECT id FROM {}.customers WHERE name = '{}'\
                    ".format('data_' + dbname, account)

            cursor.execute(script)
            con.commit()
            account_id = np.ravel(np.asarray(cursor.fetchall()))[0]
            """
            account_id = account

        if account == 'all':
            sql = "SELECT c.name, cr.{} FROM critters AS cr " \
                  "LEFT JOIN {}.customers AS c ON " \
                  "cr.name=c.id;".format(item, 'data_' + dbname)
        else:
            sql = "SELECT c.name, cr.{}  from critters AS cr " \
                  "LEFT JOIN {}.customers AS c ON cr.name=c.id " \
                  "WHERE cr.name='{}';".format(item, 'data_' + dbname,
                                               account_id)

        '''
        if account == "all":
            sql = "\
                SELECT name, {1} FROM critters\
            ".format(_dbname, item, year, account, groupby)
        else:
            sql = "\
                SELECT name, {1} FROM critters WHERE name='{3}'\
            ".format(_dbname, item, year, account, groupby)
        '''

        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        data = np.asarray(cursor.fetchall())
        df = pd.DataFrame(data, columns=columns)
        return df.to_json(orient='records')

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        return [{}]
    con.close()


def products_by_type(data, dbname, local=False):
    """
    function: Query to get the products by type
    """
    resp = dict()
    if 'product_type' not in data.keys():
        resp['product_type'] = 'product type is missing'
        return resp

    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()
        product_type = data.get('product_type')
        type_data = convert_list_tuple(str(product_type))

        response = list()
        item = dict()
        script = "SELECT `id`, `name` from `products` " \
                 "where  `product_type_id` IN {};".format(type_data)
        cur.execute(script)
        data = np.asarray(cur.fetchall())
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)
        df = df.to_dict(orient='records')
        con.commit()
        return df
    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )


def products_by_customer(data, dbname, local=False):
    """
    function: Query to get the products by customers
    """
    resp = dict()
    if 'customer_id' not in data.keys():
        resp['customer_id'] = 'customer id is missing'
        return resp

    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()
        customer_id = data.get('customer_id')

        script = "SELECT DISTINCT(products.name) as product_name, " \
                 "product_id From {db_}.sales as s " \
                 "LEFT JOIN {db_}.products  ON s.product_id = products.id " \
                 "LEFT JOIN {db_}.customers ON " \
                 "s.customer_id = customers.id where " \
                 "customers.id = " \
                 "{customer_id};".format(db_=datadb, customer_id=customer_id)

        cur.execute(script)
        data = np.asarray(cur.fetchall())
        if data.size == 0:
            return None
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)
        df = df.to_dict(orient='records')
        con.commit()
        return df
    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )


def getMinMaxVal(data, dbname, local=False):
    """
    function: get product min and max value
    """
    resp = dict()
    if 'customer_id' not in data.keys():
        resp['customer_id'] = 'customer id is missing'
        return resp

    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()
        customer_id = data.get('customer_id')

        query = "select MIN(price / quantity) as minval,  "\
                "MAX(price / quantity) as maxval from {db_}.sales "\
                "where 1=1 ".format(db_=datadb)
        if data.get('customer_id'):
            query += "AND customer_id = {customer_id} ".format(
                customer_id=data.get("customer_id")
            )
        if data.get('product_id') != 'selected_all_product':
            query += "AND product_id IN {product_id}".format(
                product_id=convert_list_tuple(str(data.get('product_id')))
            )

        cur.execute(query)
        data = np.asarray(cur.fetchall())
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)
        df = df.to_dict(orient='records')
        con.commit()
        return df
    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )


def getSuggestedRange(data, dbname, kam=None):
    """
    function: Query to get the suggestion range
    """
    resp = dict()
    if 'customer_id' not in data.keys():
        resp['customer_id'] = 'customer id is missing'
        return resp

    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        query = "select ROUND(MIN(price / quantity), 2) as minval,  "\
                "ROUND(MAX(price / quantity), 2) as maxval from {db_}.sales "\
                "where 1=1 AND year = {year} ".format(
                    db_=datadb,
                    year=str(datetime.datetime.now().year -1)
                    )
        if data.get('customer_id'):
            can_see_customer = True
            if kam is not None:
                customer_ids = [customer.id for k in kam for customer in k.customers]
                can_see_customer = data.get('customer_id') in customer_ids
            if can_see_customer:
                query += "AND customer_id = {customer_id} ".format(customer_id=data.get("customer_id"))

        if data.get('product_id') != 'selected_all_product':
            query += "AND product_id IN {product_id}".format(
                product_id=convert_list_tuple(str(data.get('product_id')))
            )

        cur.execute(query)

        data = np.asarray(cur.fetchall())
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(data, columns=columns)
        df = df.to_dict(orient='records')
        con.commit()
        return df
    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )


def convert_list_tuple(list_data):
    """
    function: convert list into tuple
    """
    return list_data.replace('[', '(').replace(']', ')')


if __name__ == "__main__":

    dbname = 'martin_masip'
    dbname = 'orbusneich_com'
    dbname = 'martin_masip'
    dbname = 'qymatix_best'

    if False:
        data = {'name': 'Product 1', 'description': 'This the first product'}
        data = {'name': 'Product 3', 'description': 'This the second product'}
        # insertProduct(data, dbname)
        # insertProduct(dbname=dbname, data=data)
        dropProduct(dbname=dbname, table='products', prod_id=16)

        prod_type = {'name': 'Product Type 2', 'description': 'This the second product type'}
        insertProductType(dbname=dbname, data=prod_type)
        dropProduct(dbname=dbname, table='product_type', prod_id=3)

        prod_line = {'name': 'Product Line 2', 'description': 'This the second product line'}
        insertProductLine(dbname=dbname, data=prod_line)
        dropProduct(dbname=dbname, table='product_line', prod_id=3)

        prod_class = {'name': 'Product Class 2', 'description': 'This the second product class'}
        insertProductClass(dbname=dbname, data=prod_class)
        dropProduct(dbname=dbname, table='product_class', prod_id=3)

    # products = getProducts(dbname)

    # products = getProductsList(dbname)
    # products = getProductsList(dbname, groupby='number')
    # products = getProductsList(dbname, groupby='product_type_id')
    # products = getProductsList(dbname, groupby='product_type')
    # account = u'Krankenhaus Hedwigsh\xf6he'
    year = None
    year = 2017
    account = 'all'
    dbname = 'qymatix_best'
    dbname = 'manhand___test_de'
    # products = getProductInsights(dbname, account=account, year=year)
    products = get_product_insights(dbname, account=account, year=year)

    # dbname = 'aet_at'
    # products = getProductTypeInsights(dbname, year=2017)

    account = 'all'
    account = 'Xeniades'
    # items = getCrossSellingItems(dbname, item='product_type',
    # account=account)
    # items = getCrossSellingItems(dbname, item='product_type',
    # account='Diakonie-Krankenhaus Wehrda')

    # items = getCrossSellingItems(dbname, item='products',
    # account='Klinikum Lippe Detmold')

    # items = getCrossSellingItems(dbname, item='product_type',
    # account='Klinikum Lippe Detmold')
