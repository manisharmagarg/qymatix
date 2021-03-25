#from django.conf.urls import patterns, re_path

from django.urls import path, re_path
from .views import token_new


urlpatterns = [
    path('gettoken', token_new, name='api_token_new'),
]


#urlpatterns = patterns('tokenapi.views',
    #re_path(r'^gettoken$', 'token_new', name='api_token'),
    ##url(r'^token/(?P<token>.{24})/(?P<user>\d+).json$', 'token', name='api_token'),
#)
