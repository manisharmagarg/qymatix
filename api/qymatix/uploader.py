import datetime
import os
import sys
from urllib.parse import unquote_plus

import MySQLdb as mysql
from . import customers
from . import kam
import numpy as np
import pandas as pd
from . import products
from . import sales
from .analytics.plans_analytics import plans_analytics

from api.infrastructure.mysql import connection


def connect_db(dbname):
    '''
    '''

    datadb = 'data_' + dbname
    mysql_connection = connection.MySQLConnection(datadb)
    con = mysql_connection.connect()
    cur = con.cursor()

    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    print("Connected to: " + dbname)
    return con


def link_user_customer(con, user_id, customer_id):
    '''
    '''
    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    dbname = 'data_' + dbname
    cur.execute("USE {}".format(dbname))

    try:
        script = "\
            INSERT INTO Users_Customers (user_id, customer_id) VALUES({},{});\
            ".format(int(user_id), int(customer_id))

        cur = con.cursor()
        cur.execute(script)
        con.commit()
        data = "{}"

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        data = {}
        data = 'Error'

    return data


def load_data(filename, skiprows=None, nrows=None):
    '''
    '''
    if os.path.splitext(filename)[1] in ['.xlsx', '.xls']:
        data = pd.read_excel(filename, skiprows=skiprows, nrows=nrows)
    if os.path.splitext(filename)[1] in ['.csv']:
        data = pd.read_csv(filename, delimiter=';')

    return data


# def insertKamFromFile(dbname, filename=None, name="default", local=False, lines=None):
def insert_kam(con, data, name="default", local=False, lines=None):
    labels = data.keys()

    if 'name' not in labels:
        return -1

    created = str(datetime.datetime.now())

    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    dbname = 'data_' + dbname
    cur.execute("USE {}".format(dbname))
    fields = ('username', 'name', 'description', 'created', 'country', 'phone', 'email', 'active')
    for f in fields:
        if f not in labels:
            data[f] = ''

        # for k in data.keys():
        # if f in ('name', 'description', 'country', 'email'):
        #     value = data[f]
        #     try:
        #         value = value.decode('utf-8').encode('cp1252')
        #     except:
        #         value = value.encode('cp1252')
        #
        #     data[f] = value

    try:
        script = "\
            INSERT INTO `users`\
            (username, name, description, created, country, phone, email, active)\
            VALUES ('', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', 0);\
            ".format(data['username'], data['name'], data['description'], created, data['country'], \
                     data['phone'], data['email'])
        cur.execute(script)
        con.commit()

        script = "\
            SELECT MAX(id) from users;\
            "
        cur.execute(script)
        # con.commit()
        user_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return user_id

    # except Exception as e:
    # print(e)
    # pass
    # raise
    except mysql.Error as e:
        # print(e)
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        if int(e.args[0]) == 1062:
            script = "\
                SELECT id FROM users WHERE name='{}';\
                ".format(data['name'])

            cur.execute(script)
            con.commit()

            user_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return user_id


def update_products(dbname, data, name="default", local=False, lines=None):
    labels = data.keys()

    # if 'name' not in labels:
    # return -1

    created = str(datetime.datetime.now())

    con = connect_db(dbname)
    cur = con.cursor()
    # cur.execute("select database()")
    # dbname = cur.fetchone()[0]
    # dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    # dbname = 'data_' + dbname
    # cur.execute("USE {}".format(dbname))

    for i in data.index:
        _data = data[['new_name', 'old_name']].loc[i].to_dict()

        fields = ('username', 'name', 'description', 'created', 'country', 'phone', 'email', 'active')
        for f in fields:
            if f not in labels:
                _data[f] = ''

            if f in ('new_name', 'old_name', 'name', 'description', 'country', 'email'):
                value = _data[f]
                try:
                    value = value.decode('utf-8').encode('cp1252')
                except:
                    value = value.encode('cp1252')

                _data[f] = value

            print(_data)
            try:
                script = "\
                    UPDATE products\
                    SET name='{1}' WHERE name='{0}';\
                    ".format(_data['old_name'], _data['new_name'])
                cur.execute(script)
                con.commit()
                print("Replaced product name {} with {}".format(_data['old_name'], _data['new_name']))
                # user_id = np.ravel(np.asarray(cur.fetchall()))[0]

            # except mysql.Error as e:
            except Exception as e:
                print(e)
                # raise
                pass

    return


def update_products_in_sales(dbname, data, name="default", local=False, lines=None):
    labels = data.keys()

    con = connect_db(dbname)
    cur = con.cursor()
    # cur.execute("select database()")
    # dbname = cur.fetchone()[0]
    # dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    # dbname = 'data_' + dbname
    # cur.execute("USE {}".format(dbname))

    for i in data.index:
        _data = data[['new_name', 'old_name']].loc[i].to_dict()

        # fields = ('username', 'name', 'description', 'created', 'country', 'phone', 'email', 'active')
        # for f in fields:
        # if f not in labels:
        # _data[f] = ''

        for f in _data.keys():
            if f in ('new_name', 'old_name', 'name', 'description', 'country', 'email'):
                value = _data[f]
                try:
                    value = value.decode('utf-8').encode('cp1252')
                except:
                    value = value.encode('cp1252')

                _data[f] = value

            # print(_data)
            try:
                script = "\
                    SELECT id FROM products\
                    WHERE name='{0}';\
                    ".format(_data['old_name'])

                cur.execute(script)
                # con.commit()
                try:
                    old_id = cur.fetchall()[0][0]
                except:
                    old_id = -1
                    raise

                new_id = -1
                if old_id != -1:
                    script = "\
                        SELECT id FROM products\
                        WHERE name='{0}';\
                        ".format(_data['new_name'])
                    cur.execute(script)
                    # con.commit()
                    try:
                        new_id = cur.fetchall()[0][0]
                    except:
                        pass

                if new_id != -1:
                    script = "\
                        UPDATE sales\
                        SET product_id={1} WHERE product_id={0};\
                        ".format(old_id, new_id)
                    cur.execute(script)
                    con.commit()
                    print("Replaced product {} with {}".format(_data['old_name'], _data['new_name']))

            # except mysql.Error as e:
            except Exception as e:
                # print(e)
                # raise
                pass

    return


