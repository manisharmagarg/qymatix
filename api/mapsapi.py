from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
import os
from api.qymatix.analytics.maps import customers

from django.views.generic import TemplateView
from django.shortcuts import render

#from ast import literal_eval
import logging


logger = logging.getLogger(__name__)


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


class ApiDocMapsView(PageView):
    template_name = u"api/docs/maps_api.html"
    page_slug = u"home"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):
        
        context = {}

        return render(request, "api/docs/maps_api.html", context )


apidoc_actions_api = ApiDocMapsView.as_view()



@ensure_csrf_cookie
def getCustomers(request, account='all', workspace=1, *args, **kwargs):

    if request.method == 'GET':

        workspace = int(workspace)
        data = customers.get_customers()

        return HttpResponse(data, content_type="application/json")

    else:
        pass


@ensure_csrf_cookie
def getAllocation(request, details):

    if request.method == 'GET':

        year = details

        data = customers.get_allocation(year=year)

        return HttpResponse(data, content_type="application/json")

    else:
        pass


