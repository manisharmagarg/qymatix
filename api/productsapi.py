"""
Script to deal with the products api's
"""
import logging
import math
# pylint: disable=broad-except
# pylint: disable=bare-except
# pylint: disable=inconsistent-return-statements
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=empty-docstring
# pylint: disable=unused-variable
# pylint: disable=unused-argument
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=redefined-argument-from-local
# pylint: disable=pointless-string-statement
# pylint: disable=too-many-locals
# pylint: disable=no-else-return
# pylint: disable=no-self-use
# pylint: disable=keyword-arg-before-vararg
# pylint: disable=super-with-arguments
import os
import traceback
from ast import literal_eval

from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

from api.insights.insights.infrastructure.mysql.mysql_connection import MySqlConnection
from api.insights.insights.infrastructure.mysql.read.kam import KamFinder
from .qymatix import products, util
from .qymatix.analytics.products_analytics.products import *

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


class ApiDocProductsView(PageView):
    """
    """
    template_name = u"api/docs/products_api.html"
    page_slug = u"home"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):
        """
        """
        context = {}
        return render(request, "api/docs/products_api.html", context)


apidoc_products_api = ApiDocProductsView.as_view()


@ensure_csrf_cookie
def insertProduct(request, data='', workspace=1):
    """
    API request to insert products
    """

    if request.method == 'POST':
        # if request.method == 'GET':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

        db_name = util.getDatabaseName(_basepath, username)

        _data = data.strip('{}').split(",")
        data = dict()
        for data_val in _data:
            key, val = data_val.split(":")
            data[key.strip('" ')] = str(val.strip('" '))

    try:
        products.insertProduct(data, db_name)
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")

    except:
        return Http404('function error')


@ensure_csrf_cookie
def insertProductType(request, data='', workspace=1):
    """
    API request to insert product Type
    """
    if request.method == 'POST':
        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

        db_name = util.getDatabaseName(_basepath, username)

        _data = data.strip('{}').split(",")
        data = dict()
        for data_val in _data:
            key, val = data_val.split(":")
            data[key.strip('" ')] = str(val.strip('" '))

    try:
        products.insertProductType(data, db_name)
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")

    except:
        return Http404('function error')


@ensure_csrf_cookie
def insertProductLine(request, data='', workspace=1):
    """
    API request to insert product line
    """
    if request.method == 'POST':
        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

        db_name = util.getDatabaseName(_basepath, username)

        _data = data.strip('{}').split(",")
        data = dict()
        for data_val in _data:
            key, val = data_val.split(":")
            data[key.strip('" ')] = str(val.strip('" '))

    try:
        products.insertProductLine(data, db_name)
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")

    except:
        return Http404('function error')


@ensure_csrf_cookie
def insertProductClass(request, data='', workspace=1):
    """
    API request to insert product class data
    """
    if request.method == 'POST':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

        db_name = util.getDatabaseName(_basepath, username)

        _data = data.strip('{}').split(",")
        data = dict()
        for data_val in _data:
            key, val = data_val.split(":")
            data[key.strip('" ')] = str(val.strip('" '))

    try:
        products.insertProductClass(data, db_name)
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")

    except:
        return Http404('function error')