def upload_plans(dbname, data, name="default", local=False, lines=None):
    labels = data.keys()

    con = connect_db(dbname)
    cur = con.cursor()
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '').replace('results_', '')
    dbname = 'data_' + dbname
    cur.execute("USE {}".format(dbname))

    # grouped = data.groupby(['invoice','customer_id', 'product', 'product type'], as_index=False)['goal'].sum()
    # print(grouped[grouped['goal']>=11000])
    # print(grouped.columns)
    # print(data.columns)
    grouped = data.groupby('invoice')
    invoices = {}
    for name, group in grouped:
        # group = group.rename(columns={'due':'due', 'action':'type', 'description':'comment', 'plan':'plan_id'})
        # group[['due', 'id', 'created', 'action', 'title', 'description' ]]
        # invoices[name] = group.to_json(orient='records')
        # invoices[name] = group
        # print(invoices)
        group = group[~group['product type'].isnull()]
        group = group[['invoice', 'name', 'customer_id', 'goal', 'product type', 'Date', 'kam']]

        if group['goal'].sum() > 11000:

            plan = {}
            fields = (
            'name', 'customer_id', 'description', 'created', 'due', 'owner_id', 'goal', 'chances', 'status', 'action',
            'visits', 'calls', 'offers', 'hot', 'group_id')

            plan['name'] = group['invoice'].values[0] + " - " + group['name'].values[0]
            plan['customer_id'] = group['customer_id'].values[0]
            plan['goal'] = round(group['goal'].sum(), 2)
            plan['created'] = group['Date'].values[0]
            plan['description'] = ' - '.join(group['product type'])
            plan['due'] = '2018-12-31 00:00:00'
            plan['status'] = 'Customer Evaluation'
            plan['chances'] = 2
            plan['action'] = 'go'
            plan['hot'] = 0
            plan['visits'] = 0
            plan['calls'] = 0
            plan['offers'] = 0
            plan['group_id'] = 1

            for f in plan.keys():

                if f in ('name', 'description'):
                    value = plan[f]
                    try:
                        value = value.decode('utf-8').encode('cp1252')
                    except:
                        value = value.encode('cp1252')

                    plan[f] = value

            try:
                script = "\
                    SELECT id FROM users\
                    WHERE name='{0}';\
                    ".format(group['kam'].values[0])
                cur.execute(script)
                con.commit()
                plan['owner_id'] = int(cur.fetchall()[0][0])
            except:
                plan['owner_id'] = 0

            script = "\
                INSERT INTO `plans`\
                (name, description, owner_id, group_id, created, due, account, goal, chances, status, action, calls, visits, offers, hot)\
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');\
                ".format(plan['name'], plan['description'], plan['owner_id'], plan['group_id'], plan['created'],
                         plan['due'], plan['customer_id'], plan['goal'], plan['chances'], plan['status'],
                         plan['action'], plan['calls'], plan['visits'], plan['offers'], plan['hot'])
            cur.execute(script)
            con.commit()

            script = "\
                SELECT MAX(id) from plans;\
                "
            # cur.execute(script)
            # con.commit()
            # plan_id = int(cur.fetchall()[0][0])
            # print(plan_id)

    plans_analytics.analyzePlans(dbname.split("data_")[1], cur)

    return


# def upload_data(dbname, username, filename):
def upload_data(dbname, filename):
    '''
    '''
    name, ext = os.path.splitext(filename)
    name = os.path.split(name)[-1] + "_" + ext[1:]
    name = name.replace("-", "_")
    name = name.replace(".", "_")

    # if os.path.splitext(filename)[1] == '.csv':
    # csv2mysql(data=filename, dbname=dbname)
    if os.path.splitext(filename)[1] in ['.xlsx', '.xls', '.csv']:
        try:
            print("Uploading data...")
            upload_customers(data=filename, dbname=dbname)
        except Exception as e:
            print("Not posible to upload data. Check your file.")
            print(e)
            # return None
            raise

        # dbname = "data_" + username + "_{}".format(name)
        # dbname = "data_" + dbname
        # config.createUsersCustomersTable(dbname)

        try:
            kam.insertKamFromFile(dbname, filename=filename)
        except:
            print("Not posible to insert KAM.")
            # return None
            raise


def upload_customers(dbname, data, from_line=None, to_line=None, local=False, id_list=None):
    '''
    '''
    con = connect_db(dbname)

    for c in data.columns:
        if c in ('Date', 'date', 'Invoice Date'):
            data.rename(columns={c: 'Date'}, inplace=True)

    if 'Date' in data.keys():
        data['Date'] = pd.to_datetime(data['Date'], dayfirst=False, yearfirst=False)

    data.drop_duplicates(inplace=True)

    if from_line == None:
        from_line = 0
    if to_line == None:
        to_line = len(data.index)

    if id_list != None:
        data = data[data['Account id'].isin(id_list)]

    for i in data.index.tolist()[from_line:to_line]:
        sys.stdout.write("{} form {}\r".format(i, max(data.index.tolist())))
        sys.stdout.flush()

        cust_address = ""
        cust_postcode = ""
        cust_city = ""
        cust_country = ""
        sales_kam = ""
        cust_revenue = -1
        cust_employees = -1
        cust_industry = ""
        cust_classification = ""
        cust_website = ""
        cust_comment = ""
        cust_favorite = 0

        for name in data.columns:
            if name.lower() in ('accountid', 'account id', 'id', 'client id', 'customer id', 'customerid'):
                cust_id = data.ix[i][name]
            if name.lower() in ('kunde', 'clients', 'customer', 'client', 'customer name', 'account', 'account name'):
                cust_name = data.ix[i][name]
            if name.lower() in (u'address', u'adresse'):
                cust_address = data.ix[i][name]
            if name.lower() in (u'plz', u'post', u'postcode', u'zipcod', u'zip', u'zipcode'):
                cust_postcode = data.ix[i][name]
            if name.lower() in ('city', 'stadt'):
                cust_city = data.ix[i][name]
            if name.lower() in (u'country', u'land'):
                cust_country = data.ix[i][name]
            if name.lower() in (u'revenue'):
                cust_revenue = data.ix[i][name]
            if name.lower() in (u'employees'):
                cust_employees = data.ix[i][name]
            if name.lower() in (u'industry'):
                cust_industry = data.ix[i][name]
            if name.lower() in (u'classification'):
                cust_classification = data.ix[i][name]
            if name.lower() in (u'website', u'webpage', u'site'):
                cust_website = data.ix[i][name]
            if name.lower() in (u'comment', u'comment'):
                cust_comment = data.ix[i][name]
            if name.lower() in (u'favorite', u'favorite'):
                try:
                    cust_favorite = int(data.ix[i][name])
                except:
                    cust_favorite = 0

            if name.lower() in ('kam', 'account manager', 'accountmanager', 'vertreter'):
                sales_kam = data.ix[i][name]

            if type(cust_city) == float:
                cust_city = ''

        try:
            _data = {
                'name': cust_name, \
                'address': cust_address, \
                'postcode': cust_postcode, \
                'city': cust_city, \
                'country': cust_country, \
                'revenue': cust_revenue, \
                'employees': cust_employees, \
                'industry': cust_industry, \
                'classification': cust_classification, \
                'website': cust_website, \
                'comment': cust_comment, \
                'favorite': cust_favorite
            }
            # print(_data)

            try:
                _data['id'] = cust_id
            except:
                pass

            customer_id = customers.insert_customer(con, data=_data)

            # if sales_kam:
            # try:
            # user_id = insert_kam(con, data={'name':sales_kam})
            # except:
            # raise
            # link_user_customer(con, user_id, customer_id)

        except Exception as e:
            # print(_data)
            print(e)
            raise
            # pass


