import datetime
import os
import sys
from urllib.parse import unquote_plus

import MySQLdb as mysql
import numpy as np
import pandas as pd

import logging

from api.infrastructure.mysql import connection

try:
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from users import getCustomersPerUser
except:
    pass

try:
    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    from users import getCustomersPerUser
except:
    pass

try:
    from api.qymatix.users import getCustomersPerUser
except:
    pass


def getCustomersIdList(cur, username):
    cur.execute("select database()")
    dbname = cur.fetchone()[0]
    dbname = dbname.replace('data_', '').replace('data_', '')
    if username in ['admin', '']:
        username = 'all'
        cust = getCustomersPerUser(dbname=dbname, username=username)
    else:
        cust = getCustomersPerUser(dbname=dbname, username=username)
        cust = cust[next(iter(cust))].replace('[', '(').replace(']', ')')
    return cust


logger = logging.getLogger(__name__)

_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path, '../../..'))
_basepath = '/home/webuser'


def insertContact(data, dbname):
    created = str(datetime.datetime.now())
    if 'name' not in data.keys():
        data = 'Name missing. Cannot insert unknown contact.'
        return data
    if 'title' not in data.keys():
        data['title'] = ''
    if 'description' not in data.keys():
        data['description'] = ''
    if 'account' not in data.keys():
        data['account'] = ''
    if 'account_id' not in data.keys():
        data['account_id'] = ''
    if 'function' not in data.keys():
        data['function'] = ''
    if 'phone' not in data.keys():
        data['phone'] = ''
    if 'email' not in data.keys():
        data['email'] = ''
    if 'linkedin' not in data.keys():
        data['linkedin'] = ''
    if 'xing' not in data.keys():
        data['xing'] = ''

    data['created'] = created

    # for k in ('name', 'account', 'title', 'description', 'function'):
    for k in ('name', 'title', 'description', 'function'):
        data[k] = unquote_plus(data[k])

        # try:
        #     data[k] = data[k].strip().decode('utf-8').encode('cp1252')
        # except:
        #     data[k] = data[k].encode('cp1252')

    try:
        datadb = 'data_' + dbname

        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()

        cur = con.cursor()

        '''
        if data['account'] != '':
            script = "\
                SELECT id from customers WHERE customers.name='{}';\
                ".format(data['account'])
            cur.execute(script)
            con.commit()
            data['account_id'] = np.ravel(np.asarray(cur.fetchall()))[0]
        '''
        data['account_id'] = data['account']

        # (name, address, postcode, city, country, webpage, description, contact)

        script = "INSERT INTO `contacts` (`name`, `title`, `description`, `customer_id`, `function`, `phone`, `email`, `linkedin`, `xing`, `created`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
            data.get('name'),
            data.get('title'),
            data.get('description'),
            data.get('account'),
            data.get('function'),
            data.get('phone'),
            data.get('email'),
            data.get('linkedin'),
            data.get('xing'),
            data.get('created')
        )

        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from contacts;"
        cur.execute(script)
        # con.commit()

        contact_id = np.ravel(np.asarray(cur.fetchall()))[0]

        return contact_id

    except mysql.Error as e:
        # print("Error {}: {}".format(e.args[0], e.args[1]))
        if int(e.args[0]) == 1062:
            script = "SELECT id FROM contacts WHERE name='{}';".format(data['name'])

            cur.execute(script)
            con.commit()

            contact_id = np.ravel(np.asarray(cur.fetchall()))[0]

            return contact_id

            # return 'Contact already exists'
        # sys.exit(1)
        raise

def setContact(dbname, data, local=False):
    """
    """
    if 'id' in data.keys():
        contact_id = data['id']
    else:
        return 'id missing'

    try:
        datadb = "data_" + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()

        cur = con.cursor()

        # for k in ('name', 'account', 'title', 'description', 'function'):
        for k in ('name', 'title', 'description', 'function'):
            if k in data.keys():
                data[k] = unquote_plus(data[k])
                # try:
                #     data[k] = data[k].strip().decode('utf-8').encode('cp1252')
                # except:
                #     data[k] = data[k].encode('cp1252')

        for col in data.keys():
            if col == 'account':
                if data['account'] != '':
                    '''
                    script = "\
                        SELECT id from customers WHERE customers.name='{}';\
                        ".format(data['account'])
                    cur.execute(script)
                    con.commit()
                    data['customer_id'] = np.ravel(np.asarray(cur.fetchall()))[0]
                    '''
                    data['customer_id'] = data['account']
                    col = 'customer_id'

            if col not in ('id', 'contact_id', 'kam_id'):
                value = data[col]
                try:
                    if isinstance(value, str):
                        script = "UPDATE {} SET `{}`='{}' WHERE id={}".format('contacts', col, value, contact_id)
                    else:
                        script = "UPDATE {} SET `{}`={} WHERE id={}".format('contacts', col, value, contact_id)
                    cur.execute(script)
                    con.commit()
                except Exception as e:
                    print(e)

            if col == 'kam_id':
                kam_id = data[col]
                script = "\
                    DELETE FROM {}.Users_Contacts WHERE contact_id={};\
                    ".format("data_" + dbname, int(contact_id))
                cur.execute(script)
                con.commit()
                script = "\
                    INSERT INTO {}.Users_Contacts (user_id, contact_id) VALUES({},{});\
                    ".format("data_" + dbname, int(kam_id), int(contact_id))
                cur.execute(script)
                con.commit()

    # except mysql.Error as e:
    # print("Error {}: {}".format(e.args[0], e.args[1]))
    except Exception as e:
        print(e)

    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. Contact your administrator."

        return contact_id


