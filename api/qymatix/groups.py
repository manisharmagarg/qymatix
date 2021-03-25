import datetime
import json
import logging
import os
from urllib.parse import unquote_plus

import MySQLdb as mysql
import numpy as np
import pandas as pd
from django.conf import settings

from api.infrastructure.mysql import connection


logger = logging.getLogger(__name__)


def createGroup(dbname, group, username=None, local=False):
    '''
    '''

    _dbname = dbname
    datadb = "data_" + dbname

    for k in group.keys():
        if k in ('name', 'description'):
            value = group[k]
            value = unquote_plus(value)

            # try:
            #     value = value.decode('utf-8').encode('cp1252')
            # except:
            #     value = value.encode('cp1252')
            group[k] = value

    created = str(datetime.datetime.now())
    name = group['name']
    description = group['description']

    try:
        owner_id = int(group['owner_id'])
    except:
        owner_id = 0

    try:
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if owner_id == 0:
            try:
                script = "SELECT id FROM users WHERE "\
                "username = '{username}'".format(
                    username=username
                )
                cur.execute(script)
                owner_id = np.ravel(np.asarray(cur.fetchall()))[0]
            except:
                data = dict()
                data["err_msg"] = "No User found related to '{}' username".format(username)
                data["message"] = "Either add the User related to '{}' username or "\
                                    "Contact Administrator".format(
                                        username
                                        )
                data["user_id"] = None
                data["error"] = 1
                return data

        script = "INSERT INTO {db_}.groups "\
                "(name, description, owner_id, created) "\
                "VALUES ('{name}', '{description}', "\
                "'{owner_id}', '{created}');".format(
                    db_=datadb, 
                    name=name, 
                    description=description, 
                    owner_id=owner_id, 
                    created=created
                )
        cur.execute(script)
        con.commit()

        '''
        script = "\
            SELECT id from groups\
            WHERE groups.owner_id='{}'\
            ;\
            ".format(owner_id)
        cur.execute(script)
        group_id = np.asarray(cur.fetchall())[0]
        '''

        script = "SELECT MAX(id) from {db_}.groups;".format(
            db_=datadb
            )
        cur.execute(script)
        group_id = np.ravel(np.asarray(cur.fetchall()))[0]

        addUserToGroup(_dbname, owner_id, group_id)

        return "Group saved."

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))

        return "Error saving plan."


def modifyGroup(dbname, group, local=False):
    """
    """
    dbname = "data_" + dbname

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        for col in group.keys():
            if col not in ('id', 'group_id', 'created'):
                value = group[col]
                if col in ('Comment', 'comment', 'description'):
                    col = 'description'
                if col in ('name', 'description'):
                    value = unquote_plus(value)
                    # try:
                    #     value = value.decode('utf-8').encode('cp1252')
                    # except:
                    #     value = value.encode('cp1252')
                    # value = value.decode('utf-8').encode('cp1252')
                if col in ('starts', 'due'):
                    col = 'due'
                    # value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                group_id = group['id']
                script = "UPDATE {db_name}.{tb_name} SET {col_name}='{val_name}' "\
                        "WHERE id={group_id}".format(
                            db_name=dbname, 
                            tb_name='groups', 
                            col_name=col, 
                            val_name=value, 
                            group_id=group_id
                            )
                cur.execute(script)
                con.commit()

            response = 'true'

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        response = 'false'

    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. Contact your administrator."

    return response


def deleteGroup(dbname, groupid, local=False):
    """
    """

    dbname = "data_" + dbname

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "\
            DELETE FROM Users_Groups WHERE group_id={};\
            ".format(int(groupid))

        cur.execute(script)
        con.commit()

        script = "\
            DELETE FROM groups WHERE id={}\
            ".format(groupid)
        cur.execute(script)
        con.commit()

        # data = np.asarray(cur.fetchall())

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)


def addUserToGroup(dbname, user_id, group_id, local=False):
    '''
    '''

    dbname = "data_" + dbname

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "INSERT INTO Users_Groups (user_id, group_id) VALUES({},{});".format(
            int(user_id), 
            int(group_id)
        )

        cur.execute(script)
        con.commit()
        '''
        try:
            data = np.asarray(cur.fetchall())
            logger.debug("__xxxyyy_____")
            logger.debug(data)
        except:
            data = {}
        '''
        data = 1

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        # data = e.args[1]
        # data = {}
        # data = 'Error'
        data = 0

    finally:
        if con:
            con.close()

    return data


def removeUserFromGroup(dbname, user_id, group_id, local=False):
    '''
    '''

    dbname = "data_" + dbname

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        script = "\
            DELETE FROM Users_Groups WHERE group_id={} AND user_id={};\
            ".format(int(group_id), int(user_id))

        cur.execute(script)
        con.commit()
        data = np.asarray(cur.fetchall())

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        # sys.exit(1)
        data = e.args[1]

    finally:
        if con:
            con.close()

    return data


