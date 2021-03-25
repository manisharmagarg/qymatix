import json
import logging
import os
from ast import literal_eval

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

from api.qymatix import contacts
from api.qymatix import results
from api.qymatix import util
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
            # u"base_url": u"/"
        }

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context[u'page'] = self.get_page_data()
        return context


class ApiDocView(PageView):
    template_name = u"api/docs/index.html"
    page_slug = u"home"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, "api/docs/index.html", context)


apidoc_index = ApiDocView.as_view()


class ApiDocSearchView(PageView):
    template_name = u"api/docs/search.html"
    page_slug = u"search"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, "api/docs/search.html", context)


apidoc_search = ApiDocSearchView.as_view()


class ApiDocGenindexView(PageView):
    template_name = u"api/docs/genindex.html"
    page_slug = u"search"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, "api/docs/genindex.html", context)


apidoc_genindex = ApiDocGenindexView.as_view()


class ApiDocIntroductionView(PageView):
    template_name = u"api/docs/introduction.html"
    page_slug = u"search"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, "api/docs/introduction.html", context)


apidoc_introduction = ApiDocIntroductionView.as_view()


class ApiContactFunctionsView(PageView):
    template_name = u"api/docs/contact_functions.html"
    page_slug = u"home"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, "api/docs/contact_functions.html", context)


apidoc_contact_functions = ApiContactFunctionsView.as_view()


@ensure_csrf_cookie
def insertContact(request, data='', workspace=1):
    '''
    '''
    try:
        data = literal_eval(data)

        # if request.method == 'GET':
        if request.method == 'POST':

            logger.debug(data)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            db_name = util.getDatabaseName(_basepath, username)

            ans = contacts.insertContact(data, db_name)
            data = {
                "message": "Contact Inserted Successfully",
                "contact_id": str(ans)
            }

            data = json.dumps(data)
            return HttpResponse(data, content_type="application/json")
    # except:
    except Exception as e:
        import sys
        print(sys.exc_info()[0])
        print(e.args)
        logger.error("message {}, error {}".format(e, traceback.format_exc()), extra={'type': 'Login'})
        return HttpResponse(data, content_type="application/json")



@ensure_csrf_cookie
def modifyContact(request, data, workspace=1):
    '''
    '''

    # if request.method == 'GET':
    if request.method == 'POST':

        try:
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            db_name = util.getDatabaseName(_basepath, username)

            contact = literal_eval(data)
            data = contacts.setContact(db_name, data=contact)
            data = json.dumps(data)

        except Exception as e:
            print(e)
            data = e

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def deleteContact(request, data='', workspace=1):
    '''
    '''
    try:
        contact_id = int(data)
    except:
        data = 'false'

    if request.method == 'POST':
        # if request.method == 'GET':
        try:
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            db_name = util.getDatabaseName(_basepath, username)

            # qymatix.kam.dropKam("data_" + db_name,\
            # user_id=kamid,\
            # )
            # data = json.dumps(planid)
            data = contacts.deleteContact(db_name, contact_id)
            # data = 'true'
        except Exception as e:
            print(e)
            data = contact_id

        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def _deleteContact(request, data, workspace=1):
    '''
    '''

    # if request.method == 'GET':
    if request.method == 'POST':

        try:
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            db_name = util.getDatabaseName(_basepath, username)

            contact = literal_eval(data)
            contact = int(data)

            data = contacts.deleteContact(db_name, data=contact)
            data = json.dumps(data)

        except Exception as e:
            print(e)
            data = e

        return HttpResponse(data, content_type="application/json")

    else:
        pass


# @ensure_csrf_cookie
def getContactsData(request, account='all', workspace=1, *args, **kwargs):
    '''
    '''
    if request.method == 'GET':
        try:
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            db_name = util.getDatabaseName(_basepath, username)

            data = dict()
            data['critters'] = results.getResults(username=db_name, account=account)
            # data['CCBM'] = getResultsRoadmap(username=db_name, func="CCBM")
            # data['CCPM'] = getResultsRoadmap(username=db_name, func="CCPM")
            data['CCBM'] = []
            data['CCPM'] = []

            contacts_list = contacts.getContacts(dbname=db_name, account=account, username=_user)
            if contacts_list != []:
                data['critters']['city'] = str(range(len(contacts_list['contact'])))
                data['critters']['country'] = str(range(len(contacts_list['contact'])))
                for i in range(len(contacts_list['contact'])):
                    # for c in contacts['contacts']:
                    try:
                        ix = data['critters']['name'].index(contacts_list['contact'][i])
                        data['critters']['city'][ix] = contacts_list['city'][i]
                        data['critters']['country'][ix] = contacts_list['country'][i]
                    except:
                        pass

            _data = json.dumps(data).encode('utf8')

        except Exception as e:
            print(e)
            # data = "{a}"
            _data = traceback.format_exc()

        return HttpResponse(_data, content_type="application/json")


@ensure_csrf_cookie
def getContactsList(request, account='all', workspace=1):
    '''
    '''
    # if request.is_ajax():
    if request.method == 'GET':

        try:
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            db_name = util.getDatabaseName(_basepath, username)

            _user = request.user.configuration.account_type
            if _user != 'admin':
                _user = request.user.username

            data = dict()
            data['contacts'] = contacts.getContactsList(dbname=db_name, account=account, username=_user)
            data = json.dumps(data)
        except:
            data = "{}"

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getContacts(request, account='all', workspace=1):
    '''
    '''

    # if request.is_ajax():
    if request.method == 'GET':

        try:
            # if 'name' in request.POST:
            # name = request.POST['name']
            # account = request.POST['name']
            # else:
            ##name = None
            # account = 'all'

            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            db_name = util.getDatabaseName(_basepath, username)

            _user = request.user.configuration.account_type
            if _user != 'admin':
                _user = request.user.username

            data = dict()
            data = contacts.getContacts(dbname=db_name, account=account, username=_user)
            data = json.dumps(data)

        except:
            data = "{}"

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getContactsByCustomer(request, account='all', workspace=1):
    '''
    '''

    if request.method == 'GET':

        try:
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            db_name = util.getDatabaseName(_basepath, username)
            # print(account)

            _user = request.user.configuration.account_type
            if _user != 'admin':
                _user = request.user.username

            data = dict()
            # data['contacts'] = results.getContacts(username=db_name, name=name)
            data = contacts.getContactsByCustomer(db_name, account=account, username=_user)
            data = json.dumps(data)

        except Exception as e:
            print(e)
            data = "{}"
            data = str(traceback.format_exc())

        return HttpResponse(data, content_type="application/json")

    else:
        pass