def deleteContact(dbname, contact_id):
    """
    """

    try:
        datadb = "data_" + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()

        cur = con.cursor()

        try:
            script = "\
                DELETE FROM {}.contacts WHERE id={}\
                ".format("data_" + dbname, int(contact_id))
            cur.execute(script)
            con.commit()

            # script = "\
            # DELETE FROM {}.Users_Contacts WHERE contact_id={};\
            # ".format("data_" + dbname, int(contact_id))
            # cur.execute(script)
            # con.commit()

            return 1

        except mysql.Error as e:
            print("Error {}: {}".format(e.args[0], e.args[1]))
            return -1

        # data = np.asarray(cur.fetchall())

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)


def getContactsList(dbname, account='all', group_id=0, user_id=0, username=""):
    '''
    '''
    datadb = 'data_{}'.format(dbname)
    try:
        mysql_connection = connection.MySQLConnection(datadb)

        con = mysql_connection.connect()

        cur = con.cursor()

        account = unquote_plus(account)

        # try:
        #     account = account.decode('utf-8').encode('cp1252')
        # except:
        #     account = account.encode('cp1252')

        if account != 'all':
            '''
            if account != "":
                script = "\
                    SELECT id FROM {}.customers WHERE name = '{}'\
                    ".format('data_' + dbname, account)

            cur.execute(script)
            con.commit()
            try:
                account_id = np.ravel(np.asarray(cur.fetchall()))[0]
            except:
                return []
            '''
            account_id = account

            # if user_id == 0 and username != "":
            # script = "\
            # SELECT id FROM {0}.users WHERE username = '{1}'\
            # ".format('data_' + dbname, username)
            # cur.execute(script)
            # con.commit()
            # user_id = np.ravel(np.asarray(cur.fetchall()))[0]

        # if group_id == -1:
        # try:
        # group_id = getGroupsPerUser(dbname, user_id=user_id)[user_id]
        # except:
        # group_id = "(-1)"

        # try:
        # group_id = ''.join(str(group_id))[1:-1]
        # except:
        # pass

        if account == 'all':
            if username in ['admin']:
                script = "\
                    SELECT name FROM contacts\
                    "
            else:
                cust = getCustomersIdList(cur, username)
                script = "\
                    SELECT name FROM contacts AS co\
                    WHERE co.customer_id IN {1}\
                    ".format('data_' + dbname, cust, user_id)


        elif account != 'all':
            '''
            script = "\
                SELECT id FROM {0}.customers WHERE name = '{1}'\
                ".format('data_' + dbname, account)
            cur.execute(script)
            con.commit()
            account_id = np.ravel(np.asarray(cur.fetchall()))[0]
            '''
            account_id = account

            if username in ['', 'admin']:
                script = "\
                    SELECT name, id FROM contacts AS co\
                    WHERE co.customer_id='{0}'\
                    ".format(account_id)
            else:
                cust = getCustomersIdList(cur, username)
                script = "\
                    SELECT name, id FROM contacts AS co\
                    WHERE co.customer_id='{0}' AND co.customer_id IN {1}\
                    ".format(account_id, cust)

        cur.execute(script)

        contacttlist = np.asarray(cur.fetchall())  # .reshape(-1)
        # print(contacttlist)
        # results = contacttlist.tolist()
        # print(results)

        results = list()
        for data in contacttlist:
            item = {
                "name": data[0],
                "id": data[1]
            }
            results.append(item)
    except Exception as e:
        results = list()
        raise

    finally:
        try:
            con.close()
        except:
            pass

    return results


