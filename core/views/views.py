from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='v1.0/login')
def index(request):
    return HttpResponse("Hello, world. You're at the Core index.")



