import os
from urllib.parse import unquote_plus

import MySQLdb as mysql
import numpy as np

from api.infrastructure.mysql import connection
import logging
import traceback
logger = logging.getLogger(__name__)

_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path, '../../..'))
_basepath = '/home'


def insertCustomer(data, dbname, local=False):
    # created = str(datetime.datetime.now())
    if 'name' not in data.keys():
        data = 'Name missing. Cannot insert unknown customer.'
        return data
    if 'postcode' not in data.keys():
        data['postcode'] = ''
    if data['postcode'] == '':
        data['postcode'] = data['postcode']

    if 'address' not in data.keys():
        data['address'] = ''
    if 'city' not in data.keys():
        data['city'] = ''
    if 'country' not in data.keys():
        data['country'] = ''
    if 'revenue' not in data.keys():
        data['revenue'] = 0
    if 'employees' not in data.keys():
        data['employees'] = 0
    if 'industry' not in data.keys():
        data['industry'] = ''
    if 'classification' not in data.keys():
        data['classification'] = ''
    if 'telephone' not in data.keys():
        data['telephone'] = ''
    if 'website' not in data.keys():
        data['website'] = ''
    if 'comment' not in data.keys():
        data['comment'] = ''
    if 'favorite' not in data.keys():
        data['favorite'] = 0
    if 'parent_customer_id' not in data.keys():
        data['parent_customer_id'] = 0
    if 'customer_number' not in data.keys():
        data['customer_number'] = 0

    for k in ('name', 'address', 'city', 'country', 'industry', 'classification', 'comment', 'telephone', 'website'):
        data[k] = unquote_plus(data[k])
        # ******** Fix Me **********
        # try:
        #     data[k] = data[k].strip().decode('utf-8').encode('cp1252')
        # except:
        #     data[k] = data[k].encode('cp1252')

    try:
        datadb = 'data_' + dbname

        mysql_connection = connection.MySQLConnection(datadb)

        con = mysql_connection.connect()

        cur = con.cursor()

        script = "INSERT INTO `customers` ("\
            "name, address, postcode, city, country, revenue, employees, industry, classification, "\
            "telephone, website, comment, favorite, customer_parent_id, customer_number) "\
            "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');\
            ".format(data['name'], data['address'], data['postcode'], data['city'], data['country'], \
                     data.get('revenue'), \
                     data.get('employees'), \
                     data.get('industry'), \
                     data.get('classification'), \
                     data.get('telephone'), \
                     data.get('website'), \
                     data.get('comment'), \
                     data.get('favorite'), \
                     data.get('parent_customer_id'),\
                     data.get('customer_number')
                     )
        
        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from customers;"
        cur.execute(script)
        customer_id = np.ravel(np.asarray(cur.fetchall()))[0]

        if data.get('kam_id'):
            script = "INSERT INTO {}.Users_Customers (user_id, customer_id) VALUES({},{});".format(
                "data_" + dbname, 
                int(data.get('kam_id')), 
                int(customer_id)
            )
            cur.execute(script)
            con.commit()

        return customer_id

    except mysql.Error as e:
        if int(e.args[0]) == 1062:
            script = "\
                SELECT id FROM customers WHERE name='{}';\
                ".format(data['name'])

            cur.execute(script)
            con.commit()

            customer_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return customer_id

        raise


def insert_customer(con, data, local=False):
    '''
    '''

    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    dbname = 'data_' + dbname
    cur.execute("USE {}".format(dbname))

    # created = str(datetime.datetime.now())
    if 'name' not in data.keys():
        data = 'Name missing. Cannot insert unknown customer.'
        return data
    if 'postcode' not in data.keys():
        data['postcode'] = ''
    if data['postcode'] == '':
        data['postcode'] = data['postcode']

    if 'address' not in data.keys():
        data['address'] = ''
    if 'city' not in data.keys():
        data['city'] = ''
    if 'country' not in data.keys():
        data['country'] = ''
    if 'revenue' not in data.keys():
        data['revenue'] = 0
    if 'employees' not in data.keys():
        data['employees'] = 0
    if 'industry' not in data.keys():
        data['industry'] = ''
    if 'classification' not in data.keys():
        data['classification'] = ''
    if 'website' not in data.keys():
        data['website'] = ''
    if 'comment' not in data.keys():
        data['comment'] = ''
    if 'favorite' not in data.keys():
        data['favorite'] = 0

    data['telephone'] = ''
    data['customer parent id'] = ''

            # for k in ('name', 'address', 'city', 'country', 'industry', 'classification', 'comment', 'website'):
    #     #data[k] = unquote_plus(data[k])
        # try:
        #     data[k] = data[k].strip().decode('utf-8').encode('cp1252')
        # except:
        #     data[k] = data[k].encode('cp1252')

    try:
        # (name, address, postcode, city, country, webpage, description, contact)\

        if 'id' not in data.keys():
            script = "\
                INSERT INTO `customers`\
                (name, address, postcode, city, country, revenue, employees, industry, classification, website, comment, favorite, telephone, customer_parent_id)\
                VALUES ('{}', '{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}');\
                ".format(data['name'], data['address'], data['postcode'], data['city'], data['country'], \
                         data['revenue'], \
                         data['employees'], \
                         data['industry'], \
                         data['classification'], \
                         data['website'], \
                         data['comment'], \
                         data['favorite'], \
                         data['telephone'], \
                         data['customer parent id'], \
                         )

        else:
            script = "\
                INSERT INTO `customers`\
                (id, name, address, postcode, city, country, revenue, employees, industry, classification, website, comment, favorite, telephone, customer_parent_id)\
                VALUES ({}, '{}', '{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}');\
                ".format(data['id'], data['name'], data['address'], data['postcode'], data['city'], data['country'], \
                         data['revenue'], \
                         data['employees'], \
                         data['industry'], \
                         data['classification'], \
                         data['website'], \
                         data['comment'], \
                         data['favorite'], \
                         data['telephone'], \
                         data['customer parent id'], \
                     )

        cur.execute(script)
        con.commit()

        if 'id' not in data.keys():
            script = "\
                SELECT MAX(id) from customers;\
                "
            cur.execute(script)
            customer_id = np.ravel(np.asarray(cur.fetchall()))[0]
            return customer_id
        else:
            return data['id']

    except Exception as e:
        print(e)

        if int(e.args[0]) == 1062:

            if 'id' in data.keys():
                return data['id']
            else:
                script = "\
                    SELECT id FROM customers WHERE name='{}';\
                    ".format(data['name'])

                cur.execute(script)

                customer_id = cur.fetchall()[0][0]

                return customer_id