def upload_kam(dbname, data, from_line=None, to_line=None, local=False, id_list=None):
    '''
    '''
    con = connect_db(dbname)

    for c in data.columns:
        if c in ('Date', 'date', 'Invoice Date'):
            data.rename(columns={c: 'Date'}, inplace=True)

    if 'Date' in data.keys():
        data['Date'] = pd.to_datetime(data['Date'], dayfirst=False, yearfirst=False)

    data.drop_duplicates(inplace=True)

    if from_line == None:
        from_line = 0
    if to_line == None:
        to_line = len(data.index)

    if id_list != None:
        data = data[data['Account id'].isin(id_list)]

    for i in data.index.tolist()[from_line:to_line]:
        sys.stdout.write("{} form {}\r".format(i, max(data.index.tolist())))
        sys.stdout.flush()

        sales_kam = ""

        for name in data.columns:
            if name.lower() in ('accountid', 'account id', 'id', 'client id', 'customer id', 'customerid'):
                cust_id = data.ix[i][name]
            # if name.lower() in ('kunde', 'clients', 'customer', 'client', 'customer name', 'account', 'account name'):
            # cust_name = data.ix[i][name]
            if name.lower() in ('kam', 'account manager', 'accountmanager', 'vertreter'):
                sales_kam = data.ix[i][name]

        try:
            try:
                script = "\
                    SELECT id from data_{}.customers WHERE id={}\
                    ".format(dbname, cust_id)
                cur = con.cursor()
                cur.execute(script)
                # con.commit()
                print(script)
                customer_id = np.ravel(np.asarray(cur.fetchall()))[0]
            except:
                print(cust_id)
                print("No customer id found")
                raise

            if sales_kam:
                try:
                    user_id = insert_kam(con, data={'name': sales_kam})
                except:
                    print("Could not insert KAM")
                    raise
                link_user_customer(con, user_id, customer_id)
                print(">>>")

        except Exception as e:
            print(e)
            # raise
            # pass


def upload_product_class(dbname, data, from_line=None, to_line=None, local=False):
    '''
    '''
    con = connect_db(dbname)

    for c in data.columns:
        if c in ('Date', 'date', 'Invoice Date'):
            data.rename(columns={c: 'Date'}, inplace=True)
        if 'berwarengruppe' in c:
            data.rename(columns={c: 'product line'}, inplace=True)

    if 'Date' in data.keys():
        data['Date'] = pd.to_datetime(data['Date'], dayfirst=False, yearfirst=False)

    data.drop_duplicates(inplace=True)

    if from_line == None:
        from_line = 0
    if to_line == None:
        to_line = len(data.index)

    for i in data.index.tolist()[from_line:to_line]:
        sys.stdout.write("{} form {}\r".format(i, max(data.index.tolist())))
        sys.stdout.flush()

        fields = ('name', 'description', 'active', 'number', 'class')
        prod_line = dict()

        for name in data.columns:
            if name.lower() in (u'product line', u'productline', u'\xc3berwarengruppe'):
                # prod_line['name'] = str(data.ix[i][name])
                if type(data.ix[i][name]) == bytes:
                    prod_line['name'] = str(data.ix[i][name], 'utf-8')
                else:
                    prod_line['name'] = str(data.ix[i][name])

                # print(type(data.ix[i][name]))
                # print(type(prod_line['name']))
                # print(prod_line['name'])
                # print("....")

            if name.lower() in (u'description'):
                prod_line['description'] = data.ix[i][name]
            if name.lower() in (u'serial'):
                prod_line['serial'] = str(data.ix[i][name])
            if name.lower() in (u'number'):
                prod_line['number'] = str(data.ix[i][name])
            if name.lower() in (u'active'):
                prod_line['active'] = int(data.ix[i][name])
            if name.lower() in (u'line'):
                prod_line['line'] = int(data.ix[i][name])

        for f in fields:
            if f not in prod_line.keys():
                prod_line[f] = ""
                if f == 'active':
                    prod_line[f] = 0

        try:

            try:
                product_line_id = products.insert_product_class(con, data=prod_line)
            except Exception as e:
                print(e)
                print("Failed: " + str(prod_line).encode('ascii', 'ignore').decode('ascii'))
                print(type(prod_line['name']))


        except Exception as e:
            print(e)
            # raise
            # pass

    # return product_line_id
    return