def getContacts(dbname, account='all', username=''):
    '''
    '''
    datadb = 'data_{}'.format(dbname)

    try:
        mysql_connection = connection.MySQLConnection(datadb)

        con = mysql_connection.connect()

        cur = con.cursor()

        account = unquote_plus(account)
        # try:
        #     account = account.decode('utf-8').encode('cp1252')
        # except:
        #     account = account.encode('cp1252')

        if account == 'all':

            if username in ['', 'admin']:
                # script_nop = "\
                # select c.*, u.name as 'kam' from {0}.customers as c\
                # left join {1}.Users_Customers as uc on c.id = uc.customer_id\
                # left join {1}.users as u on uc.user_id = u.id\
                # ".format(datadb, tasksdb)

                # script_nop = "\
                # SELECT * FROM contacts\
                # "
                script_nop = "\
                    SELECT contacts.*, customers.id, customers.name  FROM contacts left join customers on customers.id=contacts.customer_id\
                    "
            else:
                cust = getCustomersIdList(cur, username)
                script_nop = "\
                    SELECT contacts.*, customers.id, customers.name FROM contacts left join customers on customers.id=contacts.customer_id\
                    WHERE customers.id IN {}\
                    ".format(cust)
                # WHERE contacts.name = '{}'\

        else:
            # SELECT name, address, city, postcode, country FROM customers\
            script_nop = "\
                SELECT contacts.*, customers.id, customers.name FROM contacts left join customers on customers.id=contacts.customer_id\
                WHERE contacts.name = '{}'\
                ".format(account)

            # script_nop = "\
            # select c.*, u.name as 'kam' from {0}.customers as c\
            # left join {1}.Users_Customers as uc on c.id = uc.customer_id\
            # left join {1}.users as u on uc.user_id = u.id\
            # where c.name = '{2}'\
            # ".format(datadb, tasksdb, account)

        cur.execute(script_nop)

        custlist = np.asarray(cur.fetchall()).reshape(-1)
        custlist = custlist.reshape(len(custlist) // 13, 13)

        results = dict()
        results['contact_id'] = custlist[:, 0].tolist()
        results['name'] = custlist[:, 1].tolist()
        results['title'] = custlist[:, 2].tolist()
        results['description'] = custlist[:, 3].tolist()

        results['customer_id'] = custlist[:, 4].tolist()
        results['account'] = custlist[:, 11].tolist()
        results['function'] = custlist[:, 5].tolist()
        results['phone'] = custlist[:, 6].tolist()
        results['email'] = custlist[:, 7].tolist()
        results['linkedin'] = custlist[:, 8].tolist()
        results['xing'] = custlist[:, 9].tolist()
        results['account_name'] = custlist[:, 12].tolist()
        # results['created'] = custlist[:, 10].tolist()[0].strftime("%Y-%m-%d %H:%M:%S")

        for x in range(len(results['name'])):
            # for k in ('name', 'title', 'account', 'description', 'function'):
            for k in ('name', 'title', 'description', 'function'):
                if results[k][x] != None:
                    results[k][x] = results[k][x].encode('latin-1').decode('cp1252')

    except mysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        results = {}
        # raise

    finally:
        try:
            con.close()
        except:
            pass

    return results


def getContactsByCustomer(dbname, account='all', username=''):
    '''
    '''

    # username = 'admin'

    datadb = 'data_{}'.format(dbname)
    try:
        mysql_connection = connection.MySQLConnection(datadb)

        con = mysql_connection.connect()

        cur = con.cursor()

        '''
        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')
        '''

        if account == 'all':

            if username in ['', 'admin']:
                script_nop = "\
                    SELECT contacts.*, customers.name as account_name FROM contacts left join customers on customers.id=contacts.customer_id\
                    "
            else:
                cust = getCustomersIdList(cur, username)
                script_nop = "\
                    SELECT contacts.*, customers.name as account_name FROM contacts left join customers on customers.id=contacts.customer_id where customers.id IN {}\
                    ".format(cust)

        else:

            if username in ['', 'admin']:
                script_nop = "\
                    SELECT contacts.*, customers.name as account_name FROM contacts left join customers on customers.id=contacts.customer_id WHERE customers.id={}\
                    ".format(account)
            else:
                cust = getCustomersIdList(cur, username)
                script_nop = "\
                    SELECT contacts.*, customers.name as account_name FROM contacts left join customers on customers.id=contacts.customer_id where customers.id={} AND customers.id IN {}\
                    ".format(account, cust)

        cur.execute(script_nop)
        results = dict()
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]
        try:
            if data.any():
                df = pd.DataFrame(data, columns=cols)
                grouped = df.groupby('customer_id')
                for name, group in grouped:
                    # group = group.rename(columns={'due':'due', 'action':'type', 'description':'comment', 'plan':'plan_id'})
                    # group[['due', 'id', 'created', 'action', 'title', 'description' ]]
                    import json
                    results[str(name)] = json.loads(group.to_json(orient='records'))
                # return df.to_json(orient='records')
            else:
                return 'null'
        except Exception as e:
            import traceback
            return str(traceback.format_exc())
        """
        cur.execute(script_nop)
        data = np.asarray(cur.fetchall())
        script_cols = "\
            SELECT `COLUMN_NAME`\
            FROM `INFORMATION_SCHEMA`.`COLUMNS`\
            WHERE `TABLE_SCHEMA`='{}'\
            AND `TABLE_NAME`='{}';\
            ".format(datadb, 'contacts')

        cur.execute(script_cols)
        cols = np.ravel(np.asarray(cur.fetchall()))
        # cols = [c if c != 'customer_id' else 'customer' for c in cols]
        cols = cols.tolist()
        cols.append('account')

        try:
            df = pd.DataFrame(data, columns=cols)

            s = lambda x: x.encode('latin-1').decode('cp1252')
            df['account'] = df['account'].apply(s)
            df['name'] = df['name'].apply(s)
            df['title'] = df['title'].apply(s)
            df['description'] = df['description'].apply(s)
            df['function'] = df['function'].apply(s)

            # f = lambda x: x.isoformat().replace("T", " ") if x is not None else None
            grouped = df.groupby('customer_id')

            results = {}
            for name, group in grouped:
                # group = group.rename(columns={'due':'due', 'action':'type', 'description':'comment', 'plan':'plan_id'})
                # group[['due', 'id', 'created', 'action', 'title', 'description' ]]
                results[str(name)] = group.to_json(orient='records')

            # if account != 'all':
            # results = results[name]

        except Exception as e:
            print("ERROR")
            print(e)
            results = {}
            # raise
        """
    # except mysql.Error as e:
    except Exception as e:
        # print "Error %d: %s" % (e.args[0],e.args[1])
        # results = []
        print(e)
        results = {}
        # raise

    finally:
        try:
            con.close()
        except:
            pass
    
    return results


