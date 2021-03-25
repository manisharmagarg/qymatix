from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
import os
import json

from django.views.generic import TemplateView
from django.shortcuts import render

from ast import literal_eval
import logging

from api.qymatix.analytics import performance
from api.qymatix.analytics.performance_analytics import goals
from api.qymatix.analytics.performance_analytics import get_total_performance
# import qymatix.util
# import qymatix.kam
from api.qymatix import util
from api.qymatix import kam
from django.conf import settings
import pandas as pd
import traceback
import uuid 
from api.models import Reports

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


class ApiDocGoalsView(PageView):
    template_name = u"api/docs/goals_api.html"
    page_slug = u"home"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):
        
        context = {}

        return render(request, "api/docs/goals_api.html", context )

apidoc_goals_api = ApiDocGoalsView.as_view()


@ensure_csrf_cookie
def createGoal(request, data, workspace=1):

    try:
        goal = literal_eval(data)

        #if request.method == 'GET':
        if request.method == 'POST':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            
            goal['username'] = username

            goal_id = goals.createGoal(db_name,\
                        goal
                        )

            goal['id'] = str(goal_id)
            data = json.dumps(goal['id'])

            return HttpResponse(data, content_type="application/json")
    except:
        
        data = 'Cannot create goal.'
        #return HttpResponse(data, content_type="application/json")
        raise