def getGroups(dbname='username', user="", username='', user_id=0, raw=False, local=False):
    ''' Reads plans' database, manipulate the data and returns it.
    '''

    try:
        datadb = "data_" + dbname
        mysql_connection = connection.MySQLConnection(datadb)
        con = mysql_connection.connect()
        cur = con.cursor()

        if user_id == 0 and user != "":
            script = "SELECT `id` FROM `users` WHERE username = '{}';".format(user)
            cur.execute(script)

            data = cur.fetchall()
            try:
                user_id = np.ravel(np.asarray(data))[0]
            except:
                user_id = 0

        if user_id != 0:
            try:
                group_id = getGroupsPerUser(dbname, username=username, user_id=user_id)[user_id]
            except:
                group_id = "(-1)"

        try:
            group_id = ''.join(str(group_id))[1:-1]
        except:
            pass

        if user_id == 0:
            script = "SELECT * from `groups`;"
        else:
            script = "SELECT * from `groups` WHERE `groups`.id IN ({});".format(group_id)

        cur.execute(script)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]

        try:
            df = pd.DataFrame(data, columns=cols)

            # f = lambda x: x.isoformat().split("T")[0]
            f = lambda x: x.isoformat().replace("T", " ")
            df['created'] = df['created'].apply(f)

            grouped = df.groupby('name')

            groups = {}
            for name, group in grouped:
                groups[name] = group.to_json(orient='records')

            a = getUsersPerGroup(dbname, username=username)

            for acc in groups.keys():
                groups_ = json.loads(groups[acc])
                for i in range(len(groups_)):
                    group_id = groups_[i]['id']
                    if a != []:
                        if group_id in a.keys():
                            groups_[i]['members_id'] = a[group_id]
                        else:
                            groups_[i]['members_id'] = "[]"
                    else:
                        groups_[i]['members_id'] = "[]"

                groups_ = json.dumps(groups_)
                groups[acc] = groups_

        except:
            groups = []

    except mysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        # sys.exit(1)
        groups = {}

    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. Contact your administrator."

    return groups


def getUsersPerGroup(dbname='username', user='all', user_id=0, username='', raw=False, local=False):
    '''
    '''

    dbname = "data_" + dbname

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        if username == 'admin':
            user_id = 0
        else:
            script = "SELECT * FROM users WHERE username = '{}';".format(
                username
            )
            cur.execute(script)
            user_id = np.ravel(np.asarray(cur.fetchall()))[0]

        if user == 'all' and user_id == 0:

            script = "SELECT `groups`.id, `users`.id FROM (`Users_Groups` LEFT JOIN `groups` ON `Users_Groups`.group_id=`groups`.id) LEFT JOIN `users` ON `Users_Groups`.user_id=`users`.id"


        elif user == 'all' and user_id != 0:
            script = "SELECT `groups`.id, `users`.id FROM (`Users_Groups` LEFT JOIN `groups` ON `Users_Groups`.group_id=`groups`.id) LEFT JOIN `users` ON `Users_Groups`.user_id=`users`.id ".format(user_id)

        elif user != 'all' and user_id == 0:
            script = "SELECT `groups`.id, `users`.id FROM (Users_Groups LEFT JOIN groups ON `Users_Groups`.group_id=`groups`.id) LEFT JOIN `users` ON `Users_Groups`.user_id=`users`.id WHERE `users`.username='{}'; ".format(user)

        else:
            script = "SELECT `groups`.id, `users`.id FROM (`Users_Groups` LEFT JOIN `groups` ON `Users_Groups`.group_id=`groups`.id) LEFT JOIN `users` ON `Users_Groups`.user_id=`users`.id WHERE `users`.id='{}';".format(user_id)

        cur.execute(script)
        data = np.asarray(cur.fetchall())

        try:
            df = pd.DataFrame(data, columns=['group_id', 'user_id'])
            grouped = df.groupby('group_id')

            groups = {}
            for name, group in grouped:
                groups[name] = group['user_id'].to_json(orient='records')

            if username != 'admin':
                script = "\
                    SELECT group_id FROM Users_Groups\
                    WHERE Users_Groups.user_id={}\
                    ".format(user_id)
                # ".format(str(groups[user_id]).replace('[', '(').replace(']', ')'))
                cur.execute(script)
                _users = np.asarray(cur.fetchall())
                _users = [u for sl in _users for u in sl]
                # list(chain.from_iterable(_users))

                groups = {k: groups[k] for k in _users}


        except:
            groups = {}
            # raise

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        groups = e.args[1]
        return groups

    finally:
        try:
            if con:
                con.close()
        except:
            return "DB connection failed."

    return groups


