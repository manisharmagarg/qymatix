import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from api.qymatix import util
from api.qymatix import customers
from api.qymatix import results
import os
import logging
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import Http404
from ast import literal_eval
from django.conf import settings
import os
from tokenapi.http import *
import traceback

logger = logging.getLogger('django.request')

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


class ApiDocView(PageView):
    template_name = u"api/docs/index.html"
    page_slug = u"home"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):

        context = dict()

        return render(request, "api/docs/index.html", context )

apidoc_index = ApiDocView.as_view()


class ApiDocSearchView(PageView):
    template_name = u"api/docs/search.html"
    page_slug = u"search"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):

        context = dict()

        return render(request, "api/docs/search.html", context )

apidoc_search = ApiDocSearchView.as_view()


class ApiDocGenindexView(PageView):
    template_name = u"api/docs/genindex.html"
    page_slug = u"search"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):

        context = dict()

        return render(request, "api/docs/genindex.html", context )

apidoc_genindex = ApiDocGenindexView.as_view()


class ApiDocIntroductionView(PageView):
    template_name = u"api/docs/introduction.html"
    page_slug = u"search"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):

        context = {}

        return render(request, "api/docs/introduction.html", context )

apidoc_introduction = ApiDocIntroductionView.as_view()


class ApiCustomerFunctionsView(PageView):
    template_name = u"api/docs/customer_functions.html"
    page_slug = u"home"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):

        context = {}

        return render(request, "api/docs/customer_functions.html", context )

apidoc_customer_functions = ApiCustomerFunctionsView.as_view()



@ensure_csrf_cookie
def insertCustomer(request, data='', workspace=1):
    '''
    '''
    try:
        #if request.method == 'GET':
        if request.method == 'POST':
            data = literal_eval(data)
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            ans = customers.insertCustomer(data, db_name)
            data = {
                'customer_id': str(ans)
            }
            return json_response(data)
            # return HttpResponse(data, content_type="application/json")
    #except:
    except Exception as e:
        import sys
        logger.error("{}".format(sys.exc_info()[0]), extra={'type': 'Login'})
        logger.error("{}".format(e.args), extra={'type': 'Login'})
        data = 'Cannot insert data'
        data = str(traceback.format_exc())
        return HttpResponse(data, content_type="application/json")
        #return HttpResponse(data, content_type="application/json")
        raise


@ensure_csrf_cookie
def modifyCustomer(request, data, workspace=1):
    '''
    '''
    #if request.method == 'GET':
    if request.method == 'POST':

        try:
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            customer = literal_eval(data)
            data = customers.setCustomer(db_name, data=customer)
            data = json.dumps(data)

        except Exception as e:
            logger.error("{}".format(e), extra={'type': 'Login'})
            data = e

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def deleteCustomer(request, data='', workspace=1):
    try:
        customer_id = literal_eval(data)
        customer_id = int(customer_id)
    except:
        data = 'false'

    if request.method == 'POST':
        try:
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split(
                    '@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            data = customers.deleteCustomer(db_name, customer_id)
            data = json.dumps(data)
            return HttpResponse(data, content_type="application/json")
        except Exception as e:
            logger.error("{}".format(e), extra={'type': 'Login'})
            data = json.dumps(
                {
                    "msg": "Internal Server Error"
                }
            )
            return HttpResponse(
                data,
                content_type="application/json",
                status=500
            )


@ensure_csrf_cookie
def _deleteCustomer(request, data, workspace=1):
    '''
    '''

    #if request.method == 'GET':
    if request.method == 'POST':

        try:
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            customer = literal_eval(data)
            customer = int(data)

            data = customers.deleteCustomer(db_name, data=customer)
            data = json.dumps(data)

        except Exception as e:
            print(e)
            data = e

        return HttpResponse(data, content_type="application/json")

    else:
        pass



@ensure_csrf_cookie
def getCustomersData(request, account='all', workspace=1, *args, **kwargs):
    '''
    '''
    if request.method == 'GET':
        try:
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)


            _user = request.user.configuration.account_type
            if _user != 'admin':
                _user = request.user.username

            #if 'masip' in _user:
                #_user = 'admin'
            #if 'pedretti' in _user:
                #_user = 'admin'


            data = dict()
            data['critters'] = results.getResults(dbname=db_name, account=account, username=_user)
            #data['CCBM'] = getResultsRoadmap(username=db_name, func="CCBM")
            #data['CCPM'] = getResultsRoadmap(username=db_name, func="CCPM")
            data['CCBM'] = []
            data['CCPM'] = []

            customers  = results.getCustomers(dbname=db_name, account=account, username=_user)
            if customers != []:
                data['critters']['city'] = '' #str(range(len(customers['customer'])))
                data['critters']['country'] = '' #str(range(len(customers['customer'])))
                print('I am here', data)
                # for i in range(len(customers['customer'])):
                # #for c in customers['customers']:
                #     try:
                #         ix = data['critters']['name'].index(customers['customer'][i])
                #         data['critters']['city'][ix] = customers['city'][i]
                #         data['critters']['country'][ix] = customers['country'][i]
                #     except:
                #         pass

            # _data = json.dumps(data, encoding='latin-1')
            _data = json.dumps(data).encode('utf8')

        except Exception as e:
            print(e)
            # import traceback
            # _data = {
            #     "message": e,
            #     "error": traceback.format_exc()
            # }
            #data = "{a}"
            # _data = traceback.format_exc()
            _data = {}
            raise

        return HttpResponse(_data, content_type="application/json")