if __name__ == "__main__":
    new_contact = {
        'name': "John",
        'email': "johny@tolengo.com",
        'description': "This is a test contact, it is not real.",
        # 'customer_id': 1
        # 'customer': 'Acrion Solutions'
        'account': 'Acrion Solutions'
    }
    new_contact = {
        'name': "Ricky Ticky Tavi",
        'email': "ricky@tolengo.com",
        'description': "This is a test contact, it is not real.",
        # 'customer_id': 1
        # 'customer': 'Acrion Solutions'
        'account': 'Diotimus AG'
    }
    new_contact = {
        'name': "Batman Returns",
        'email': "batman@cientific.com",
        'description': "This is a test contact, it is not real.",
        # 'customer_id': 1
        # 'customer': 'Acrion Solutions'
        'account': 'Diotimus AG'
    }

    # modify_contact = {'id':44, 'name':'Bartman'}
    # modify_contact = {'id':44, 'account':'Acrion Solutions'}
    modify_contact = {'id': 1, 'description': 'DD'}

    username = "martinmasip"
    username = 'qymatix_best'
    dbname = 'qymatix_best'
    # username = "demo"
    # contact = insertContact(new_contact, dbname=username)
    # print(contact)

    # contact_id = 3
    # deleteContact(contact_id=contact_id, dbname=username)
    # setContact(data=modify_contact, dbname=username)

    # contacts = getContacts(username)
    # print(contacts)
    # contacts = getContacts(username, 'Carlitos Way')
    # print(contacts)
    # contacts = getContacts(username, 'Bartman')
    # print(contacts)
    dbname = 'qymatix_de'
    dbname = 'qymatix_best'
    account = 'TZ AG'
    account = 'all'
    username = 'Thilo_Oenning__qymatix_de'
    username = 'martin_masip__qymatix_de'
    # username = 'admin'
    username = 'chancho_babe__qymatix_best'
    # account = 'Robo TZ AG'
    # account = 'AET Entwaesserungstechnik GmbH'
    account = 'Acrion Solutions'
    # account = 'all'
    account = 1
    # contacts = getContacts(dbname, account, username=username)
    # contacts = getContactsList(dbname, account, username=username)
    # print(contacts)
    # contacts = getContacts(dbname=dbname, account=account, username=username)
    # print(contacts)

    contacts = getContactsByCustomer(dbname, account=account, username=username)
    print(contacts)

    # account = 'Diotimus AG'
    # account = 'Witty Chemie GmbH n Co KG'
    # contacts = getContactsByCustomer(dbname, account, username)
    # print(contacts)

    # contacts = getContactsByCustomer(username, 'Acrion Solutions')
    # print(contacts)
