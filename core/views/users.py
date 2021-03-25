from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def config(request):
    return HttpResponse("Config Users view.")



