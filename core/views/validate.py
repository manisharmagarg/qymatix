from django.contrib.auth.models import User
import logging
from django.http import HttpResponseRedirect
from .config_user import ConfigUser


django_logger = logging.getLogger('django.request')


def get(request, *args, **kwargs):

    user = User.objects.get(id=request.user.id)

    user.is_active = True
    user.save()

    config_user = ConfigUser(user)
    config_user.setup_user()

    return HttpResponseRedirect('/webapp/v1.0/login')
