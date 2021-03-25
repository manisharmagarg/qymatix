from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from ..models import Activity
from ..models import Configuration
from ..models import Contact
import os
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import logging


logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class MainView(View):


    def get(self, request):
        context = {}
        return render(request, "main/index.html", context)
