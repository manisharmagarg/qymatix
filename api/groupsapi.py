from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from api.qymatix import util
from api.qymatix import kam
from api.qymatix import actions
from api.qymatix import plans
from api.qymatix import groups
import os
import json

from django.views.generic import TemplateView
from django.shortcuts import render

from ast import literal_eval
import logging
from django.conf import settings
import traceback


logger = logging.getLogger(__name__)

_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path,'../../..'))
_basepath = settings.BASE_DIR


class PageView(TemplateView):
    page_slug = None
    page_title = None
    page_lead = None
    page_nav = None

    def get_page_data(self):
        return {
            u"slug": self.page_slug,
            u"title": self.page_title,
            u"lead": self.page_lead,
            u"nav": self.page_nav,
            #u"base_url": u"/"
        }

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context[u'page'] = self.get_page_data()
        return context


class ApiDocActionsView(PageView):
    template_name = u"api/docs/groups_api.html"
    page_slug = u"home"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):
        
        context = {}

        return render(request, "api/docs/groups_api.html", context )

apidoc_actions_api = ApiDocActionsView.as_view()


@ensure_csrf_cookie
def createGroup(request, group, workspace=1):
    '''
    '''
    try:
        group = literal_eval(group)

        if request.method == 'POST':
            workspace = int(workspace)
            if 'workspace' == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
                db_name = util.getDatabaseName(_basepath, username)

            
            if 'name' not in group.keys():
                data = 'You have to provide at least a name for the new group'
                return HttpResponse(data, content_type="application/json")
 
            if 'description' not in group.keys():
                group['description'] = ''
            if 'owner_id' not in group.keys():
                group['owner_id'] = 0

            group_id = groups.createGroup(
                        db_name,\
                        group=group,\
                        username=request.user.username\
                        )

            logging.info(group_id)
            data = json.dumps(group_id)

            return HttpResponse(data, content_type="application/json")

    except Exception as e:
        print(e)
        data = 'Cannot create group'
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def deleteGroup(request, group_id=None, workspace=1):
    '''
    '''
    try:
        groupid = int(group_id)
    except:
        data = 'None'

    try:
        if request.method == 'POST':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            db_name = util.getDatabaseName(_basepath, username)

            groups.deleteGroup(db_name,\
                        groupid=groupid,\
                        )
            
            data = json.dumps(groupid)

            return HttpResponse(data, content_type="application/json")
    except:
        data = 'None'
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def modifyGroup(request, group, workspace=1):
    '''
    '''
    if request.method == 'POST':

        group = literal_eval(group)

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

        db_name = util.getDatabaseName(_basepath, username)

        data = groups.modifyGroup(dbname=db_name, group=group)
        data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def addUserToGroup(request, lk, workspace=1):
    '''
    '''
    if request.method == 'POST':
        
        try:
            lk = literal_eval(lk)
            user_id = lk[0]
            group_id = lk[1]
            
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            data = dict()
            data['Response'] = groups.addUserToGroup(db_name, user_id, group_id, local=False)
            data['Status'] = 'Ok'

            data = json.dumps(data, sort_keys=True)
        except:
            data = "Could not add user to group"

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def removeUserFromGroup(request, lk, workspace=1):
    '''
    '''
    if request.method == 'POST':

        lk = literal_eval(lk)
        user_id = lk[0]
        group_id = lk[1]
        
        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        data = dict()
        data = groups.removeUserFromGroup(db_name, user_id, group_id, local=False)

        data = 'true'
        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getGroups(request, user_id=0, workspace=1, *args, **kwargs):
    '''
    '''

    workspace = int(workspace)

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

        data = groups.getGroups(dbname=db_name, user=request.user.username, username=_user, user_id=user_id)
        data = dict(data)
        data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")
    else:
        pass


@ensure_csrf_cookie
def getUsersPerGroup(request, user_name='all', workspace=1, *args, **kwargs):
    '''
    '''
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


        data = groups.getUsersPerGroup(dbname=db_name, user=user_name, username=_user)
        data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getGroupsPerUser(request, user_name='all', user_id=0, workspace=1, *args, **kwargs):
    '''
    '''
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

        data = groups.getGroupsPerUser(dbname=db_name, user=user_name, username=_user, user_id=user_id)
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")
    else:
        pass