def upload_product_line(dbname, data, from_line=None, to_line=None, local=False):
    '''
    '''
    con = connect_db(dbname)

    for c in data.columns:
        if c in ('Date', 'date', 'Invoice Date'):
            data.rename(columns={c: 'Date'}, inplace=True)
        if 'berwarengruppe' in c:
            data.rename(columns={c: 'product line'}, inplace=True)

    if 'Date' in data.keys():
        data['Date'] = pd.to_datetime(data['Date'], dayfirst=False, yearfirst=False)

    data.drop_duplicates(inplace=True)

    if from_line == None:
        from_line = 0
    if to_line == None:
        to_line = len(data.index)

    for i in data.index.tolist()[from_line:to_line]:
        sys.stdout.write("{} form {}\r".format(i, max(data.index.tolist())))
        sys.stdout.flush()

        fields = ('name', 'description', 'active', 'number', 'class')
        prod_line = dict()

        for name in data.columns:
            if name.lower() in (u'product line', u'productline', u'\xc3berwarengruppe'):
                if type(data.ix[i][name]) == bytes:
                    prod_line['name'] = str(data.ix[i][name], 'utf-8')
                else:
                    prod_line['name'] = data.ix[i][name]

            if name.lower() in (u'description'):
                prod_line['description'] = data.ix[i][name]
            if name.lower() in (u'serial'):
                prod_line['serial'] = str(data.ix[i][name])
            if name.lower() in (u'number'):
                prod_line['number'] = str(data.ix[i][name])
            if name.lower() in (u'active'):
                prod_line['active'] = int(data.ix[i][name])
            if name.lower() in (u'line'):
                prod_line['line'] = int(data.ix[i][name])

        for f in fields:
            if f not in prod_line.keys():
                prod_line[f] = ""
                if f == 'active':
                    prod_line[f] = 0

        try:
            product_line_id = products.insert_product_line(con, data=prod_line)
        # except:
        except Exception as e:
            # print("Failed: " + str(prod_line).encode('ascii', 'ignore').decode('ascii'))
            print(e)
            # raise
            # pass

    # return product_line_id
    return


def upload_product_type(dbname, data, from_line=None, to_line=None, local=False):
    '''
    '''
    con = connect_db(dbname)

    for c in data.columns:
        if c in ('Date', 'date', 'Invoice Date'):
            data.rename(columns={c: 'Date'}, inplace=True)
        if 'berwarengruppe' in c:
            data.rename(columns={c: 'product line'}, inplace=True)

    if 'Date' in data.keys():
        data['Date'] = pd.to_datetime(data['Date'], dayfirst=False, yearfirst=False)

    data.drop_duplicates(inplace=True)

    if from_line == None:
        from_line = 0
    if to_line == None:
        to_line = len(data.index)

    for i in data.index.tolist()[from_line:to_line]:
        sys.stdout.write("{} form {}\r".format(i, max(data.index.tolist())))
        sys.stdout.flush()

        fields = ('name', 'description', 'active', 'number', 'class')
        prod_type = dict()

        for name in data.columns:
            if name.lower() in (u'product type', u'producttype', u'warengruppe'):
                if type(data.ix[i][name]) == bytes:
                    prod_type['name'] = str(data.ix[i][name], 'utf-8')
                else:
                    prod_type['name'] = data.ix[i][name]

            if name.lower() in (u'product line', u'productline', u'warengruppe'):
                try:
                    prod_type['product_line_id'] = products.get_product_line_id(con, data.ix[i][name])
                except:
                    prod_type['product_line_id'] = 1

            if name.lower() in (u'description'):
                prod_type['description'] = data.ix[i][name]
            if name.lower() in (u'serial'):
                prod_type['serial'] = str(data.ix[i][name])
            if name.lower() in (u'number'):
                prod_type['number'] = str(data.ix[i][name])
            if name.lower() in (u'active'):
                prod_type['active'] = int(data.ix[i][name])
            if name.lower() in (u'line'):
                prod_type['line'] = int(data.ix[i][name])

        for f in fields:
            if f not in prod_type.keys():
                prod_type[f] = ""
                if f == 'active':
                    prod_type[f] = 0

        # print(prod_type)
        try:

            try:
                product_type_id = products.insert_product_type(con, data=prod_type)
            except Exception as e:
                # print("Failed: " + str(prod_type))
                print(e)

        except Exception as e:
            print(e)
            # raise
            # pass


def upload_products(dbname, data, from_line=None, to_line=None, local=False):
    '''
    '''
    con = connect_db(dbname)

    for c in data.columns:
        if c in ('Date', 'date', 'Invoice Date'):
            data.rename(columns={c: 'Date'}, inplace=True)
        if 'berwarengruppe' in c:
            data.rename(columns={c: 'product line'}, inplace=True)

    if 'Date' in data.keys():
        data['Date'] = pd.to_datetime(data['Date'], dayfirst=False, yearfirst=False)

    data.drop_duplicates(inplace=True)

    if from_line == None:
        from_line = 0
    if to_line == None:
        to_line = len(data.index)

    j = 0
    LEN = len(data.index.tolist()[from_line:to_line])
    for i in data.index.tolist()[from_line:to_line]:
        # sys.stdout.write("{} form {}\r".format(i, max(data.index.tolist())))
        j = j + 1
        sys.stdout.write("{} form {}\r".format(j, LEN))
        sys.stdout.flush()

        fields = ('name', 'description', 'active', 'number', 'class')
        prod = dict()

        for name in data.columns:
            if name.lower() in (u'product', u'artikel', u'artikelnummer'):
                if type(data.ix[i][name]) == bytes:
                    prod['name'] = str(data.ix[i][name], 'utf-8')
                else:
                    prod['name'] = data.ix[i][name]
            if name.lower() in (u'product type', u'producttype', u'warengruppe', 'wg'):
                if type(data.ix[i][name]) == bytes:
                    prodtype = str(data.ix[i][name], 'utf-8')
                else:
                    prodtype = data.ix[i][name]
                prod['product_type_id'] = products.get_product_type_id(con, prodtype)
                if prod['product_type_id'] in ('', 'nan'):
                    prod['product_type_id'] = 1
            if name.lower() in (u'description', 'artikeltext', 'artikel text'):
                prod['description'] = data.ix[i][name]
                if type(prod['description']) == float:
                    prod['description'] = ""
            if name.lower() in (u'serial'):
                prod['serial'] = str(data.ix[i][name])
            if name.lower() in (u'number'):
                prod['number'] = str(data.ix[i][name])
            if name.lower() in (u'active'):
                prod['active'] = int(data.ix[i][name])
            if name.lower() in (u'line'):
                prod['line'] = int(data.ix[i][name])

        for f in fields:
            if f not in prod.keys():
                prod[f] = ""
                if f == 'active':
                    prod[f] = 0

        try:

            try:
                product = products.insert_product(con, data=prod)
            except Exception as e:
                # print("Failed: " + str(prod))
                # raise
                print(e)

        except Exception as e:
            print(e)
            # raise
            # pass


