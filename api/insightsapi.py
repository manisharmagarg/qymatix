import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from api.qymatix import extras_results as results
from api.qymatix.analytics import extras_insights as extras_insights
from api.qymatix.analytics import new_insights as newInsights
from api.qymatix import insights
from api.qymatix import util
from api.qymatix import analysis
from api.qymatix import products
import os
import logging
from django.shortcuts import render
from django.http import Http404
from ast import literal_eval
from django.conf import settings


logger = logging.getLogger(__name__)

_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path,'../../..'))
_basepath = settings.BASE_DIR,


@ensure_csrf_cookie
def getAllInsights(request, account='all', workspace=1, *args, **kwargs):
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
            data = dict()
            data = extras_insights.getInsights(username=db_name, account=account, local=False)

            data['critters'] = results.getResults(username=db_name, account=account)
            #data['CCBM'] = getResultsRoadmap(username=db_name, func="CCBM")
            #data['CCPM'] = getResultsRoadmap(username=db_name, func="CCPM")
            data['CCBM'] = []
            data['CCPM'] = []

            customers  = results.getCustomers(username=db_name, account=account)
            data['critters']['city'] = range(len(customers['customer']))
            data['critters']['country'] = range(len(customers['customer']))
            for i in range(len(customers['customer'])):
            #for c in customers['customers']:
                try:
                    ix = data['critters']['name'].index(customers['customer'][i])
                    data['critters']['city'][ix] = customers['city'][i]
                    data['critters']['country'][ix] = customers['country'][i]
                except:
                    pass

            data = json.dumps(data, sort_keys=True)

        except:
            data = "{}"
            #raise

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getInsights(request, account='all', workspace=1, *args, **kwargs):
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
            data = dict()
            #data = insights.getInsights(username=db_name, account=account, local=False)

            _user = request.user.configuration.account_type
            if _user != 'admin':
                _user = request.user.username

            print(_user)

            #if 'masip' in _user:
                #_user = 'admin'
            #if 'pedretti' in _user:
                #_user = 'admin'

            data = newInsights.getInsights(dbname=db_name, account=account, local=False, dbusername='webuser', passwd='Qymatix!!!', username=_user)
            data = json.dumps(data)
        except Exception as e:
            import traceback
            data = '[]'
            #raise
            data= traceback.format_exc()
        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def get_insights(request, account='all', workspace=1, *args, **kwargs):
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
            data = dict()
            # import pdb
            # pdb.set_trace()
            _user = request.user.configuration.account_type
            if _user != 'admin':
                _user = request.user.username


            if request.user.configuration.plan == 'crm':
                data = insights.get_insights_crm(dbname=db_name, account=account, local=False, dbusername='webuser', passwd='Qymatix!!!', username=_user, user=request.user.username)
            else:
                data = insights.get_insights(dbname=db_name, account=account, local=False, dbusername='webuser', passwd='Qymatix!!!', username=_user, user=request.user.username)
                # data = json.dumps(data, sort_keys=True, encoding='latin-1')
                # data['pipelines'])
                data['pipelines'] = round(data['pipelines'], 4)
                data['pipelines'] = float(data['pipelines'])
                data['pipelines'] = str(data['pipelines'])
                data['pipelines2'] = str(data['pipelines'])


            data = json.dumps(data).encode('utf8')
        except Exception as e:
            import traceback
            data = {
                "message": e,
                "error": traceback.format_exc()
            }
            raise
            data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")

    else:
        pass

@ensure_csrf_cookie
def getInsightsPerCustomer(request, account='', workspace=1):
    '''
    '''
    #if request.is_ajax():
    if request.method == 'GET':
        
        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        data = dict()
        #data['actions'] = dbTasks.getTasks(dbname="data_" + db_name)
        #data = dbTasks.getPlans(dbname="data_" + db_name)
        data = extras_insights.getInsightsPerCustomer(username=db_name, local=False, account=account)
        data = json.dumps(data, sort_keys=True)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getCustomerRisk(request, account='', workspace=1):
    '''
    '''
    if request.method == 'GET':
        
        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        #data = dict()
        data = analysis.customer_risk(username=db_name, groupby='customer_id', local=False, account=account)
        data = json.dumps(data, sort_keys=True)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


def getProductRisk(request, account='', workspace=1):
    '''
    '''
    if request.method == 'GET':
        
        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        #data = dict()
        data = analysis.product_risk(username=db_name, groupby='name', local=False, account=account)
        data = json.dumps(data, sort_keys=True)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


def getProductTypeRisk(request, account='', workspace=1):
    '''
    '''
    if request.method == 'GET':
        
        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        #data = dict()
        data = analysis.product_type_risk(username=db_name, groupby='product_type', local=False, account=account)
        data = json.dumps(data, sort_keys=True)

        return HttpResponse(data, content_type="application/json")

    else:
        pass



@ensure_csrf_cookie
def getCustomerRiskByCustomer(request, account='', workspace=1):
    '''
    '''
    if request.method == 'GET':
        
        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        #data = dict()
        # data = qymatix.analysis.customer_at_risk(username=db_name, groupby='customer_id', local=False, account=account)
        data = analysis.customer_at_risk(username=db_name, groupby='customer_id', local=False, account=account)
        data = json.dumps(data, sort_keys=True)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getCrossSellingProducts(request, account='all', workspace=1, *args, **kwargs):
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
            data = products.getCrossSellingItems(dbname=db_name, item='products', account=account, local=False)
            # data = json.dumps(data, sort_keys=True, encoding='latin-1')
            data = json.dumps(data, sort_keys=True)
        except:
            data = {}
            raise

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getCrossSellingProductTypes(request, account='all', workspace=1, *args, **kwargs):
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
            data = products.getCrossSellingItems(dbname=db_name, item='product_type', account=account, local=False)
            # data = json.dumps(data, sort_keys=True, encoding='latin-1')
            data = json.dumps(data, sort_keys=True)
        except:
            data = {}
            raise

        return HttpResponse(data, content_type="application/json")

    else:
        pass


