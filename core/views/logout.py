from django.http import HttpResponseRedirect
from django.views import View
from django.contrib import auth


class LogoutView(View):

    def get(self, request):
        """
        """
        auth.logout(request)
        return HttpResponseRedirect('/webapp/v1.0/login')