@ensure_csrf_cookie
def modifyGoal(request, data, workspace=1):

    #if request.method == 'GET':
    if request.method == 'POST':
        
        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        db_name = util.getDatabaseName(_basepath, username)

        goal = literal_eval(data)
        data = goals.modifyGoal(db_name, data=goal)
        data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getGoals(request, data={}, workspace=1):
    '''
    '''

    try:

        try:
            data = literal_eval(data)
        except:
            data = {}

        if request.method == 'GET':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            kam = goals.getGoals(db_name,\
                        data\
                        )

            data = json.dumps(kam)

            return HttpResponse(data, content_type="application/json")
    except:
        
        raise
        #data = 'Cannot retrieve KAM'
        #return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def getGoalsByYear(request, data={}, workspace=1):
    '''
    '''

    try:
        try:
            data = literal_eval(data)
        except:
            data = {}

        if request.method == 'GET':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            kam = goals.getGoals(db_name,\
                        data,\
                        groupedby='year'\
                        )

            data = json.dumps(kam)

            return HttpResponse(data, content_type="application/json")
    except:
        
        #raise
        #data = 'Cannot retrieve KAM'
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def getGoalsPerQuarter(request, data={}, workspace=1):
    '''
    '''

    try:

        try:
            data = literal_eval(data)
        except:
            data = {}


        if request.method == 'GET':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            kam = goals.getGoalsPerQuarter(db_name,\
                        data\
                        )

            data = json.dumps(kam)

            return HttpResponse(data, content_type="application/json")
    except:
        
        raise
        #data = 'Cannot retrieve KAM'
        #return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def getTotalPerformance(request, data='all', workspace=1):

    try:

        try:
            user_id = literal_eval(data)
        except:
            user_id = 'all'

        if request.method == 'GET':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            results = get_total_performance.get_total_performance(db_name,\
                        )

            data = json.dumps(results)

            return HttpResponse(data, content_type="application/json")
    except:
        
        raise
        #data = 'Cannot retrieve KAM'
        #return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def getPerformance(request, data='all', workspace=1):

    try:

        try:
            user_id = literal_eval(data)
        except:
            user_id = 'all'

        if request.method == 'GET':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            results = kam.getPerformance(db_name,\
                        )

            data = json.dumps(results)

            return HttpResponse(data, content_type="application/json")
    except:
        
        raise
        #data = 'Cannot retrieve KAM'
        #return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def getPerformanceKpi(request, data='all', workspace=1):

    try:
        #if data == '':
            #kam = 'all'
        #else:
            ##kam = data
            #kam = literal_eval(data)

        try:
            user_id = literal_eval(data)
        except:
            user_id = 'all'

        if request.method == 'GET':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            results = kam.getPerformanceKpi(db_name,\
                        )

            data = json.dumps(results)

            return HttpResponse(data, content_type="application/json")
    except:
        
        raise
        #data = 'Cannot retrieve KAM'
        #return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def getPerformanceCRM(request, data='all', workspace=1):

    try:
        #if data == '':
            #kam = 'all'
        #else:
            ##kam = data
            #kam = literal_eval(data)

        try:
            user_id = literal_eval(data)
        except:
            user_id = 'all'

        if request.method == 'GET':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            results = performance.getPerformanceCRM(db_name, account=data)

            data = json.dumps(results)

            return HttpResponse(data, content_type="application/json")
    except:
        
        raise
        #data = 'Cannot retrieve Performance'
        #return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def get_performance_crm(request, data='all', workspace=1):

    try:
        #if data == '':
            #kam = 'all'
        #else:
            ##kam = data
            #kam = literal_eval(data)

        try:
            user_id = literal_eval(data)
        except:
            user_id = 'all'

        if request.method == 'GET':

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            results = performance.get_performance_crm(db_name,\
                        account=data)

            data = json.dumps(results)

    except:
        
        data = {}
        #raise
        #data = 'Cannot retrieve Performance'
        #return HttpResponse(data, content_type="application/json")

    return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def get_performance_products(request, workspace=1):
    try:
        if request.method == 'GET':
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            product_type = performance.get_performance_products(db_name)
            if product_type:
                data = json.dumps(product_type)
                return HttpResponse(data, content_type="application/json")
            else:
                data = {
                    'message': 'null>>>>>',
                    'success': False
                }
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")

    except Exception as e:
        data = {
            'message': e,
            "error": traceback.format_exc()
        }
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def performance_search(request, data, workspace=1):
    data = literal_eval(data)
    try:
        if request.method == 'POST':
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            data = performance.performance_search_db(request, data, db_name)

            if data:
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            else:
                data = {
                    'message': 'null',
                    'success': False
                }
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
    except Exception as e:
        data = {
            'message': e,
            "error": traceback.format_exc()
        }
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def insertReport(request, data, workspace=1):
    report_data = literal_eval(data)

    """
    {
        'first_year': '2018', 'first_month': 7, 'first_product_type': 1, 'first_product': 5, 
        'second_year': '2018', 'second_month': 7, 'second_product_type': 2, 'second_product': 5, 
        'first_sales_data': [
            {'id': '7', 'account_name': 'MeghaTest', 'margin': '12.0', 'price': '1.0', 'cost': '1.0'}, 
            {'id': '8', 'account_name': 'MeghaTest', 'margin': '10.0', 'price': '12.0', 'cost': '23.0'}
        ], 
        'second_sales_data': [
                {'id': '7', 'account_name': 'MeghaTest', 'margin': '12.0', 'price': '1.0', 'cost': '1.0'}, 
                {'id': '8', 'account_name': 'MeghaTest', 'margin': '10.0', 'price': '12.0', 'cost': '23.0'}
        ]
    }
    """
    data = dict()
    if request.method == 'POST':
        try:
            # first_industry = report_data.get("first_industry")
            first_year = report_data.get("first_year")
            first_month = report_data.get("first_month")
            first_kam = report_data.get("first_kam")
            first_product_type = report_data.get("first_product_type")
            first_product = report_data.get("first_product")

            second_industry = report_data.get("second_industry")
            second_year = report_data.get("second_year")
            second_month = report_data.get("second_month")
            second_kam = report_data.get("second_kam")
            second_product_type = report_data.get("second_product_type")
            second_product = report_data.get("second_product")

            reportName = "Report" + "-" +"{}".format(uuid.uuid1())

            if report_data.get("first_industry") == "selected_all_industry":
                first_industry = report_data.get("first_industry")
            else:
                first_industry = json.dumps(report_data.get("first_industry"))

            if report_data.get("second_industry") == "selected_all_industry":
                second_industry = report_data.get("second_industry")
            else:
                second_industry = json.dumps(report_data.get("second_industry"))

            rep_obj = Reports.objects.create(
                    industory1 = first_industry,
                    year1 = first_year,
                    month1 = first_month,
                    kam1=first_kam,
                    product_type1 = first_product_type,
                    product1 = first_product,
                    industory2 = second_industry,
                    year2 = second_year,
                    month2 = second_month,
                    kam2=second_kam,
                    product_type2 = second_product_type,
                    product2 = second_product,
                    report_name = reportName
                )
            data["success"] = True
            data["id"] = "{}".format(rep_obj.id)
        except Exception as e:
            data["success"] = False
            data["message"] = e
            data["error"] = traceback.format_exc()
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def getReport(request, data, workspace=1):
    """
    {"reportName" : "Report-d479dfc4-d858-11e9-8c79-0242ac140007"}

    """
    response = dict()
    report_record = list()

    try:
        report_data = literal_eval(data)
    except:
        report_data = None

    if request.method == 'GET':
        try:
            if not report_data:
                report_obj = Reports.objects.all()
                for report in report_obj:
                    item = dict()
                    item["first_industry"] = report.industory1
                    item["report_id"] = report.id
                    item["first_year"] = report.year1
                    item["first_month"] = report.month1
                    item["first_kam"] = report.kam1
                    item["first_product_type"] = report.product_type1
                    item["first_product"] = report.product1

                    item["second_industry"] = report.industory2
                    item["second_year"] = report.year2
                    item["second_month"] = report.month2
                    item["second_kam"] = report.kam2
                    item["second_product_type"] = report.product_type2
                    item["second_product"] = report.product2
                    item["report_name"] = report.report_name
                    report_record.append(item)
            else:
                rep_name = report_data.get("reportName")
                # report_obj = Reports.objects.filter(report_name__in=rep_name)
                report_obj = Reports.objects.filter(report_name=rep_name)
                for report in report_obj:
                    item = dict()
                    item["first_industry"] = report.industory1
                    item["report_id"] = report.id
                    item["first_year"] = report.year1
                    item["first_month"] = report.month1
                    item["first_kam"] = report.kam1
                    item["first_product_type"] = report.product_type1
                    item["first_product"] = report.product1

                    item["second_industry"] = report.industory2
                    item["second_year"] = report.year2
                    item["second_month"] = report.month2
                    item["second_kam"] = report.kam2
                    item["second_product_type"] = report.product_type2
                    item["second_product"] = report.product2
                    item["report_name"] = report.report_name
                    report_record.append(item)

            response["success"] = True
            response["report"] = report_record
        except Exception as e:
            response["success"] = False
            response["message"] = e
            response["error"] = "{}".format(traceback.format_exc())
        resp = json.dumps(response)
        return HttpResponse(resp, content_type="application/json")


@ensure_csrf_cookie
def modifyReport(request, data, workspace=1):
    try:
        report_data = literal_eval(data)
        # return report_data
    except:
        report_data = None

    response = dict()
    report_id = report_data.get("report_id")

    first_industry = report_data.get("first_industry")
    first_year = report_data.get("first_year")
    first_month = report_data.get("first_month")
    first_product_type = report_data.get("first_product_type")
    first_product = report_data.get("first_product")

    second_industry = report_data.get("second_industry")
    second_year = report_data.get("second_year")
    second_month = report_data.get("second_month")
    second_product_type = report_data.get("second_product_type")
    second_product = report_data.get("second_product")

    report_name = report_data.get("reportName")
    try:
        report_obj = Reports.objects.get(report_name=report_name)
    except Exception as e:
        report_obj = None

    if report_obj:
        report_obj.industory1 = first_industry
        report_obj.year1 = first_year
        report_obj.month1 = first_month
        report_obj.product_type1 = first_product_type
        report_obj.product1 = first_product
        report_obj.industory2 = second_industry
        report_obj.year2 = second_year
        report_obj.month2 = second_month
        report_obj.product_type2 = second_product_type
        report_obj.product2 = second_product
        report_obj.save()
        response["status"] = True
        response["message"] = "Record Updated Successfully"
    else:
        response["status"] = False
        response["message"] = "Record Not Found"
    resp = json.dumps(response)
    return HttpResponse(resp, content_type="application/json")


@ensure_csrf_cookie
def dropReport(request, data, workspace=1):
    try:
        report_data = literal_eval(data)
    except:
        report_data = None
    response = dict()
    report_name = report_data.get("reportName")
    try:
        Reports.objects.filter(report_name=report_name).delete()
        response["status"] = True
        response["delete_report"] = report_name
    except Exception as e:
        response["status"] = False
        response["error"] = "{}".format(traceback.format_exc())
    resp = json.dumps(response)
    return HttpResponse(resp, content_type="application/json")


@ensure_csrf_cookie
def get_sales_year(request, workspace=1):
    try:
        if request.method == 'GET':
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            years_data = performance.get_sales_year(db_name)
            years_lst = list()
            for year in years_data:
                years_lst.append(int(year))

            if years_lst:
                record = {
                    'years': years_lst,
                    'success': True
                }
                data = json.dumps(record)
                return HttpResponse(data, content_type="application/json")
            else:
                data = {
                    'message': 'Record Not Found',
                    'success': False
                }
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")

    except Exception as e:
        data = {
            'message': e,
            "error": traceback.format_exc()
        }
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")

