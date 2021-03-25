"""
Databases queries related to Task Model
"""
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=bare-except
# pylint: disable=broad-except
# pylint: disable=lost-exception
# pylint: disable=pointless-string-statement
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=unidiomatic-typecheck
# pylint: disable=too-many-nested-blocks
# pylint: disable=superfluous-parens
# pylint: disable=no-name-in-module
# pylint: disable=unused-variable
# pylint: disable=too-many-lines
# pylint: disable=too-many-arguments
# pylint: disable=unexpected-keyword-arg
# pylint: disable=redefined-outer-name
# pylint: disable=logging-format-interpolation
# pylint: disable=no-else-return
import datetime
import logging
import traceback
from urllib.parse import unquote_plus
import numpy as np
import pandas as pd
import MySQLdb as mysql
from .groups import getGroupsPerUser
from ..infrastructure.mysql import connection

logger = logging.getLogger(__name__)


def createTask(dbname, account, title, action, due, group_id=1, plan="",
               plan_id=0, kam="", kam_id=0, status="New",
               description="", end=None, allday=0, username=None):
    """
    Query to create Task record into db
    """
    created = str(datetime.datetime.now())

    try:
        _due = datetime.datetime.strptime(due, "%Y-%m-%d %H:%M:%S")
    except:
        _due = datetime.datetime.strptime(due, "%Y-%m-%d")

    if end is None or _due >= end:
        end = _due + datetime.timedelta(hours=1)
    end = str(end)

    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        plan = unquote_plus(plan)
        try:
            plan = plan.decode('utf-8').encode('cp1252')
        except:
            plan = plan.encode('cp1252')

        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')
        title = unquote_plus(title)
        try:
            title = title.decode('utf-8').encode('cp1252')
        except:
            title = title.encode('cp1252')
        description = unquote_plus(description)
        try:
            description = description.decode('utf-8').encode('cp1252')
        except:
            description = description.encode('cp1252')
        kam = unquote_plus(kam)
        try:
            kam = kam.decode('utf-8').encode('cp1252')
        except:
            kam = kam.encode('cp1252')

        if kam_id == 0:
            if kam != "":
                script = "\
                    SELECT id FROM users WHERE username = '{}'\
                    ".format(kam)
            else:
                script = "\
                    SELECT id FROM users WHERE username = '{}'\
                    ".format(username)

            cur.execute(script)
            con.commit()
            kam_id = np.ravel(np.asarray(cur.fetchall()))[0]

        if plan_id == 0:
            if plan != "":
                script = "\
                    SELECT id FROM plans WHERE name = '{}'\
                    ".format(plan)
            else:
                plan_id = None

            cur.execute(script)
            con.commit()
            kam_id = np.ravel(np.asarray(cur.fetchall()))[0]

        script = "INSERT INTO `tasks` " \
                 "(group_id, owner_id, plan, account, title, " \
                 "description, action, created, due, status, " \
                 "end, allday) VALUES " \
                 "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', " \
                 "'{}', '{}', '{}', '{}');".format(group_id, kam_id,
                                                   plan_id, account, title,
                                                   description, action,
                                                   created, due, status,
                                                   end, allday)
        cur.execute(script)
        con.commit()

        script = "\
            SELECT MAX(id) from tasks;\
            "
        cur.execute(script)
        con.commit()

        task_id = np.ravel(np.asarray(cur.fetchall()))[0]

        if plan_id != None:
            script = "INSERT INTO Plans_Actions (plan_id, task_id) " \
                     "VALUES({},{});".format(int(plan_id), int(task_id))
            cur.execute(script)
            con.commit()

        script = "INSERT INTO Users_Actions (user_id, task_id) " \
                 "VALUES({},{});".format(int(kam_id), int(task_id))
        cur.execute(script)
        con.commit()

        return task_id

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )


def createAction(dbname, action, username=None):
    """
        Query to create Task record into db

        var action = {
          "account": this.model.account,
          "owner_id": this.model.owner_id,
          "due":this.model.due,
          "type":this.model.type,
          "plan_id":5,
          "title":this.model.title,
          "comment":this.model.comment,
          "end":this.model.end,
          "date":this.model.due,
          "group_id": this.model.group_id,
          "contact_id": this.model.contact
        }
    """
    ls = dict()
    try:
        action['type']
    except:
        action['type'] = ['Call']
    if 'group_id' not in action.keys():
        action['group_id'] = 1
    if 'group' not in action.keys():
        action['group'] = ""
    if 'plan_id' not in action.keys():
        action['plan_id'] = 0
    if type(action['plan_id']) is not int:
        action['plan_id'] = None
    if 'plan' not in action.keys():
        action['plan'] = ""
    if 'owner_id' not in action.keys():
        action['owner_id'] = 0
        # action['kam_id'] = request.user.id
    if 'kam' not in action.keys():
        action['kam'] = ""
    if 'end' not in action.keys():
        action['end'] = None
    if 'allday' not in action.keys():
        action['allday'] = 0
    if 'comment' not in action.keys():
        action['comment'] = ""
    if 'due' not in action.keys():
        action['due'] = ""
    if 'description' not in action.keys():
        action['description'] = ""
    if 'comment' in action.keys():
        action['description'] = action['comment']
    if 'contact_id' not in action.keys():
        action['contact_id'] = 0
    if 'contact' not in action.keys():
        action['contact'] = ""

    for k in action.keys():
        if k in ('name', 'description', 'owner', 'title',
                 'kam', 'group', 'plan', 'contact'):
            value = action[k]
            value = unquote_plus(value)

            # try:
            #     value = value.decode('utf-8').encode('cp1252')
            # except:
            #     value = value.encode('cp1252')
            action[k] = value

    account = action.get('account')
    title = action.get('title')
    description = action.get('description')  # .replace("'", "''")
    action_type = action.get('type')
    status = 'New'
    due = action.get('due')
    group_id = action.get('group_id')
    group = action.get('group')
    plan_id = action.get('plan_id')
    plan = action.get('plan')
    kam = action.get('kam')
    kam_id = action.get('owner_id')
    end = action.get('end')
    allday = action.get('allday')
    created = str(datetime.datetime.now())
    contact = action.get('contact')
    contact_id = action.get('contact_id')

    try:
        _due = datetime.datetime.strptime(action.get('due'), "%Y-%m-%d %H:%M")
    except:
        _due = datetime.datetime.strptime(action.get('due'), "%Y-%m-%d")

    if action.get('end') is None:
        end = _due + datetime.timedelta(hours=1)

    end = str(end)

    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        '''
        if account != 'all':
            if account != "":
                script = "\
                    SELECT id FROM {}.customers WHERE name = '{}'\
                    ".format(dbname.replace('data_', 'data_'), account)

            cur.execute(script)
            con.commit()
            account_id = np.ravel(np.asarray(cur.fetchall()))[0]
        '''
        account_id = account

        if action['owner_id'] == 0:
            if kam != "":
                script = "SELECT id FROM users WHERE " \
                         "username = '{}';".format(kam)
            else:
                script = "SELECT id FROM users WHERE " \
                         "username = '{}';".format(username)

            cur.execute(script)
            # con.commit()
            kam_id = np.ravel(np.asarray(cur.fetchall()))

        if action['contact_id'] == 0:
            if contact != "":
                script = "SELECT id FROM {}.contacts WHERE " \
                         "name = '{}';".format(dbname.replace('data_',
                                                              'data_'),
                                               contact)

                cur.execute(script)
                try:
                    contact_id = np.ravel(np.asarray(cur.fetchall()))[0]
                except:
                    contact_id = "NULL"
                    contact_id = 0
            else:
                contact_id = 0

        if action['plan_id'] == 0:
            if plan not in ("", 'null'):
                script = "SELECT id FROM plans WHERE name = '{}';".format(
                    plan
                )
                cur.execute(script)
                # con.commit()
                plan_id = np.ravel(np.asarray(cur.fetchall()))[0]
            else:
                plan_id = "NULL"

        if action['group_id'] == 0:
            if group != "":
                script = "SELECT id FROM groups WHERE name = '{}';".format(
                    group
                )
                cur.execute(script)
                # con.commit()
                group_id = np.ravel(np.asarray(cur.fetchall()))[0]

            else:
                group_id = 1

        script = "INSERT INTO `tasks` " \
                 "(`group_id`, `owner_id`, `plan`, `account`, `title`, " \
                 "`description`, `action`, `created`, `due`, " \
                 "`status`, `end`, `allday`, `contact_id`) " \
                 "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', " \
                 "'{}', '{}', '{}', '{}', '{}');;".format(group_id, kam_id,
                                                          plan_id, account_id,
                                                          title, description,
                                                          action_type,
                                                          created, due,
                                                          status, end, allday,
                                                          contact_id)
        cur.execute(script)
        con.commit()

        script = "SELECT MAX(id) from tasks;"
        cur.execute(script)

        task_id = np.ravel(np.asarray(cur.fetchall()))[0]

        if plan_id not in ('NULL', 'None', None):
            script = "INSERT INTO Plans_Actions " \
                     "(plan_id, task_id) " \
                     "VALUES({},{});".format(int(plan_id), int(task_id))
            cur.execute(script)
            con.commit()

        script = "INSERT INTO Users_Actions (user_id, task_id) " \
                 "VALUES({},{});".format(int(kam_id), int(task_id))
        cur.execute(script)
        con.commit()

        return task_id

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )


def setAction(dbname, action):
    """
    Query for Update the tasks record
    """
    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        for col in action.keys():
            if col not in ('id', 'plan_id', 'created', 'kam_id'):
                value = action[col]
                if col in ('Comment', 'comment', 'description'):
                    col = 'description'
                if col in ('title', 'description'):
                    value = unquote_plus(value)
                    try:
                        value = value.decode('utf-8').encode('cp1252')
                    except:
                        value = value.encode('cp1252')
                    value = value.replace("'", "''")
                if col in ('starts', 'due'):
                    col = 'due'
                if col in ('type'):
                    col = 'action'

                action_id = action['id']
                script = "UPDATE {} SET {}='{}' " \
                         "WHERE id={}".format('tasks', col, value, action_id)
                cur.execute(script)
                con.commit()

            if col == 'plan_id':
                script = "INSERT INTO Plans_Actions (plan_id, task_id) " \
                         "VALUES({},{});".format(int(action['plan_id']),
                                                 int(action['id']))
                cur.execute(script)
                con.commit()

                script = "UPDATE {} SET {}='{}' " \
                         "WHERE id={}".format('tasks', col, value, action_id)
                cur.execute(script)
                con.commit()

            if col == 'kam_id':
                script = "INSERT INTO Users_Actions (user_id, task_id) " \
                         "VALUES({},{});".format(int(action['kam_id']),
                                                 int(action['id']))
                cur.execute(script)
                con.commit()

                script = "UPDATE {} SET {}='{}' " \
                         "WHERE id={}".format('tasks', col, value, action_id)
                cur.execute(script)
                con.commit()

            response = 'true'

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        response = 'false'

    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. " \
                   "Contact your administrator."

    return response


def modifyActionExtended(dbname, action):
    """
    Query to Update the tasks
    """
    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        if 'end' in action.keys():
            if 'starts' in action.keys():
                action['due'] = action['starts']
            if action['due'] >= action['end']:
                action['end'] = action['due'] + datetime.timedelta(hours=1)
        else:
            action['end'] = action['due'] + datetime.timedelta(hours=1)

        for col in action.keys():
            if col not in ('id', 'plan', 'plan_id', 'created', 'owner',
                           'group', 'kam_id', 'contact_id'):
                value = action[col]
                if col in ('Comment', 'comment', 'description'):
                    col = 'description'
                if col in ('title', 'description'):
                    value = unquote_plus(value)
                    try:
                        value = value.decode('utf-8').encode('cp1252')
                    except:
                        value = value.encode('cp1252')
                    value = value.replace("'", "''")
                if col in ('starts', 'due'):
                    col = 'due'
                if col in ('type'):
                    col = 'action'

                action_id = action['id']
                script = "UPDATE {} SET {}='{}' " \
                         "WHERE id={}".format('tasks', col, value, action_id)
                cur.execute(script)
                con.commit()

            if col in ('owner', 'group', 'plan', 'contact'):
                value = unquote_plus(value)
                try:
                    value = value.decode('utf-8').encode('cp1252')
                except:
                    value = value.encode('cp1252')

            if col == 'plan':
                script = "SELECT id FROM plans WHERE " \
                         "plans.name='{}'".format(value)
                cur.execute(script)
                con.commit()
                col = 'plan_id'
                value = np.ravel(np.asarray(cur.fetchall()))[0]

            if col == 'owner':
                script = "\
                    SELECT id FROM users WHERE users.username='{}'\
                    ".format(value)
                cur.execute(script)
                con.commit()
                col = 'owner_id'
                value = np.ravel(np.asarray(cur.fetchall()))[0]

            if col == 'group':
                script = "\
                    SELECT id FROM groups WHERE groups.name='{}'\
                    ".format(value)
                cur.execute(script)
                con.commit()
                col = 'group_id'
                value = np.ravel(np.asarray(cur.fetchall()))[0]

            if col == 'plan_id' and value != None:
                script = "INSERT INTO Plans_Actions (plan_id, task_id) " \
                         "VALUES({},{});".format(int(action['plan_id']),
                                                 int(action['id']))
                cur.execute(script)
                con.commit()

                script = "UPDATE {} SET {}='{}' " \
                         "WHERE id={}".format('tasks', col, value, action_id)
                cur.execute(script)
                con.commit()

            if col == 'kam_id':
                script = "INSERT INTO Users_Actions (user_id, task_id) " \
                         "VALUES({},{});".format(int(action['kam_id']),
                                                 int(action['id']))
                cur.execute(script)
                con.commit()

                script = "UPDATE {} SET {}='{}' " \
                         "WHERE id={}".format('tasks', col, value, action_id)
                cur.execute(script)
                con.commit()

            response = 'true'

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        response = 'false'
    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. " \
                   "Contact your administrator."

    return response


