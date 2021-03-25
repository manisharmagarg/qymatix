from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib import auth
import logging


logger = logging.getLogger('django.request')


class AuthenticationView(View):

    def post(self, request, username=None, password=None):
        if username is None:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

        logger.info("User {} attemps to log in...".format(username), extra={'type': 'Login'})

        user_name = username.replace("@", "__")
        user_name = user_name.replace('.', '_').replace("-", "___")
        user = auth.authenticate(username=user_name, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            logger.info("User {} logged in".format(user), extra={'type': 'Login'})
            return HttpResponseRedirect('/webapp/v1.0')

        else:
            return HttpResponseRedirect('/webapp/v1.0/login')