@ensure_csrf_cookie
def deleteProduct(request, product=None, workspace=1):
    """
    API request to delete the product from database
    """
    try:
        prod_id = int(product)
    except:
        data = 'None'
        # raise

    try:
        if request.method == 'POST':
            # logger.debug(request.environ)
            # logger.debug(taskid)

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            dbname = util.getDatabaseName(_basepath, username)
            products.dropProduct(dbname=dbname, table='products', prod_id=prod_id)
            data = json.dumps(prod_id)

            return HttpResponse(data, content_type="application/json")
    except:
        data = 'None'
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def deleteProductType(request, product=None, workspace=1):
    """
    API request to delete the product type data
    """
    try:
        prod_id = int(product)
    except:
        data = 'None'
        # raise

    try:
        if request.method == 'POST':
            # logger.debug(request.environ)
            # logger.debug(taskid)

            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

            dbname = util.getDatabaseName(_basepath, username)
            products.dropProduct(dbname=dbname, table='product_type', prod_id=prod_id)
            data = json.dumps(prod_id)

            return HttpResponse(data, content_type="application/json")
    except:
        data = 'None'
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def topProducts(request, params=None, workspace=1, *args, **kwargs):
    """
    API request to get the top products details
    """

    if request.method == 'GET':
        if params is None:
            year = None
            account = 'all'
        else:
            params = literal_eval(params)
            if 'year' in params.keys():
                year = params['year']
            else:
                year = None
            if 'account' in params.keys():
                account = params['account']  # .encode('latin-1')
            else:
                account = 'all'

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        dbname = 'data_' + username
        # dbname = username

        data = top_products(dbname, year, account)
        return HttpResponse(data, content_type="application/json")

    else:
        # raise
        pass


@ensure_csrf_cookie
def getProducts(request, product='all', workspace=1, *args, **kwargs):
    """
    API request to get the products records from database
    """
    if request.method == 'GET':
        if product is None:
            year = None
            product = 'all'
        # else:
        # product = literal_eval(params)
        # if 'year' in params.keys():
        # year = params['year']
        # else:
        # year = None
        # if 'account' in params.keys():
        # account = params['account']
        # else:
        # account = 'all'

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        dbname = username
        data = products.getProducts(dbname, product=product)
        final_list = list()
        products_data = json.loads(data)

        for product in products_data:
            item = dict()
            item['id'] = product.get('id')
            item["name"] = product.get('name')
            item["description"] = product.get('description')
            item["product_type"] = product.get('product_type')
            item["product_type_id"] = product.get("product_type_id")
            final_list.append(item)
        number_of_pages = 0
        divide_result = len(final_list) / 20
        if math.modf(divide_result)[0] == 0.0:
            number_of_pages = math.modf(divide_result)[1]
        else:
            number_of_pages = math.modf(divide_result)[1] + 1
        offset = 0
        limit = 500
        offset = int(offset)
        final_res = final_list[offset:offset + limit]
        data = json.dumps(final_res)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