def modifyAction(dbname, action):
    """
    Query to Update the Action
    """
    response = ""
    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        if 'starts' in action.keys():
            action['due'] = action['starts']

        if 'due' in action.keys():
            try:
                _due = datetime.datetime.strptime(
                    action['due'], "%Y-%m-%d %H:%M:%S"
                )
            except:
                _due = datetime.datetime.strptime(action['due'], "%Y-%m-%d")

            if 'end' in action.keys():
                try:
                    _end = datetime.datetime.strptime(
                        action['end'], "%Y-%m-%d %H:%M:%S"
                    )
                except:
                    _end = datetime.datetime.strptime(
                        action['end'], "%Y-%m-%d"
                    )

                if _due >= _end:
                    _end = _due + datetime.timedelta(hours=1)
            else:
                _end = _due + datetime.timedelta(hours=1)

            action['end'] = _end.isoformat().replace("T", " ")

        for col in action.keys():
            if col not in ('id', 'plan_id', 'created', 'kam_id', 'contact',
                           'contact_id'):
                value = action[col]
                if col in ('Comment', 'comment', 'description'):
                    col = 'description'
                if col in ('title', 'description'):
                    value = unquote_plus(value)

                    value = value.replace("'", "''")
                if col in ('starts', 'due'):
                    col = 'due'
                if col in ('type'):
                    col = 'action'

                action_id = action['id']
                script = "UPDATE {} SET {}='{}' " \
                         "WHERE id={};".format('tasks', col, value, action_id)
                cur.execute(script)
                con.commit()

            if col == 'contact' and 'contact_id' not in action.keys():
                value = action[col]
                value = unquote_plus(value)
                if action[col] != "":
                    script = "SELECT id FROM {}.contacts " \
                             "WHERE id = '{}';".format(dbname.replace('data_',
                                                                      'data_'),
                                                       value)
                    cur.execute(script)
                    try:
                        value = np.ravel(np.asarray(cur.fetchall()))[0]
                    except:
                        value = 0
                else:
                    value = 0

                col = 'contact_id'
                script = "UPDATE {} SET {}='{}' " \
                         "WHERE id={};".format('tasks', col, value, action_id)
                cur.execute(script)
                con.commit()

            if col == 'plan_id':
                try:
                    script = "INSERT INTO Plans_Actions (plan_id, task_id) " \
                             "VALUES({},{});".format(int(action['plan_id']),
                                                     int(action['id']))
                    cur.execute(script)
                    con.commit()

                    script = "UPDATE {} SET {}='{}' " \
                             "WHERE id={};".format('tasks', col, value,
                                                   action_id)
                    cur.execute(script)
                    con.commit()
                except:
                    response = response + " " + "Could not assign Plan."

            if col == 'kam_id':
                try:
                    # script = "UPDATE Users_Actions SET user_id={}
                    # WHERE task_id={}".format(action['kam_id'], action['id'])
                    script = "DELETE FROM Users_Actions " \
                             "WHERE task_id={};".format(action['id'])
                    cur.execute(script)
                    con.commit()

                    script = "INSERT INTO Users_Actions (user_id, task_id) " \
                             "VALUES({},{});".format(int(action['kam_id']),
                                                     int(action['id']))
                    cur.execute(script)
                    con.commit()

                    script = "UPDATE {} SET {}='{}' WHERE " \
                             "id={};".format('tasks', 'owner_id',
                                             action['kam_id'], action['id'])
                    cur.execute(script)
                    con.commit()
                except:
                    response = response + " " + "Could not assign KAM."

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
        raise

    finally:
        try:
            if con:
                con.close()
        except:
            return "Problem connecting to the database. " \
                   "Contact your administrator."

    if response == "":
        response = "true"

    return response


def dropTask(dbname, tasks):
    """
    Query to delete the task from db
    """
    taskid = tasks.get('id')
    task_type = tasks.get('_type')

    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        if task_type == 'action':
            script = "\
                DELETE FROM Plans_Actions WHERE task_id={};\
                ".format(int(taskid))

            cur.execute(script)
            con.commit()

            script = "\
                DELETE FROM Users_Actions WHERE task_id={};\
                ".format(int(taskid))

            cur.execute(script)
            con.commit()

            script = "\
                DELETE FROM {data_db}.tasks WHERE id = {task_id}\
                ".format(data_db=dbname, task_id=taskid)
            cur.execute(script)
            con.commit()
            return taskid
            # data = np.asarray(cur.fetchall())
        else:
            script = "DELETE FROM {data_db}.tasks WHERE " \
                     "id = {task_id}".format(data_db=dbname, task_id=taskid)
            cur.execute(script)
            con.commit()
            return taskid

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        task = {
            "err": str(traceback.format_exc()),
            "status_code": 500
        }
        return task