def getGroupsPerUser(dbname='username', user='all', user_id=0, username='', raw=False, local=False):
    '''
    '''

    dbname = "data_" + dbname

    try:
        mysql_connection = connection.MySQLConnection(dbname)
        con = mysql_connection.connect()
        cur = con.cursor()

        if username == 'admin':
            user_id = 0
        else:

            script = "SELECT * FROM `users` WHERE username = '{}';".format(username)
            cur.execute(script)
            user_id = np.ravel(np.asarray(cur.fetchall()))[0]

        if user == 'all' and user_id == 0:

            script = "SELECT `groups`.id, `users`.id FROM (`Users_Groups` LEFT JOIN `groups` ON `Users_Groups`.group_id=`groups`.id) LEFT JOIN `users` ON `Users_Groups`.user_id=`users`.id;"

        elif user == 'all' and user_id != 0:
            script = "SELECT `groups`.id, `users`.id FROM (`Users_Groups` LEFT JOIN `groups` ON `Users_Groups`.group_id=`groups`.id) LEFT JOIN `users` ON `Users_Groups`.user_id=`users`.id;".format(user_id)

        elif user != 'all' and user_id == 0:
            script = "SELECT `groups`.id, `users`.id FROM (`Users_Groups` LEFT JOIN `groups` ON `Users_Groups`.group_id=`groups`.id) LEFT JOIN `users` ON `Users_Groups`.user_id=`users`.id WHERE `users`.username='{}';".format(user)

        else:
            script = "SELECT `groups`.id, `users`.id FROM (`Users_Groups` LEFT JOIN `groups` ON `Users_Groups`.group_id=`groups`.id) LEFT JOIN `users` ON `Users_Groups`.user_id=`users`.id WHERE `users`.id='{}';".format(user_id)

        cur.execute(script)
        data = np.asarray(cur.fetchall())

        try:
            df = pd.DataFrame(data, columns=['group_id', 'user_id'])
            grouped = df.groupby('user_id')

            groups = {}
            for name, group in grouped:
                groups[name] = group['group_id'].to_json(orient='records')

            if username != 'admin':
                script = "SELECT user_id FROM Users_Groups "\
                        "WHERE `Users_Groups`.`group_id` IN {};".format(
                            str(groups[user_id]).replace('[', '(').replace(']', ')')
                        )
                cur.execute(script)
                _users = np.asarray(cur.fetchall())
                _users = [u for sl in _users for u in sl]
                # list(chain.from_iterable(_users))

                groups = {k: groups[k] for k in _users}

        except Exception as e:
            print(e)
            groups = {}
            # raise
            # groups = {'No groups': 2}

    except mysql.Error as e:
        print("Error {}: {}".format(e.args[0], e.args[1]))
        groups = e.args[1]
        return groups

    finally:
        try:
            if con:
                con.close()
        except:
            return "DB connection failed."

    return groups


if __name__ == "__main__":
    group = dict()
    group['name'] = 'Test Group 4'
    group['owner_id'] = 2
    group['description'] = 'A tiny description of the group.'

    username = 'martin_masip'

    dbname = 'qymatix_best'
    username = 'sapo_pepe'

    dbname = 'qymatix_com'
    username = 'lucas_pedretti'
    username = 'sapo_pepe'
    dbname = 'qymatix_de'
    username = 'martin_masip'
    dbname = 'qymatix_best'

    # createGroup(dbname, group, username=username)

    group['id'] = 2
    group['owner_id'] = 1
    # modifyGroup(dbname, group)
    # deleteGroup(dbname, 11)
    # groups = getGroups(dbname)
    username = 'lobo_feroz'
    username = 'martin_masip__qymatix_de'
    username = 'chancho_babe__qymatix_best'
    dbname = 'qymatix_de'
    dbname = 'qymatix_best'
    # groups = getGroups(dbname, username=username, user_id=0)
    # groups = getGroups(dbname, username="chancho_babe", user_id=0)
    # print(groups)
    # addUserToGroup(dbname, 1, 2)
    # addUserToGroup(dbname, 20, 1)
    # addUserToGroup(dbname, 17, 2)
    # groups = getGroupsPerUser(dbname)
    print("GROUPS")
    # print(groups)
    # users = getUsersPerGroup(dbname, user='all', user_id=0)
    # print(">>>")
    # print(users)
    # users = getGroupsPerUser(dbname, user=username, user_id=0)
    username = 'admin'
    users = getGroupsPerUser(dbname, user='all', username=username)
    print(users)
    users = getUsersPerGroup(dbname, user='all', username=username)
    print("...")
    print(users)
    # removeUserFromGroup(dbname, 17, 2)
    # groups = getGroupsPerUser(dbname)
    # print(groups)