def setCustomer(dbname, data):
    """
    """

    try:
        datadb = 'data_' + dbname

        mysql_connection = connection.MySQLConnection(datadb)

        con = mysql_connection.connect()

        cur = con.cursor()

        for k in ('name', 'address', 'address', 'city', 'country', 'industry', 'classification', 'comment', 'website'):
            try:
                data[k] = unquote_plus(data[k])
                # try:
                #     data[k] = data[k].strip().decode('utf-8').encode('cp1252')
                # except:
                #     data[k] = data[k].encode('cp1252')
            except:
                pass

        for col in data.keys():
            # customer_id = data['customer_id']
            customer_id = data['id']
            if col not in ('id', 'customer_id', 'kam_id'):
                value = data[col]
                try:
                    if isinstance(value, str):
                        script = "UPDATE {} SET `{}`='{}' WHERE id={};".format('customers', col, value, customer_id)
                    else:
                        script = "UPDATE {} SET `{}`={} WHERE id={};".format('customers', col, value, customer_id)
                    cur.execute(script)
                    con.commit()
                    if col == 'nameXX':
                        old_name = ""
                        if isinstance(value, str):
                            script = "UPDATE {} SET `{}`='{}' WHERE name={};".format("results_" + dbname + '.critters',
                                                                                  col, value, old_name)
                        else:
                            script = "UPDATE {} SET `{}`={} WHERE name={};".format("results_" + dbname + '.critters', col,
                                                                                value, old_name)
                        cur.execute(script)
                        con.commit()
                except Exception as e:
                    print(e)
            if col == 'kam_id':
                kam_id = data[col]
                script = "DELETE FROM {}.Users_Customers WHERE customer_id={};".format(
                    "data_" + dbname, 
                    int(customer_id)
                )
                cur.execute(script)
                con.commit()
                script = "INSERT INTO {}.Users_Customers (user_id, customer_id) VALUES({},{});".format(
                    "data_" + dbname, 
                    int(kam_id), 
                    int(customer_id)
                )
                cur.execute(script)
                con.commit()

    # except mysql.Error as e:
    # print("Error {}: {}".format(e.args[0], e.args[1]))
    except Exception as e:
        print(e)
        # sys.exit(1)
        # raise

    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. Contact your administrator."

        return customer_id


def deleteCustomer(dbname, customer_id):
    try:
        datadb = 'data_' + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        try:
            script = "DELETE FROM {}.Users_Customers WHERE "\
                    "customer_id={};".format(
                        "data_" + dbname, 
                        int(customer_id)
                    )
            cur.execute(script)
            con.commit()

            script = "DELETE FROM {}.customers WHERE id={};".format(
                    "data_" + dbname, 
                int(customer_id)
            )
            cur.execute(script)
            con.commit()
            return {
                "status_code": 200,
                "message": "Account Deleted Successfully"
            }
        except mysql.Error as e:
            logger.error(
                "message {}, error {}".format(
                    e, traceback.format_exc()
                ),
                extra={'type': 'Login'}
            )
            return {
                "status_code": 500
            }

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))


if __name__ == "__main__":
    dbname = 'qymatix_de'
    dbname = 'qymatix_best'
    data = {"id": 1, "comment": "Desa"}
    data = {"name": "HHH"}
    # setCustomer(dbname, data)
    data = {"name": "Tester 2", "comment": "", "postcode": "", "address": "%25C3%259F", "city": "", "country": ""}
    # data = {"name":"Tester 4","comment":"","postcode":"","address":"\xdf","city":"","country":""}
    # data = {"name":"Tester 4","comment":"","postcode":"","address":"%C3%9F","city":"","country":""}
    insertCustomer(data, dbname)
    print("...")