def getTasks(dbname='username', account='all'):
    ''' Reads tasks's database, manipulate the data and returns it.
    '''

    try:
        mysql_connection = connection.MySQLConnection(dbname)

        con = mysql_connection.connect()

        cur = con.cursor()

        '''
        script_cols = "\
            SELECT `COLUMN_NAME`\
            FROM `INFORMATION_SCHEMA`.`COLUMNS`\
            WHERE `TABLE_SCHEMA`='{}'\
            AND `TABLE_NAME`='{}';\
            ".format(dbname, 'tasks')

        cur.execute(script_cols)
        cols = np.ravel(np.asarray(cur.fetchall()))
        '''

        # script_nop = "\
        # select c.*, u.name as 'kam' from {0}.customers as c\
        # left join {1}.Users_Customers as uc on c.id = uc.customer_id\
        # left join {1}.users as u on uc.user_id = u.id\
        # ".format(datadb, tasksdb)

        account = unquote_plus(account)
        try:
            account = account.decode('utf-8').encode('cp1252')
        except:
            account = account.encode('cp1252')

        if account.decode() == 'all':
            script = "\
                SELECT * from tasks;\
                "
        else:
            script = "\
                SELECT * from tasks\
                WHERE account='{}';\
                ".format(account)

        cur.execute(script)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]

        try:
            df = pd.DataFrame(data, columns=cols)

            # f = lambda x: x.isoformat().split("T")[0]
            f = lambda x: x.isoformat().replace("T", " ") if x is not None else None
            # print(df)
            try:
                df['due'] = df['due'].apply(f)
            except Exception as exception:
                df['due'] = None

            try:
                df['end'] = df['end'].apply(f)
            except Exception as exception:
                df['end'] = None

            df['created'] = df['created'].apply(f)
            # print(df['plan'])

            grouped = df.groupby('account')

            tasks = {}
            for name, group in grouped:
                group = group.rename(
                    columns={'due': 'due', 'action': 'type',
                             'description': 'comment', 'plan': 'plan_id'}
                )
                tasks[name] = group.to_json(orient='records')
        except Exception as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )
            tasks = list()

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        tasks = list()

    finally:
        if con:
            con.close()

    return tasks