def upload_records(dbname, data, from_line=None, to_line=None, local=False):
    '''
    '''
    con = connect_db(dbname)

    for c in data.columns:
        if c in ('Date', 'date', 'Invoice Date'):
            data.rename(columns={c: 'Date'}, inplace=True)

    # if 'Date' in data.keys():
    # data['Date'] = pd.to_datetime(data['Date'], dayfirst=False, yearfirst=False)
    # data['Date'] = pd.to_datetime(data['Date'], dayfirst=True, yearfirst=False)
    # data['Date'] = pd.to_datetime(data['Date'])

    data.drop_duplicates(inplace=True)
    if from_line == None:
        from_line = 0
    if to_line == None:
        to_line = len(data.index)

    _columns = [ \
        'customer_id', \
        'product_id', \
        'quantity', \
        'price', \
        'cost', \
        'margin', \
        'year', \
        'month', \
        'date', \
        'invoice']

    data_not_uploaded = pd.DataFrame(columns=_columns)
    for i in data.index.tolist()[from_line:to_line]:
        sys.stdout.write("{} form {}\r".format(i, max(data.index.tolist())))
        sys.stdout.flush()
        # print(i)

        sales_date = ""
        sales_kam = ""

        sales_data = {}

        for name in data.columns:
            if name.lower() in (
            'accountid', 'account id', 'id', 'client id', 'customer_id', 'customer id', 'customerid',
            'customer address#'):
                cust_id = data.ix[i][name]
            if name.lower() in (
            'kunde', 'clients', 'customer', 'client', 'customer name', 'account', 'customer_name', 'account_name'):
                cust_name = data.ix[i][name]

            if name.lower() in (u'product id', u'material id', u'article id', u'artikel id', 'item id'):
                prod_id = str(data.ix[i][name])
            if name.lower() in (u'product', u'material', u'article', u'artikel', 'item', 'article#'):
                try:
                    prod_name = str(data.ix[i][name])
                except:
                    prod_name = data.ix[i][name]

            # if name.lower() in (u'product group', u'item group', u'article group', 'product type', 'type', 'warengruppe'):
            # prod_type = str(data.ix[i][name])
            if name.lower() in ('price', 'pay', 'preis', 'price', 'sum price'):
                sales_data['prod_price'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name.lower() in ('margin', 'margin', 'marge', 'sum margin'):
                sales_data['prod_margin'] = float(str(data.ix[i][name]).replace(",", "."))
            if name.lower() in ('cost', 'costs', 'fabrication cost', 'sum costs'):
                sales_data['prod_cost'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name.lower() in ('unit cost'):
                sales_data['prod_unit_cost'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name.lower() in ('unit price'):
                sales_data['prod_unit_price'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name.lower() in ('unit margin'):
                sales_data['prod_unit_margin'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name.lower() in ('quantity', 'qty', 'amount'):
                try:
                    sales_data['prod_quantity'] = int(str(data.ix[i][name]).replace(',', '.'))
                except:
                    sales_data['prod_quantity'] = 1
            if name.lower() in ('year', 'yy', 'jahr'):
                sales_year = data.ix[i][name]
            if name.lower() in ('month', 'mm', 'monat'):
                sales_month = data.ix[i][name]
            if name.lower() in ('date', 'date', 'invoice date'):
                sales_date = data.ix[i][name]
            if name.lower() in ('invoice', 'invoice no.', 'transaction id'):
                sales_invoice = data.ix[i][name]
            if name.lower() in ('kam', 'account manager', 'accountmanager'):
                sales_kam = data.ix[i][name]

        if 'prod_quantity' in sales_data.keys() and sales_data['prod_quantity'] == 0:
            sales_data['prod_quantity'] = 1

        if 'prod_quantity' not in sales_data.keys():
            sales_data['prod_quantity'] = 1

        if 'prod_unit_price' in sales_data.keys() and 'prod_price' not in sales_data.keys():
            sales_data['prod_price'] = sales_data['prod_unit_price'] * sales_data['prod_quantity']

        if 'prod_unit_price' not in sales_data.keys() and 'prod_price' in sales_data.keys():
            sales_data['prod_unit_price'] = sales_data['prod_price'] / sales_data['prod_quantity']

        if 'prod_unit_cost' in sales_data.keys() and 'prod_cost' not in sales_data.keys():
            sales_data['prod_cost'] = sales_data['prod_unit_cost'] * sales_data['prod_quantity']

        if 'prod_unit_cost' not in sales_data.keys() and 'prod_cost' in sales_data.keys():
            sales_data['prod_unit_cost'] = sales_data['prod_cost'] / sales_data['prod_quantity']

        if 'prod_unit_margin' not in sales_data.keys() and 'prod_unit_cost' in sales_data.keys():
            sales_data['prod_unit_margin'] = sales_data['prod_unit_price'] - sales_data['prod_unit_cost']
        if 'prod_unit_margin' in sales_data.keys() and 'prod_cost' not in sales_data.keys():
            sales_data['prod_unit_cost'] = sales_data['prod_unit_price'] - sales_data['prod_unit_margin']

        if 'prod_margin' not in sales_data.keys() and 'prod_cost' in sales_data.keys():
            sales_data['prod_margin'] = sales_data['prod_price'] - sales_data['prod_cost']
        if 'prod_margin' in sales_data.keys() and 'prod_cost' not in sales_data.keys():
            sales_data['prod_cost'] = sales_data['prod_price'] - sales_data['prod_margin']

        try:
            sales_invoice
        except:
            sales_invoice = 'NULL'

        try:
            prod_type
        except:
            prod_type = ""

        sales_data['prod_name'] = prod_name
        k = 'prod_name'
        try:
            sales_data[k] = sales_data[k].strip().decode('utf-8').encode('cp1252')
        except:
            sales_data[k] = sales_data[k].encode('cp1252')

        try:
            script = "\
                SELECT id from products WHERE name='{}'\
                ".format(prod_name)
            cur = con.cursor()
            cur.execute(script)
            # con.commit()
            prod_id = np.ravel(np.asarray(cur.fetchall()))[0]
        except:
            print(prod_name)
            print("Sales record without  product name/id.")
            # raise

        # print(prod_id)
        try:
            _data = { \
                'customer_id': cust_id, \
                'product_id': prod_id, \
                'quantity': sales_data['prod_quantity'], \
                'price': sales_data['prod_price'], \
                'cost': sales_data['prod_cost'], \
                'margin': sales_data['prod_margin'], \
                'year': sales_date.year, \
                'month': sales_date.month, \
                'date': sales_date.isoformat().replace("T", " "), \
                'invoice': sales_invoice, \
                # 'kam':sales_kam,\
            }

            print(_data)
            # sales.insert_sales_record(con, _data)

        except Exception as e:
            print(e)
            pd_data = pd.DataFrame([_data])
            data_not_uploaded = data_not_uploaded.append(pd_data)
            # raise

        print(data_not_uploaded)
        # data_not_uploaded.to_excel('/home/webuser/users/aet_at/data/AET_Sales_2017_not_uploaded.xlsx')


def upload_sales(dbname, data, from_line=None, to_line=None, local=False, id_list=None, col_account_id='customer_id'):
    '''
    '''
    con = connect_db(dbname)

    for c in data.columns:
        if c in ('Date', 'date', 'Invoice Date'):
            data.rename(columns={c: 'Date'}, inplace=True)

    if 'Date' in data.keys():
        # data['Date'] = pd.to_datetime(data['Date'], dayfirst=False, yearfirst=False)
        # data['Date'] = pd.to_datetime(data['Date'], dayfirst=True, yearfirst=False)
        data['Date'] = pd.to_datetime(data['Date'])

    # data['year'] = data['Date'].map(lambda x: x.year)
    # data.drop_duplicates(inplace=True)

    if id_list != None:
        data = data[data[col_account_id].isin(id_list)]

    if from_line == None:
        from_line = 0
    if to_line == None:
        to_line = len(data.index)

    _columns = [ \
        'customer_id', \
        'product_id', \
        'quantity', \
        'price', \
        'cost', \
        'margin', \
        'year', \
        'month', \
        'date', \
        'invoice']

    data_not_uploaded = pd.DataFrame(columns=_columns)

    j = 0
    LEN = len(data.index.tolist()[from_line:to_line])
    for i in data.index.tolist()[from_line:to_line]:
        # sys.stdout.write("{} form {}\r".format(i, max(data.index.tolist())))
        sys.stdout.write("{} form {}\r".format(j, LEN))
        sys.stdout.flush()
        j = j + 1
        # print(i)

        sales_date = ""
        sales_kam = ""

        sales_data = {}

        for name in data.columns:
            if name.lower() in (
            'accountid', 'account id', 'id', 'client id', 'customer_id', 'customer id', 'customerid',
            'customer address#', 'customer no.'):
                cust_id = data.ix[i][name]

            # if name.lower() in ('kunde', 'clients', 'customer', 'client', 'customer name', 'account'):
            # cust_name = data.ix[i][name]
            if name.lower() in (u'product id', u'material id', u'article id', u'artikel id', 'item id'):
                prod_id = str(data.ix[i][name])
            if name.lower() in (u'product', u'material', u'article', u'artikel', 'item', 'article#'):
                try:
                    prod_name = str(data.ix[i][name])
                except:
                    prod_name = data.ix[i][name]
            # if name.lower() in (u'product group', u'item group', u'article group', 'product type', 'type', 'warengruppe'):
            # prod_type = str(data.ix[i][name])
            if name.lower() in ('price', 'pay', 'preis', 'price', 'sum price'):
                sales_data['prod_price'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name.lower() in ('margin', 'margin', 'marge', 'sum margin'):
                sales_data['prod_margin'] = float(str(data.ix[i][name]).replace(",", "."))
            if name.lower() in ('cost', 'costs', 'fabrication cost', 'sum costs'):
                sales_data['prod_cost'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name.lower() == 'unit cost':
                sales_data['prod_unit_cost'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name.lower() == 'unit price':
                sales_data['prod_unit_price'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name.lower() == 'unit margin':
                sales_data['prod_unit_margin'] = float(str(data.ix[i][name]).replace(',', '.'))
            if name.lower() in ('quantity', 'qty', 'amount'):
                try:
                    sales_data['prod_quantity'] = float(str(data.ix[i][name]).replace(',', '.'))
                except:
                    sales_data['prod_quantity'] = 1
            if name.lower() in ('date', 'date', 'invoice date'):
                sales_date = data.ix[i][name]
            if name.lower() in ('invoice', 'invoice no.', 'transaction id'):
                sales_invoice = data.ix[i][name]
            if name.lower() in ('kam', 'account manager', 'accountmanager'):
                sales_kam = data.ix[i][name]

        if 'prod_quantity' in sales_data.keys() and sales_data['prod_quantity'] == 0:
            sales_data['prod_quantity'] = 1

        if 'prod_quantity' not in sales_data.keys():
            sales_data['prod_quantity'] = 1

        if 'prod_unit_price' in sales_data.keys() and 'prod_price' not in sales_data.keys():
            sales_data['prod_price'] = sales_data['prod_unit_price'] * sales_data['prod_quantity']

        if 'prod_unit_price' not in sales_data.keys() and 'prod_price' in sales_data.keys():
            sales_data['prod_unit_price'] = sales_data['prod_price'] / sales_data['prod_quantity']

        if 'prod_unit_cost' in sales_data.keys() and 'prod_cost' not in sales_data.keys():
            sales_data['prod_cost'] = sales_data['prod_unit_cost'] * sales_data['prod_quantity']

        if 'prod_unit_cost' not in sales_data.keys() and 'prod_cost' in sales_data.keys():
            sales_data['prod_unit_cost'] = sales_data['prod_cost'] / sales_data['prod_quantity']

        if 'prod_unit_margin' not in sales_data.keys() and 'prod_unit_cost' in sales_data.keys():
            sales_data['prod_unit_margin'] = sales_data['prod_unit_price'] - sales_data['prod_unit_cost']
        if 'prod_unit_margin' in sales_data.keys() and 'prod_cost' not in sales_data.keys():
            sales_data['prod_unit_cost'] = sales_data['prod_unit_price'] - sales_data['prod_unit_margin']

        if 'prod_margin' not in sales_data.keys() and 'prod_cost' in sales_data.keys():
            sales_data['prod_margin'] = sales_data['prod_price'] - sales_data['prod_cost']
        if 'prod_margin' in sales_data.keys() and 'prod_cost' not in sales_data.keys():
            sales_data['prod_cost'] = sales_data['prod_price'] - sales_data['prod_margin']

        try:
            sales_invoice
        except:
            sales_invoice = 'NULL'

        sales_data['prod_name'] = prod_name
        k = 'prod_name'
        # sales_data[k] = unquote_plus(sales_data[k])
        # try:
        #     sales_data[k] = sales_data[k].strip().decode('utf-8').encode('cp1252')
        # except:
        #     sales_data[k] = sales_data[k].encode('cp1252')

        try:
            script = "\
                SELECT id from products WHERE name='{}'\
                ".format(prod_name)
            cur = con.cursor()
            cur.execute(script)
            # con.commit()
            prod_id = cur.fetchall()[0][0]
            # prod_id = np.ravel(np.asarray(cur.fetchall()))[0]
        except:
            # print(prod_name)
            print("Sales record without  product name/id.")
            # raise

        # print(prod_id)
        try:
            _data = { \
                'customer_id': int(cust_id), \
                'product_id': int(prod_id), \
                'quantity': sales_data['prod_quantity'], \
                'price': sales_data['prod_price'], \
                'cost': sales_data['prod_cost'], \
                'margin': sales_data['prod_margin'], \
                'year': sales_date.year, \
                'month': sales_date.month, \
                'date': sales_date.isoformat().replace("T", " "), \
                'invoice': sales_invoice, \
                # 'kam':sales_kam,\
            }

            sales.insert_sales_record(con, _data)

            # link_user_customer(con, user_id, customer_id)

        except Exception as e:
            print(e)
            print("????")
            pd_data = pd.DataFrame([_data])
            data_not_uploaded = data_not_uploaded.append(pd_data)
            raise

        # print(data_not_uploaded)
        # data_not_uploaded.to_excel('data_not_uploaded.xlsx')


if __name__ == "__main__":
    # dbname = 'ftest'
    # username = 'ftest'
    dbname = 'martinmasip_data_test_2015_2016_copy_super_reduced_xlsx'
    # filename = '/home/webuser/users/aet_at/data/20180124_AET_Accounts.csv'
    username = 'martinmasip'
    dbname = 'martinmasip'
    dbname = 'martin_masip'
    dbname = 'qymatix_best'

    dbname = 'qymatix___aet_com'
    # dbname = 'aet_at'

    local = True
    local = False

    # delete_databases(dbname, username)
    # init_databases(dbname, username)

    # config.clear_table('data_' + dbname + '.sales')
    ##xls2mysql(data='/home/webuser/users/martinmasip/data/data_test_few_records.xlsx', dbname=dbname)
    # xls2mysql(data='/home/webuser/users/martinmasip/data/Sales_analytics_520_Oli_modified_2_short.xlsx', dbname=dbname)
    # xls2mysql(data='/home/webuser/users/martin_masip/data/20170622_Orbus_January_2016-June_2017.xlsx', dbname=dbname)
    ##xls2mysql(data='/home/webuser/users/martin_masip/data/20170622_Orbus_January_2016-June_2017_reduced.xlsx', dbname=dbname)
    # xls2mysql(data='/home/webuser/users/coldjet_qy/data/sales_coldjet.xlsx', dbname=dbname)

    # data = pd.read_excel(filename)
    # data = pd.read_csv(filename, delimiter=';', encoding='cp1252')
    # data = pd.read_csv(filename)
    # print(len(data['AccountId'].unique()))
    # upload_data(dbname, filename)

    UPLOAD_PRODUCT_CLASS = False
    UPLOAD_PRODUCT_LINE = False
    UPLOAD_PRODUCT_TYPE = False
    UPLOAD_PRODUCTS = False
    UPLOAD_CUSTOMERS = False
    # UPLOAD_CUSTOMERS = True
    # UPLOAD_KAM = True
    UPLOAD_KAM = False
    # UPLOAD_SALES = True
    UPLOAD_SALES = False

    # Product Line and Product Type
    if UPLOAD_PRODUCT_CLASS == True:
        filename = '/home/webuser/users/aet_at/data/AET_Warengruppen.xlsx'
        data_cl = load_data(filename=filename)
        upload_product_class(dbname=dbname, data=data_cl)

    # Product Line and Product Type
    if UPLOAD_PRODUCT_LINE == True:
        filename = '/home/webuser/users/aet_at/data/AET_Warengruppen.xlsx'
        data_pl = load_data(filename=filename)
        upload_product_line(dbname=dbname, data=data_pl)

    # Products
    if UPLOAD_PRODUCT_TYPE == True:
        filename_products = '/home/webuser/users/aet_at/data/AET_alle_Artikel.xlsx'
        filename = '/home/webuser/users/aet_at/data/AET_Warengruppen.xlsx'
        data_pt = load_data(filename=filename)
        upload_product_type(dbname=dbname, data=data_pt)
        # upload_products(dbname=dbname, data=data)

    # Products
    if UPLOAD_PRODUCTS == True:
        filename_products = '/home/webuser/users/aet_at/data/AET_alle_Artikel.xlsx'
        data_products = load_data(filename=filename_products)
        upload_products(dbname=dbname, data=data_products)

    # filename = '/home/webuser/users/aet_at/data/AET_Sales_2017.xlsx'
    filename = '/home/webuser/users/aet_at/data/AET_Sales_2017_transactions_not_uploaded-TOIMPORT.xlsx'
    filename = '/home/webuser/users/aet_at/data/AET_Sales_2018-02_A.xlsx'
    filename = '/home/webuser/users/aet_at/data/AET_Sales_bis_2018-02.xls'
    # filename_accounts = '/home/webuser/users/aet_at/data/AET_alle_Adressen.xlsx'
    filename_accounts = filename
    print(filename)
    # dbname = 'aet_at'

    # Upload sales records
    # data.rename(columns={'Price':'Unit Price'}, inplace=True)
    # print(data)
    # print(data['Date'])
    # print(data['Article#'].drop_duplicates())
    # print(data[data['Article#']=='0341201']['Article#'])
    # print(data.columns)
    # print(len(data['Customer address#'].unique()))
    # upload_products(dbname=dbname, data=data)
    # upload_sales(dbname=dbname, data=data, from_line=0, to_line=400)

    # TO UPLOAD ACCOUNTS FROM AET
    if UPLOAD_CUSTOMERS == True:
        # filename_accounts = '/home/webuser/users/aet_at/data/data_AET_qwAdressenAsp.xls'
        filename_accounts = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse.xls'
        data_accounts = load_data(filename=filename_accounts)
        cols = {
            'ADRESSEN_NAM1': 'Account Name',
            'ADRESSEN_KEY': 'Account id',
            'ADRESSEN_ORT': 'city',
            'VORGANG_VERTRETER': 'kam',
            'VORGANG_L_PLZ': 'postcode',
        }
        # data_accounts.rename(columns={'Name 1':'Account Name'}, inplace=True)
        # data_accounts.rename(columns={'AdrKey':'Account id'}, inplace=True)
        data_accounts.rename(columns=cols, inplace=True)
        data_accounts = data_accounts[data_accounts['Account id'] < 300000]
        data_accounts.drop_duplicates('Account id', inplace=True)
        upload_customers(dbname=dbname, data=data_accounts)

    if UPLOAD_KAM == True:
        # filename_accounts = '/home/webuser/users/aet_at/data/data_AET_qwAdressenAsp.xls'
        filename_accounts = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse.xls'
        data_accounts = load_data(filename=filename_accounts)
        cols = {
            'ADRESSEN_NAM1': 'Account Name',
            'ADRESSEN_KEY': 'customer id',
            'ADRESSEN_ORT': 'city',
            'VORGANG_VERTRETER': 'kam',
            'VORGANG_L_PLZ': 'postcode',
        }
        # data_accounts.rename(columns={'Name 1':'Account Name'}, inplace=True)
        # data_accounts.rename(columns={'AdrKey':'Account id'}, inplace=True)
        data_accounts.rename(columns=cols, inplace=True)

        # data_accounts = data_accounts[data_accounts['Jahr']==2018]
        data_accounts = data_accounts[data_accounts['Art'] == 'Verkauf']
        data_accounts = data_accounts[data_accounts['customer id'] < 300000]
        data_accounts.drop_duplicates('customer id', inplace=True)

        upload_kam(dbname=dbname, data=data_accounts)

    # filename_customers = '/home/webuser/users/aet_at/data/data_not_uploaded_AET_Sales_2018-02_A.xlsx'
    # filename_customers = '/home/webuser/users/aet_at/data/data_not_uploaded_AET_Sales_2018-02_A_3.xlsx'
    # data_cust = load_data(filename=filename_customers)
    # id_list = data_cust['customer_id'].drop_duplicates().values
    # print(id_list)
    # upload_customers(dbname=dbname, data=data_accounts, id_list=id_list)

    if UPLOAD_SALES == True:
        ##filename_sales = '/home/webuser/users/aet_at/data/data_not_uploaded_AET_Sales_2018-02_A.xlsx'
        # filename_sales = '/home/webuser/users/aet_at/data/AET_Sales_2018-02_A.xlsx'
        # filename_sales = '/home/webuser/users/aet_at/data/data_not_uploaded_AET_Sales_2018-02_A_3.xlsx'
        filename_sales = '/home/webuser/users/aet_at/data/data_AET_QedvUmsatzAdressenPositionenLieferadresse.xls'
        data_sales = load_data(filename=filename_sales)
        # data_sales.rename(columns={'AdrKey':'customer_id'}, inplace=True)
        cols = {
            'VORGANG_LIEFADR': 'customer_id',
            'VORGANG_VERTRETER': 'kam',
            'VORGANG_DATUM': 'Date',
            'POSITION_ARTNR': 'product',
            'POSITION_SUMN': 'price',
            'POSITION_SUME': 'cost',
            'VORGANG_MENGE': 'quantity',
            'VORGANG_NR': 'invoice',
        }
        data_sales.rename(columns=cols, inplace=True)
        data_sales = data_sales[data_sales['Jahr'] == 2018]
        data_sales = data_sales[data_sales['Art'] == 'Verkauf']
        # print(data_sales.columns)
        # data_sales.rename(columns={'Customer address#':'customer_id'}, inplace=True)
        # upload_sales(dbname=dbname, data=data_sales, id_list=id_list)
        # print(data_sales)
        upload_sales(dbname=dbname, data=data_sales)

    # c1 = data.columns[1]
    # c1 = data.columns[0]
    # data[c1] = data[c1].astype(unicode)
    # print(data[c1].unique())
    # print(len(data[c1]))
    # print(data['Date'])
    # print(data['Article#'])
    # print(len(data[c1].unique()))
    # user_id = insert_kam(dbname=dbname, data=data)
    # upload_customers(dbname=dbname, data=data)
    # upload_product_line(dbname=dbname, data=data)
    # upload_product_type(dbname=dbname, data=data)
    # upload_products(dbname=dbname, data=data)
    # upload_records(dbname=dbname, data=data, from_line=0, to_line=400)

    # ESTE
    # upload_records(dbname=dbname, data=data)

    # insertKamFromFile(dbname=dbname, filename=filename)

    # con = connect_db(dbname)
    # _data = {'date': '2017-07-31 00:00:00', 'cost': 38.0, 'product_id': 5, 'invoice': u'AR027294', 'year': 2017, 'month': 7, 'price': 38.0, 'customer_id': 200140, 'margin': 0.0, 'quantity': 4}
    # sales.insert_sales_record(con, _data)