@ensure_csrf_cookie
def getCustomersList(request, workspace=1):
    '''
    '''
    #if request.is_ajax():
    if request.method == 'GET':

        try:
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

            data['customers'] = results.getCustomersList(dbname=db_name, username=_user)

            data = json.dumps(data)
        except:
            data = "{}"

        return HttpResponse(data, content_type="application/json")
    else:
        pass


@ensure_csrf_cookie
def getCustomers(request, account='all', workspace=1):
    '''
    '''
    #if request.is_ajax():
    if request.method == 'GET':
        try:
            if 'name' in request.POST:
                name = request.POST['name']
                account = request.POST['name']
            else:
                name = None
                account = 'all'

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
            # data['customers'] = results.getCustomers(username=db_name, name=name)
            data = results.getCustomers(dbname=db_name, account=account, username=_user)
            if not data:
                data = {
                    "message": "No data found",
                    "data": data
                }
            data = json.dumps(data)
        except Exception as e:
            data = {
                "message": e,
                "error": traceback.format_exc()
            }
            # raise
            data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")

    else:
        pass

@ensure_csrf_cookie
def get_customers(request, account='all', workspace=1):
    '''
    '''

    #if request.is_ajax():
    if request.method == 'GET':

        try:
            #if 'name' in request.POST:
                #name = request.POST['name']
                #account = request.POST['name']
            #else:
                ##name = None
                #account = 'all'

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            _user = request.user.configuration.account_type
            plan = request.user.configuration.plan
            if _user != 'admin':
                _user = request.user.username

            #data = dict()
            #data['customers'] = results.getCustomers(username=db_name, name=name)
            if plan == 'crm':
                data = results.get_customers_crm(dbname=db_name, account=account, username=_user)
            else:
                data = results.get_customers(dbname=db_name, account=account, username=_user)

            data = json.dumps(data)
        except Exception as e:
            data = "{}"
            raise

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def get_group_customers(request, account='all', workspace=1):
    '''
    '''

    #if request.is_ajax():
    if request.method == 'GET':

        try:
            #if 'name' in request.POST:
                #name = request.POST['name']
                #account = request.POST['name']
            #else:
                ##name = None
                #account = 'all'

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            _user = request.user.configuration.account_type
            plan = request.user.configuration.plan
            if _user != 'admin':
                _user = request.user.username

            data = results.get_group_customers(dbname=db_name, account=account, username=_user)
            # if plan == 'crm':
            #     data = results.get_customers_crm(dbname=db_name, account=account, username=_user)
            # else:
            #     data = results.get_group_customers(dbname=db_name, account=account, username=_user)

            data = json.dumps(data)
        except Exception as e:
            data = "{}"
            raise

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getlinkedcustomers(request, account='all', workspace=1):
    '''
    '''
    #if request.is_ajax():
    if request.method == 'GET':
        try:
            # if 'name' in request.POST:
            #     name = request.POST['name']
            #     account = request.POST['name']
            # else:
            #     name = None
            #     account = 'all'

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
            # data['customers'] = results.getCustomers(username=db_name, name=name)
            data = results.get_linked_customer(dbname=db_name, account=account, username=_user)
            data = json.dumps(data)
        except:
            data = "{}"
            raise

        return HttpResponse(data, content_type="application/json")

    else:
        pass