def getActions(dbname='username', account='all', group_id=0, user_id=0, username=""):
    """
     Reads tasks's database, manipulate the data and returns it.
    """
    if username == 'admin':
        username = ''
        user_id = 0
        group_id = 0
    tasks = dict()
    try:
        datadb = 'data_' + dbname

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

        if account != 'all':
            account_id = account

        if user_id == 0 and username != "":
            script = "SELECT id FROM users WHERE username = '{}';".format(
                username
            )
            cur.execute(script)
            # con.commit()
            user_id = np.ravel(np.asarray(cur.fetchall()))[0]

        if group_id == -1:
            try:
                group_id = getGroupsPerUser(dbname, user_id=user_id)[user_id]
            except:
                group_id = "(-1)"

            try:
                group_id = ''.join(str(group_id))[1:-1]
            except:
                pass

        if account == 'all' and group_id == 0 and user_id == 0:
            script = "SELECT t.*, c.name AS account_name, " \
                     "c.address as account_address, " \
                     "c.postcode as account_postcode, " \
                     "c.city as account_city, c.country as account_country, " \
                     "p.name AS 'plan_name', u.name AS 'owner', " \
                     "g.name AS 'group', co.name AS 'contact' " \
                     "FROM tasks AS t " \
                     "LEFT JOIN {0}.customers AS c ON t.account = c.id " \
                     "LEFT JOIN {0}.contacts AS co ON t.contact_id = co.id " \
                     "LEFT JOIN plans AS p ON t.plan = p.id " \
                     "LEFT JOIN `users` AS `u` ON t.owner_id = u.id " \
                     "LEFT JOIN `groups` AS g ON " \
                     "t.group_id = g.id;".format('data_' + dbname)

        elif account == 'all' and group_id != 0 and user_id == 0:
            script = "SELECT t.*, c.name AS account_name, " \
                     "c.address as account_address, " \
                     "c.postcode as account_postcode, " \
                     "c.city as account_city, c.country as account_country, " \
                     "p.name AS 'plan_name', u.name AS 'owner', " \
                     "g.name AS 'group', co.name AS 'contact' " \
                     "FROM tasks AS t " \
                     "LEFT JOIN {0}.customers AS c ON t.account = c.id " \
                     "LEFT JOIN {0}.contacts AS co ON t.contact_id = co.id " \
                     "LEFT JOIN plans AS p ON t.plan = p.id " \
                     "LEFT JOIN `users` AS u ON t.owner_id = u.id " \
                     "LEFT JOIN `groups` AS g ON t.group_id = g.id " \
                     "WHERE t.group_id IN ({1});".format('data_' + dbname,
                                                         group_id)

        elif account == 'all' and group_id == 0 and user_id != 0:
            script = "SELECT t.*, c.name AS account_name, " \
                     "c.address as account_address, " \
                     "c.postcode as account_postcode, " \
                     "c.city as account_city, " \
                     "c.country as account_country, p.name AS 'plan_name', " \
                     "u.name AS 'owner', g.name AS 'group', " \
                     "co.name AS 'contact' FROM tasks AS t " \
                     "LEFT JOIN {0}.customers AS c ON t.account = c.id " \
                     "LEFT JOIN {0}.contacts AS co ON t.contact_id = co.id " \
                     "LEFT JOIN plans AS p ON t.plan = p.id " \
                     "LEFT JOIN `users` AS u ON t.owner_id = u.id " \
                     "LEFT JOIN `groups` AS g ON t.group_id = g.id " \
                     "WHERE t.owner_id = '{1}';".format('data_' + dbname,
                                                        user_id)

        elif account == 'all' and group_id != 0 and user_id != 0:
            script = "SELECT t.*, c.name AS account_name, " \
                     "c.address as account_address, "\
                     "c.postcode as account_postcode, " \
                     "c.city as account_city, c.country as account_country, "\
                     "p.name AS 'plan_name', u.name AS 'owner', " \
                     "g.name AS 'group', co.name AS 'contact' " \
                     "FROM tasks AS t "\
                     "LEFT JOIN {0}.customers AS c ON t.account = c.id "\
                     "LEFT JOIN {0}.contacts AS co ON t.contact_id = co.id "\
                     "LEFT JOIN plans AS p ON t.plan = p.id "\
                     "LEFT JOIN `users` AS u ON t.owner_id = u.id "\
                     "LEFT JOIN `groups` AS g ON t.group_id = g.id "\
                     "WHERE t.group_id IN ({1}) OR " \
                     "t.owner_id = '{2}';".format('data_' + dbname,
                                                  group_id,
                                                  user_id)

        elif account != 'all' and group_id != 0 and user_id == 0:
            script = "SELECT t.*, c.name AS account_name, " \
                     "c.address as account_address, "\
                     "c.postcode as account_postcode, " \
                     "c.city as account_city, " \
                     "c.country as account_country, "\
                     "p.name AS 'plan_name', u.name AS 'owner', " \
                     "g.name AS 'group', co.name AS 'contact' " \
                     "FROM tasks AS t "\
                     "LEFT JOIN {0}.customers AS c ON t.account = c.id "\
                     "LEFT JOIN {0}.contacts AS co ON t.contact_id = co.id "\
                     "LEFT JOIN plans AS p ON t.plan = p.id "\
                     "LEFT JOIN `users` AS u ON t.owner_id = u.id "\
                     "LEFT JOIN `groups` AS g ON t.group_id = g.id "\
                     "WHERE t.account = {1} and " \
                     "t.group_id IN ({2});".format('data_' + dbname,
                                                   account_id,
                                                   group_id)

        elif account != 'all' and group_id != 0 and user_id != 0:
            script = "SELECT t.*, c.name AS 'account_name', " \
                     "c.address as account_address, "\
                     "c.postcode as account_postcode, " \
                     "c.city as account_city, c.country as account_country, "\
                     "p.name AS 'plan_name', u.name AS 'owner', " \
                     "g.name AS 'group', co.name AS 'contact' " \
                     "FROM tasks AS t "\
                     "LEFT JOIN {0}.customers AS c ON c.id=t.account "\
                     "LEFT JOIN {0}.contacts AS co ON t.contact_id = co.id "\
                     "LEFT JOIN plans AS p ON t.plan = p.id "\
                     "LEFT JOIN `users` AS u ON t.owner_id = u.id "\
                     "LEFT JOIN `groups` AS g ON t.group_id = g.id "\
                     "WHERE t.account = '{1}' and (t.group_id IN ({2}) OR " \
                     "t.owner_id = '{3}');".format('data_' + dbname,
                                                   account_id,
                                                   group_id,
                                                   user_id)

        elif account != 'all' and group_id == 0 and user_id != 0:
            # else:
            script = "SELECT t.*, c.name AS account_name, " \
                     "c.address as account_address, "\
                     "c.postcode as account_postcode, " \
                     "c.city as account_city, c.country as account_country, "\
                     "p.name AS 'plan_name', u.name AS 'owner', " \
                     "g.name AS 'group', co.name  AS 'contact' " \
                     "FROM tasks AS t "\
                     "LEFT JOIN {0}.customers AS c ON t.account = c.id "\
                     "LEFT JOIN {0}.contacts AS co ON t.contact_id = co.id "\
                     "LEFT JOIN plans AS p ON t.plan = p.id "\
                     "LEFT JOIN `users` AS `u` ON t.owner_id = u.id "\
                     "LEFT JOIN `groups` AS g ON t.group_id = g.id "\
                     "WHERE t.account = '{1}' and " \
                     "t.owner_id = '{2}';".format('data_' + dbname,
                                                  account_id,
                                                  user_id)

        elif account != 'all' and group_id == 0 and user_id == 0:
            # else:
            script = "SELECT t.*, c.name AS account_name, " \
                     "c.address as account_address, "\
                     "c.postcode as account_postcode, " \
                     "c.city as account_city, c.country as account_country, "\
                     "p.name AS 'plan_name', u.name AS 'owner', " \
                     "g.name AS 'group', co.name AS 'contact' " \
                     "FROM tasks AS t "\
                     "LEFT JOIN {0}.customers AS c ON t.account = c.id "\
                     "LEFT JOIN {0}.contacts AS co ON t.contact_id = co.id "\
                     "LEFT JOIN plans AS p ON t.plan = p.id "\
                     "LEFT JOIN `users` AS `u` ON t.owner_id = u.id "\
                     "LEFT JOIN `groups` AS g ON t.group_id = g.id "\
                     "WHERE t.account = {1};".format('data_' + dbname,
                                                     account_id)

        test = dict()
        cur.execute(script)
        data = np.asarray(cur.fetchall())
        cols = [desc[0] for desc in cur.description]

        try:
            try:
                df = pd.DataFrame(data, columns=cols)
            except:
                df = ""
            if str(df):
                s = lambda x: x  # encode('latin-1').decode('cp1252')
                df['description'] = df['description'].apply(s)
                df['account_id'] = df['account']
                df['account'] = df['account_name']
                df['account_address'] = df['account_address']
                df['account_postcode'] = df['account_postcode']
                df['account_city'] = df['account_city']
                df['account_country'] = df['account_country']
                df.drop('account_name', inplace=True, axis=1)
                df['account'].replace('None', 'Missing account', inplace=True)
                df['account'].fillna('Missing account', inplace=True)
                df['account'] = df['account'].apply(s)
                df['plan'] = df['plan'].apply(s)
                df['title'] = df['title'].apply(s)
                # df['owner'] = df['owner'].apply(s)
                df['group'] = df['group'].apply(s)
                df['contact'].replace('None', '', inplace=True)
                df['contact'].fillna('', inplace=True)
                df['contact'] = df['contact'].apply(s)
                # df.drop('contact_id', inplace=True, axis=1)

                # f = lambda x: x.isoformat().split("T")[0]
                f = lambda x: x.isoformat().replace("T", " ") if x is not None else None
                # print(df)
                try:
                    df['due'] = df['due'].apply(f)
                    due_date_format = pd.to_datetime(df['due'])
                    df['due_cal'] = due_date_format.dt.strftime('%Y%m%dT%H%M%S')
                except:
                    df['due'] = None

                try:
                    df['end'] = df['end'].apply(f)
                    end_date_format = pd.to_datetime(df['end'])
                    df['end_cal'] = end_date_format.dt.strftime('%Y%m%dT%H%M%S')
                except:
                    df['end'] = None

                df['created'] = df['created'].apply(f)

                grouped = df.groupby('account_id')

                for name, group in grouped:
                    group = group.rename(
                        columns={'due': 'due', 'action': 'type',
                                 'description': 'comment', 'plan': 'plan_id'})
                    tasks[name] = group.to_json(orient='records')
        except Exception as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )
            tasks = traceback.format_exc()

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        tasks = traceback.format_exc()

    finally:
        if con:
            con.close()

    return tasks


