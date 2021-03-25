"""
Script responsible to API related to Task Model
"""
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=empty-docstring
# pylint: disable=unused-argument
# pylint: disable=bare-except
# pylint: disable=broad-except
# pylint: disable=unexpected-keyword-arg
# pylint: disable=unused-variable
# pylint: disable=no-value-for-parameter
# pylint: disable=too-many-lines
# pylint: disable=keyword-arg-before-vararg
# pylint: disable=no-self-use
# pylint: disable=assignment-from-no-return
# pylint: disable=too-many-branches
# pylint: disable=redefined-outer-name
# pylint: disable=no-member
import json
import logging
import os
import traceback
from ast import literal_eval
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from .qymatix import actions, kam, plans, util, sales


logger = logging.getLogger(__name__)

_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path, '../../..'))
_basepath = settings.BASE_DIR


class PageView(TemplateView):
    """
    """
    page_slug = None
    page_title = None
    page_lead = None
    page_nav = None

    def get_page_data(self):
        """
        """
        return {
            u"slug": self.page_slug,
            u"title": self.page_title,
            u"lead": self.page_lead,
            u"nav": self.page_nav,
            # u"base_url": u"/"
        }

    def get_context_data(self, **kwargs):
        """
        """
        context = super(PageView, self).get_context_data(**kwargs)
        context[u'page'] = self.get_page_data()
        return context


class ApiDocActionsView(PageView):
    """
    """
    template_name = u"api/docs/actions_api.html"
    page_slug = u"home"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):
        """
        """
        context = {}

        return render(request, "api/docs/actions_api.html", context)


apidoc_actions_api = ApiDocActionsView.as_view()


@ensure_csrf_cookie
def getTasks(request, account='all', workspace=1, *args, **kwargs):
    """
    API to get the tasks record
    """
    if request.method == 'GET':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

        db_name = util.getDatabaseName(_basepath, username)

        data = actions.getTasks(dbname="data_" + db_name, account=account)
        response = json.dumps(data)
        status = 200
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def getActions(request, account='all', workspace=1, *args, **kwargs):
    """
    API to get the actions records
    """
    if request.method == 'GET':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

        db_name = util.getDatabaseName(_basepath, username)

        _user = request.user.configuration.account_type
        if _user != 'admin':
            _user = request.user.username

        data = actions.getActions(
            dbname=db_name, account=account, group_id=-1,
            user_id=0, username=_user
        )
        response = json.dumps(data)
        status = 200
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def dropTask(request, task, workspace=1):
    """
    API to delete the tasks data from db
    """
    try:
        task_raw_data = literal_eval(task)
    except:
        task_raw_data = 'None'

    try:
        if request.method == 'POST':
            logger.debug(request.environ)
            logger.debug(task_raw_data)

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            db_name = util.getDatabaseName(_basepath, username)

            task_response = actions.dropTask(
                "data_" + db_name,
                tasks=task_raw_data
            )
            response = json.dumps(task_response)
            status = 200
        else:
            response = ''
            status = 400
    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        response = {
            "message": str(traceback.format_exc())
        }
        response = json.dumps(response)
        status = 500
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def setTask(request, task, workspace=1):
    """
    API to update the tasks records
    """
    try:
        task = literal_eval(task)

        if request.method == 'POST':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
                db_name = util.getDatabaseName(_basepath, username)

            try:
                task['type']
            except:
                task['type'] = ['Call']
            if 'group_id' not in task.keys():
                task['group_id'] = 1
            if 'plan' not in task.keys():
                task['plan'] = ""
            if 'plan_id' not in task.keys():
                task['plan_id'] = 0
            if 'kam' not in task.keys():
                task['kam'] = ""
            if 'kam_id' not in task.keys():
                task['kam_id'] = 0
                # task['kam_id'] = request.user.id
            if 'end' not in task.keys():
                task['end'] = None
            if 'allday' not in task.keys():
                task['allday'] = 0
            if 'comment' not in task.keys():
                task['comment'] = ""

            task_id = actions.createTask( \
                "data_" + db_name, \
                username=request.user.username, \
                account=task['account'], \
                title=task['title'], \
                description=task['comment'], \
                action=task['type'], \
                status='New', \
                due=task['date'], \
                group_id=task['group_id'], \
                plan_id=task['plan_id'], \
                kam=task['kam'], \
                kam_id=task['kam_id'], \
                end=task['end'], \
                allday=task['allday'] \
                )

            logging.info(task_id)
            task['id'] = str(task_id)
            response = json.dumps(task)
            status = 200
        else:
            response = ''
            status = 400

    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={'type': 'Login'}
        )
        response = 'Cannot create task'
        status = 500
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )



@ensure_csrf_cookie
def createAction(request, task, workspace=1):
    """
    API to create the action record in db
    """
    try:
        task = literal_eval(task)

        if request.method == 'POST':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
                db_name = util.getDatabaseName(_basepath, username)

            task_id = actions.createAction(
                "data_" + db_name, task,
                username=request.user.username
            )

            response = str(task_id)
            status = 200
        else:
            response = ''
            status = 400
    except Exception as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={'type': 'Login'}
        )
        response = json.dumps(
            {
                "message": "Internal Server Error"
            }
        )
        status = 500
    return HttpResponse(
        response, content_type="application/json", status=status
    )


@ensure_csrf_cookie
def modifyAction(request, action, workspace=1):
    """
    API to update the Action record
    """
    if request.method == 'POST':
        action = literal_eval(action)

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

        db_name = util.getDatabaseName(_basepath, username)

        data = actions.modifyAction(dbname="data_" + db_name, action=action)
        response = json.dumps(data)
        status = 200
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def createKam(request, data, workspace=1):
    """
    API to insert the KAM record
    """
    try:
        kam_data = literal_eval(data)

        if request.method == 'POST':
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            db_name = util.getDatabaseName(_basepath, username)
            kam_data["username"] = username
            user_id = kam.insertKam(db_name, kam_data)

            data = {'id': str(user_id)}
            response = json.dumps(data)
            status = 200
        else:
            response = ''
            status = 400
    except (
            NameError,
            TypeError,
            KeyError,
            ValueError,
            AttributeError,
            IndexError
    ) as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        response = json.dumps(
            {
                "error": str(traceback.format_exc()),
                "status_code": 500
            }
        )
        status = 500
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def modifyKam(request, data, workspace=1):
    """
    API to modify the KAM record
    """
    if request.method == 'POST':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        user = literal_eval(data)
        data = kam.setKam(db_name, data=user)
        response = json.dumps(data)
        status = 200

    else:
        response = ''
        status = 400

    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def deleteKam(request, kamid='', workspace=1):
    """
    API to delete KAM record
    """
    try:
        kamid = int(kamid)
    except:
        data = 'false'

    if request.method == 'POST':
        try:
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            kam.dropKam("data_" + db_name, \
                        user_id=kamid, \
                        )
            # data = json.dumps(planid)
            response = 'true'
            status = 200
        except:
            response = kamid
            status = 500
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def getKam(request, data='all', workspace=1):
    """
    API to get the KAM record
    """
    try:
        try:
            kam_ = literal_eval(data)
        except:
            kam_ = 'all'

        if request.method == 'GET':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            _user = request.user.configuration.account_type
            if _user != 'admin':
                _user = request.user.username
            try:
                _kam = kam.getKam("data_" + db_name, user=kam_, username=_user, group_id=-1)
                response = json.dumps(_kam)
                status = 200
            except Exception as e:
                data = {
                    "message": e,
                    "traceback": traceback.format_exc()
                }
                response = json.dumps(data)
                status = 500
        else:
            response = ''
            status = 400
    except Exception as e:
        response = str(traceback.format_exc())
        status = 500
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def mergeKams(request, data, workspace=1):
    """
    API to merge the KAM
    """
    if request.method == 'POST':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        data = literal_eval(data)
        response = kam.mergeKams(db_name, data=data)
        # data = json.dumps(data)
        status = 200

    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def plansToActions(request, account='all', workspace=1):
    """
    API to get PLan per Action
    """
    if request.method == 'GET':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)
        db_name = 'data_' + db_name

        data = dict()
        data = plans.plansToActions(db_name, local=False, account=account)
        response = json.dumps(data.tolist())
        status = 200
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def getPlansGroupedByAction(request, account='all', workspace=1):
    """
    API to get the plan as per group
    """
    if request.method == 'GET':

        workspace = int(workspace)

        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)
        db_name = 'data_' + db_name

        data = dict()
        data = plans.getPlansPerAction(db_name, local=False, account=account)
        response = str(data)
        status = 200
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def getActionsGroupedByPlan(request, account='all', workspace=1):
    """
    API to get Action group by plan
    """
    if request.method == 'GET':
        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        data = dict()
        data = actions.getActionsGroupedByPlan(db_name, local=False, account=account)
        # data = json.dumps(data, sort_keys=True)
        response = str(data)
        status = 200

    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def linkPlanToAction(request, lk, workspace=1):
    """
    API to get the link plan to action
    """
    if request.method == 'POST':

        try:
            lk = literal_eval(lk)
            plan_id = lk[0]
            task_id = lk[1]

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            db_name = 'data_' + db_name
            logging.debug(db_name)

            data = dict()
            data['Response'] = plans.linkPlanToAction(
                db_name, plan_id=plan_id,
                task_id=task_id, local=False
            )
            # data = json.dumps(data, sort_keys=True)
            # str(data)
            data['Status'] = 'Ok'

            response = json.dumps(data, sort_keys=True)
            status = 200
        except:
            response = "Could not link data"
            status = 500
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def linkKamToAction(request, lk, workspace=1):
    """
    API to link Kam with action
    """

    if request.method == 'POST':

        try:
            lk = literal_eval(lk)
            user_id = lk[0]
            task_id = lk[1]

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            db_name = 'data_' + db_name
            logging.debug(db_name)

            data = dict()
            data['Response'] = kam.linkUserToAction(
                db_name, user_id=user_id,
                task_id=task_id, local=False
            )
            # data = json.dumps(data, sort_keys=True)
            # str(data)
            # logger.debug(data)
            data['Status'] = 'Ok'

            response = json.dumps(data, sort_keys=True)
            status = 200
        except:
            response = "Could not link data"
            status = 500
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def linkKamToPlan(request, lk, workspace=1):
    """
    API link Kam to Plan
    """
    if request.method == 'POST':

        try:
            lk = literal_eval(lk)
            user_id = lk[0]
            plan_id = lk[1]

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            db_name = 'data_' + db_name
            logging.debug(db_name)

            data = dict()
            data['Response'] = kam.linkUserToPlan(
                db_name, user_id=user_id,
                plan_id=plan_id, local=False
            )
            # data = json.dumps(data, sort_keys=True)
            # str(data)
            # logger.debug(data)
            data['Status'] = 'Ok'

            response = json.dumps(data, sort_keys=True)
            status = 200
        except:
            response = "Could not link data"
            status = 500
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def unlinkKamFromAction(request, lk, workspace=1):
    """
    API to unlink the Kam from Action
    """
    if request.method == 'POST':

        lk = literal_eval(lk)
        user_id = lk[0]
        task_id = lk[1]

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)
        db_name = 'data_' + db_name

        data = dict()
        data = kam.unlinkUserFromAction(db_name, user_id=user_id, task_id=task_id, local=False)
        response = json.dumps(data, sort_keys=True)
        status = 200
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def unlinkKamFromPlan(request, lk, workspace=1):
    """
    API to unlink KAM
    """
    if request.method == 'POST':

        lk = literal_eval(lk)
        user_id = lk[0]
        plan_id = lk[1]

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)
        db_name = 'data_' + db_name

        data = dict()
        data = kam.unlinkUserFromPlan(db_name, user_id=user_id, plan_id=plan_id, local=False)
        response = json.dumps(data, sort_keys=True)
        status = 200
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def unlinkPlanFromAction(request, lk, workspace=1):
    """
    API to unlink Plan Action
    """
    if request.method == 'POST':

        lk = literal_eval(lk)
        plan_id = lk[0]
        task_id = lk[1]

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)
        db_name = 'data_' + db_name

        data = dict()
        data = plans.unlinkPlanFromAction(db_name, plan_id=plan_id, task_id=task_id, local=False)
        # data = json.dumps(data, sort_keys=True)

        response = 'true'
        status = 200
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def setPlan(request, plan, workspace=1):
    """
    API to update the Plan
    """
    if request.method == 'POST':
        plan = literal_eval(plan)

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        try:
            plan = plans.createPlan(
                "data_" + db_name, plan=plan,
                username=request.user.username
            )
            response = plan
            status = 200
        except Exception as e:
            response = traceback.format_exc()
            status = 500
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def getPlans(request, account='all', workspace=1):
    """
    function: API request for get plan
    return: json response of get plans data
    """

    if request.method == 'GET':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        _user = request.user.configuration.account_type
        if _user != 'admin':
            _user = request.user.username

        try:
            get_plans_data = plans.getPlans(
                dbname=db_name, account=account, group_id=-1,
                user_id=0, username=_user
            )
            response = json.dumps(get_plans_data)
            status = 200
        except (NameError,
                TypeError,
                KeyError,
                ValueError,
                AttributeError,
                IndexError) as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={'type': 'Login'}
            )
            response = json.dumps(
                {
                    "message": "Internal Server Error"
                }
            )
            status = 500
    else:
        response = json.dumps(
            {'message': 'Method Not Allowed'}
        )
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def get_plans(request, account='all', workspace=1):
    """
    API to get the plan data
    """
    if request.method == 'GET':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        _user = request.user.configuration.account_type
        if _user != 'admin':
            _user = request.user.username

        data = dict()
        data = plans.get_plans(
            dbname=db_name, account=account, group_id=-1,
            user_id=0, username=_user
        )
        response = json.dumps(data)
        status = 200

    else:
        response = ''
        status = 400

    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def modifyPlan(request, plan, workspace=1):
    """
    API to update the Plan
    """
    if request.method == 'POST':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        logger.debug(plan)
        plan = literal_eval(plan)
        data = plans.setPlan(dbname="data_" + db_name, plan=plan)
        response = json.dumps(data)
        status = 200
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def dropPlan(request, planid='', workspace=1):
    """
    API to delete the Plan record
    """
    try:
        planid = int(planid)
    except:
        data = 'false'

    if request.method == 'POST':

        try:
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            plans.dropPlan("data_" + db_name, \
                           planid=planid, \
                           )
            # data = json.dumps(planid)
            response = 'true'
            status = 200
        except:
            response = planid
            status = 500
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def pipelines(request, details=None, workspace=1):
    """
    API for pipelines
    """
    if request.method == 'GET':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        response = sales.pipelines()
        status = 200
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def insertKam(request, data='', workspace=1):
    """
    API to insert the Kam record
    """
    try:
        data = literal_eval(data)

        if request.method == 'POST':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            if 'name' not in data.keys():
                data = 'Name missing. Cannot insert unknown customer.'
                return HttpResponse(data, content_type="application/json")
            if 'description' not in data.keys():
                data['description'] = ''

            ans = kam.insertKam(dbname=db_name, kam=data)
            response = json.dumps(str(ans))
            status = 200
        else:
            response = ''
            status = 400
    except (
            NameError,
            TypeError,
            KeyError,
            ValueError,
            AttributeError,
            IndexError
    ) as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        response = 'Cannot insert data'
        status = 500
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def linkKamToCustomer(request, lk, workspace=1):
    """
    API link Kam to customer
    """
    if request.method == 'POST':

        try:
            lk = literal_eval(lk)
            user_id = lk[0]
            customer_id = lk[1]

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            db_name = 'data_' + db_name
            logging.debug(db_name)

            data = dict()
            data['Response'] = kam.linkUserToCustomer(
                db_name, user_id=user_id,
                customer_id=customer_id, local=False
            )
            # data = json.dumps(data, sort_keys=True)
            # str(data)
            # logger.debug(data)
            data['Status'] = 'Ok'

            response = json.dumps(data, sort_keys=True)
            status = 200
        except:
            response = "Could not link data"
            status = 500
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )


@ensure_csrf_cookie
def unlinkKamFromCustomer(request, lk, workspace=1):
    """
    API unlink Kam from customers
    """
    if request.method == 'POST':

        lk = literal_eval(lk)
        user_id = lk[0]
        customer_id = lk[1]

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)
        db_name = 'data_' + db_name

        data = dict()
        data = kam.unlinkUserFromCustomer(
            db_name, user_id=user_id,
            customer_id=customer_id, local=False
        )
        response = json.dumps(data, sort_keys=True)
        status = 200
    else:
        response = ''
        status = 400
    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )
