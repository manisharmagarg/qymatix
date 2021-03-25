from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from functools import wraps


def token_required(view_func):
    """Decorator which ensures the user has provided a correct user and token pair."""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, user, token, *args, **kwargs):
        #user = None
        #token = None
        basic_auth = request.META.get('HTTP_AUTHORIZATION')

        #user = request.POST.get('user', request.GET.get('user'))
        #token = request.POST.get('token', request.GET.get('token'))


        if not (user and token) and basic_auth:
            auth_method, auth_string = basic_auth.split(' ', 1)

            if auth_method.lower() == 'basic':
                auth_string = auth_string.strip().decode('base64')
                user, token = auth_string.split(':', 1)

        if not (user and token):
            return HttpResponseForbidden("Must include 'user' and 'token' parameters with request.")

        user = authenticate(request, pk=user, token=token)
        if user:
            login(request, user)
            #return view_func(request, *args, **kwargs)
            response = view_func(request, *args, **kwargs)
            logout(request)
            return response

        return HttpResponseForbidden()
    return _wrapped_view


def token_required_v1(view_func):
    """Decorator which ensures the user has provided a correct user and token pair."""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        basic_auth = request.META.get('HTTP_AUTHORIZATION')


        #TODO: Fix this workaround to make tests work
        try:
            user, token = request.headers['api-token'].split(':')
        except:
            #For tests
            user, token = request.META.get('api-token').split(':')


        if not (user and token) and basic_auth:
            dd
            auth_method, auth_string = basic_auth.split(' ', 1)

            if auth_method.lower() == 'basic':
                auth_string = auth_string.strip().decode('base64')
                user, token = auth_string.split(':', 1)

        if not (user and token):
            return HttpResponseForbidden("Must include 'user' and 'token' parameters with request.")

        user = authenticate(request, pk=user, token=token)
        if user:
            login(request, user)
            response = view_func(request, *args, **kwargs)
            logout(request)
            return response

        return HttpResponseForbidden()
    return _wrapped_view