# def topProducts(request, year=None, account='all', *args, **kwargs):
def getProductsBy(request, groupby=None, workspace=1, *args, **kwargs):
    """
    API request to get the products lists
    """
    if request.method == 'GET':

        if groupby is None:
            year = None
            account = 'all'
            groupby = 'name'
            '''
        else:
            params = literal_eval(groupby)
            if 'year' in params.keys():
                year = params['year']
            else:
                year = None
            if 'account' in params.keys():
                account = params['account']
            else:
                account = 'all'
            '''

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        dbname = username

        data = products.getProductsList(dbname, groupby=groupby)
        data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getProductInsights(request, params=None, workspace=1, *args, **kwargs):
    """
    API request to get the products Insights records
    """
    if request.method == 'GET':

        if params is None:
            year = None
            account = 'all'
            # groupby = 'id'
        else:
            params = literal_eval(params)
            # if 'groupby' not in params.keys():
            # groupby = 'id'
            if 'year' in params.keys():
                year = params['year']
            else:
                year = None
            if 'account' in params.keys():
                account = params['account']
            else:
                account = 'all'

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        dbname = username

        data = products.getProductInsights(dbname, account=account, year=year)
        # data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def get_product_insights(request, params=None, workspace=1, *args, **kwargs):
    """
    API request to get products insights records
    """
    if request.method == 'GET':

        if params is None:
            year = None
            account = 'all'
            # groupby = 'id'
        else:
            params = literal_eval(params)
            # if 'groupby' not in params.keys():
            #     groupby = 'id'
            if 'year' in params.keys():
                year = params['year']
            else:
                year = None
            if 'account' in params.keys():
                account = params['account']
            else:
                account = 'all'

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        dbname = username

        data = products.get_product_insights(dbname, account=account, year=year)
        data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getProductTypeInsights(request, params=None, workspace=1, *args, **kwargs):
    """
    API request to get the products type insights records
    """
    if request.method == 'GET':

        if params is None:
            year = None
            account = 'all'
            groupby = 'id'
        else:
            params = literal_eval(params)
            if 'year' in params.keys():
                year = params['year']
            else:
                year = None
            if 'account' in params.keys():
                account = params['account']
            else:
                account = 'all'

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
        dbname = username

        data = products.getProductTypeInsights(dbname, account=account, year=year)
        # data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getProductsByType(request, data, workspace=1):
    """
    API request to get the products recorsa by products type
    """
    data = literal_eval(data)
    try:
        if request.method == 'POST':
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            data = products.products_by_type(data, db_name)

            if data:
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            else:
                data = {
                    'message': 'No data found',
                    'success': False
                }
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
    except Exception as exception:
        data = {
            'message': exception,
            "error": traceback.format_exc()
        }
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def getProductsByCustomer(request, data, workspace=1):
    """
    API request to get the products associated by particular customers
    """
    data = literal_eval(data)
    try:
        if request.method == 'GET':
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            data = products.products_by_customer(data, db_name)

            if data:
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            else:
                data = {
                    'message': 'No data found',
                    'success': False
                }
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
    except Exception as exception:
        data = {
            'message': exception,
            "error": traceback.format_exc()
        }
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def getMinMaxVal(request, data, workspace=1):
    """
    API request to get products minimum and maximum value
    """
    data = literal_eval(data)
    try:
        if request.method == 'GET':
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)
            data = products.getMinMaxVal(data, db_name)

            if data:
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            else:
                data = {
                    'message': 'No data found',
                    'success': False
                }
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
    except Exception as exception:
        data = {
            'message': exception,
            "error": traceback.format_exc()
        }
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def getSuggestedRange(request, data, workspace=1):
    """
    API request to get the product suggested range
    """
    data = literal_eval(data)
    try:
        if request.method == 'GET':
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            # kam = get_kams(request)
            kam = None

            data_ = products.getSuggestedRange(data, db_name, kam)

            if data_[0]['minval'] and data_[0]['maxval']:

                if data.get('ppb') == 0:
                    factor_min = 1.02
                    factor_max = 1.08

                if data.get('ppb') == 1:
                    factor_min = 1.04
                    factor_max = 1.07

                if data.get('ppb') == 2:
                    factor_min = 1.00
                    factor_max = 1.06

                risk_corrector = (1.15 - 0.95) * ((data.get('srisk') - 0.2) / (0.95)) + 0.95

                factor_min = risk_corrector * factor_min
                factor_max = risk_corrector * factor_max

                sales_corrector = (1.10 - 0.95) * ((data.get('ssales') - 0.01) / (0.95)) + 0.95

                factor_min = sales_corrector * factor_min
                factor_max = sales_corrector * factor_max
                factor_min = 1000 * factor_min
                factor_max = 1000 * factor_max


                data = {
                    "suggested_min_val": factor_min * data_[0]['minval'],
                    "suggested_max_val": factor_max * data_[0]["maxval"]
                }

                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            else:
                data = {
                    'message': 'No data found',
                    'success': False
                }
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
    except Exception as exception:
        data = {
            'message': exception,
            "error": traceback.format_exc()
        }
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")


def get_kams(request):
    group_name = request.user.groups.all()[0]

    data_db = "data_{}".format(group_name)
    db_connection = MySqlConnection(data_db)
    session = db_connection.session()

    kam = None
    if request.user.configuration.account_type == 'basic':
        limit_to_user = request.user.username
        kam_finder = KamFinder(session)
        kam = kam_finder.get_kam_by_name(limit_to_user)
        # group_finder = GroupFinder(session)
        # groups = group_finder.get_group_by_owner(kam.id)
        # kam = [user.id for user in group.users for group in groups]
        kam = [kam]

    return kam