def getActionsGroupedByPlan(dbname='username', account='all'):
    """
    Query to get the action per group
    """

    try:
        datadb = "data_" + dbname

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

            try:
                script = "\
                    SELECT plans.id, tasks.id\
                    FROM (Plans_Actions\
                    LEFT JOIN plans\
                    ON Plans_Actions.plan_id=plans.id)\
                    LEFT JOIN tasks\
                    ON Plans_Actions.task_id=tasks.id\
                    "

                cur.execute(script)
                data = np.asarray(cur.fetchall())

            except mysql.Error as e:
                logger.debug("Error {}: {}".format(e.args[0], e.args[1]))

        else:
            try:
                '''
                script = "\
                    SELECT id FROM {}.customers WHERE name = '{}'\
                    ".format('data_' + dbname, account)
                cur.execute(script)
                con.commit()
                account_id = np.ravel(np.asarray(cur.fetchall()))[0]
                '''
                account_id = account

                script = "\
                    SELECT plans.id, tasks.id\
                    FROM (Plans_Actions\
                    LEFT JOIN plans\
                    ON Plans_Actions.plan_id=plans.id)\
                    LEFT JOIN tasks\
                    ON Plans_Actions.task_id=tasks.id\
                    WHERE plans.account='{}';\
                    ".format(account_id)

                cur.execute(script)
                data = np.asarray(cur.fetchall())

            except mysql.Error as e:
                logger.debug("Error {}: {}".format(e.args[0], e.args[1]))

        try:
            df = pd.DataFrame(data, columns=['plan_id', 'task_id'])
            grouped = df.groupby('plan_id')

            plans = {}
            for name, group in grouped:
                plans[name] = group['task_id'].to_json(orient='records')
        except:
            plans = {}
            logger.debug("Error")

    except mysql.Error as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        logger.debug("Error {}: {}".format(exception.args[0],
                                           exception.args[1]))
        plans = []
        return plans

    finally:
        try:
            if con:
                con.close()
        except:
            return "DB connection failed."

    return plans


if __name__ == "__main__":

    local = True
    local = False

    if local:
        dbusername = 'webadmin'
    else:
        dbusername = 'webuser'
    passwd = 'Qymatix!!!'

    username = 'martinmasip'
    username = 'crmtest1'
    dbname = username
    dbname = "data_crmtest1"
    username = 'sapo_pepe'
    username = 'alice__qymatix___solutions_com'
    dbname = 'qymatix___solutions_com'

    username = 'martin_masip__qymatix_de'
    dbname = 'qymatix_de'
    account = 'A100 Row Gmbh'
    account = 'all'

    username = 'martin__qy___test_com'
    dbname = 'qy___test_com'

    account = 'all'
    account = 'Diotimus AG'

    # username = 'ep__mtm___ne_de'
    # dbname = 'mtm___ne_de'

    username = 'chancho_babe__qymatix_best'
    # username = 'admin'
    dbname = 'qymatix_best'
    # account = 'Diotimus AG'
    account = 'all'
    account = 852
    # dbname = 'aet_at'
    # username = 'waselberger__aet_at'

    action = {"id": 20, "title": "Action New",
              "comment": "Descriptions", "type": "visit",
              "due": "2017-08-31 08:00:00",
              "end": "2017-08-31 08:30:00", "status": "New",
              "kam_id": 8998, "plan_id": "None"}
    action = {"title": "Action NEW NEW NEW", "comment": "Descriptions",
              "type": "visit", "due": "2017-08-31 08:00:00",
              "end": "2017-08-31 08:30:00", "status": "New",
              "kam_id": 8998, "plan_id": "None",
              'account': 'Herz-Zentrum Landau'}
    action = {'comment': 'Yes we can',
              'account': 'Gemeinschaftsklinikum Koblenz-Mayen / St. Elisabet',
              'end': '2017-08-24 01:00:00',
              'title': 'This was massuploaded',
              'due': '2017-8-25', 'kam': '',
              'plan': 'null', 'date': '2017-8-25',
              'type': 'visit'}
    action = {'comment': '2017-8-16 | User modified the Sales Plan',
              'account': 'Kliniken der Stadt K\\xc3\\xb6ln gGmbH '
                         'Krankenhaus Merheim',
              'end': '2017-08-22 13:00:00',
              'title': 'Sales Plan modified',
              'due': '2017-8-25', 'kam': '', 'plan': 'null',
              'date': '2017-8-25',
              'type': 'change'}
    action = {'comment': 'User modified the Sales Plan',
              'account': 'Diotimus AG', 'end': '2017-08-22 13:00:00',
              'title': 'Test', 'due': '2017-8-25', 'kam': '',
              'plan': 'null', 'date': '2017-8-25', 'type': 'change'}
    action = {'id': 160, 'status': 'Closed'}
    action = {'id': 160, 'status': 'New'}

    action = {"account": 1, "owner_id": 0, "due": "2018-02-16 12:00:00",
              "type": "call", "title": "AAA", "comment": "",
              "date": "2018-02-16 12:00:00", "contact": ""}
    action = {"account": "63", "plan_id": 73,
              "title": "Hot Plan Qymatix Alarm",
              "comment": "This is a Qymatix Alarm. Do something.",
              "type": "alarm", "due": "2018-2-2 12:00:00"}
    data = getActions(dbname=dbname, local=local, group_id=-1,
                      user_id=0, username=username, account=account)