"""
from django.views import View
class GetParentCustomers(View):

    def get(self, request, *args, **kwargs):
        workspace = kwargs.get("workspace")
        account = kwargs.get("customer_id")
        if not account:
            account = 'all'
        return HttpResponse(kwargs, content_type="application/json")
        try:
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
                db_name = util.getDatabaseName(_basepath, username)
            _user = request.user.configuration.account_type
            if _user != 'admin':
                _user = request.user.username
            data = results.get_parent_customer(dbname=db_name, account=account, username=_user)
            data = json.dumps(data)
            return HttpResponse(data, content_type="application/json")
        except Exception as e:
            import traceback
            return (traceback.format_exc())
"""

@ensure_csrf_cookie
def getparentcustomers(request, account='all', workspace=1):
    if request.method == 'GET':
        try:
            # if 'name' in request.POST:
            #     name = request.POST['name']
            #     account = request.POST['name']
            # else:
            #     name = None
            #     account = 'all'

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
            # data['customers'] = results.getCustomers(username=db_name, name=name)
            data = results.get_parent_customer(dbname=db_name, account=account, username=_user)
            data = json.dumps(data)
        except:
            data = "{}"
            raise

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def get_sales_per_customer(request, account='all', workspace=1):
    raw_data = literal_eval(account)

    if request.method == 'GET':
        try:
            #if 'name' in request.POST:
                #name = request.POST['name']
                #account = request.POST['name']
            #else:
                ##name = None
                #account = 'all'

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            _user = request.user.configuration.account_type
            plan = request.user.configuration.plan
            if _user != 'admin':
                _user = request.user.username

            #data = dict()
            data = results.get_sales_per_customer(dbname=db_name, account=raw_data, username=_user)

            data = json.dumps(data)
        except Exception as e:
            data = "{}"
            raise
        return HttpResponse(data, content_type="application/json")

    else:
        pass



def add_linked_customer(request, account='all', workspace=1):
    raw_data = literal_eval(account)

    if request.method == 'POST':
        try:
            #if 'name' in request.POST:
                #name = request.POST['name']
                #account = request.POST['name']
            #else:
                ##name = None
                #account = 'all'

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            _user = request.user.configuration.account_type
            plan = request.user.configuration.plan
            if _user != 'admin':
                _user = request.user.username

            #data = dict()
            data = results.add_linked_customer(dbname=db_name, account=raw_data, username=_user)

            data = json.dumps(data)
        except Exception as e:
            data = "{}"
            raise
        return HttpResponse(data, content_type="application/json")

    else:
        pass

def remove_linked_customer(request, account='all', workspace=1):
    raw_data = literal_eval(account)

    if request.method == 'GET':
        try:
            #if 'name' in request.POST:
                #name = request.POST['name']
                #account = request.POST['name']
            #else:
                ##name = None
                #account = 'all'

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            _user = request.user.configuration.account_type
            plan = request.user.configuration.plan
            if _user != 'admin':
                _user = request.user.username

            #data = dict()
            data = results.remove_linked_customer(dbname=db_name, account=raw_data, username=_user)

            data = json.dumps(data)
        except Exception as e:
            data = "{}"
            raise
        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def customer_by_products(request, account='all', workspace=1):
    raw_data = literal_eval(account)

    if request.method == 'GET':
        try:
            #if 'name' in request.POST:
                #name = request.POST['name']
                #account = request.POST['name']
            #else:
                ##name = None
                #account = 'all'

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            _user = request.user.configuration.account_type
            plan = request.user.configuration.plan
            if _user != 'admin':
                _user = request.user.username

            data = results.customer_by_products(dbname=db_name, account=raw_data, username=_user)
            data = json.dumps(data)
        except Exception as e:
            data = "{}"
            raise
        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def customer_by_product_types(request, account='all', workspace=1):
    raw_data = literal_eval(account)

    if request.method == 'GET':
        try:
            #if 'name' in request.POST:
                #name = request.POST['name']
                #account = request.POST['name']
            #else:
                ##name = None
                #account = 'all'

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            _user = request.user.configuration.account_type
            plan = request.user.configuration.plan
            if _user != 'admin':
                _user = request.user.username

            data = results.customer_by_product_types(dbname=db_name, account=raw_data, username=_user)
            data = json.dumps(data)
        except Exception as e:
            data = "{}"
            raise
        return HttpResponse(data, content_type="application/json")

    else:
        pass
