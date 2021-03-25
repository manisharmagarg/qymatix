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
from core.models import CustomerIndustries
import traceback
from django.contrib.auth.models import Group
import pandas as pd

logger = logging.getLogger(__name__)

_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path, '../../..'))
_basepath = settings.BASE_DIR,


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
def get_industry(request, workspace=1):
    """
    """
    response = dict()

    try:
        industry_data = literal_eval(data)
    except:
        industry_data = None
        industry_list = list()
    if request.method == 'GET':
        try:
            industry_obj = Group.objects.filter(user=request.user)
            if industry_obj:
                response["success"] = True
                response["customer_industries"] = eval(industry_obj[0].industries_name)
                response["username"] = request.user.username
                response["group_name"] = industry_obj[0].name
            else:
                response["message"] = "No group found related "\
                                        "to '{}' username".format(
                                                request.user.username
                                            )
                response["customer_industries"] = "No Industries Found due to No group exist"
                response["success"] = False
        except Exception as e:
            response["success"] = False
            response["message"] = e
            response["error"] = "{}".format(traceback.format_exc())
        resp = json.dumps(response)
        return HttpResponse(resp, content_type="application/json")


def industries(request):
    response = dict()
    try:
        industry_obj = Group.objects.filter(user=request.user)
        return eval(industry_obj[0].industries_name)
    except Exception as e:
        response['customer_industries'] = None
    return response
