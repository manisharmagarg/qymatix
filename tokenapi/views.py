from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

try:
    from django.contrib.auth import get_user_model
except ImportError: # Django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from .tokens import token_generator
from .http import json_response, json_error, json_response_forbidden, \
    json_response_unauthorized
import logging


django_logger = logging.getLogger('django.request')

# Creates a token if the correct username and password is given
# token/new.json
# Required: username&password
# Returns: success&token&user


@csrf_exempt
def token_new(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        if email and password:
            #username = email.split("@")[0]
            username = email.replace("@", "__")
            username = username.replace(".", "_")
            username = username.replace("-", "___")

            try:
                user = User.objects.get(username=username)
            except:
                user = None
                return json_error("Invalid username or password.")

            if user.check_password(password):
                if user.is_active:
                    data = {
                        'token': "{}:{}".format(
                            user.pk, 
                            token_generator.make_token(user)
                        ),
                    }
                    return json_response(data)
                else:
                    return json_error("User is no longer active, please "\
                        "contact us"
                    )
            else:
                return json_error("Invalid username or password.")
        else:
            return json_error("Must include 'username' and 'password' as "\
                "POST parameters.")
    else:
        return json_error("Must access via a POST request.")


def token_(username, password):

    if username and password:
        #username = email.replace("@", "__")
        #username = username.replace(".", "_").replace("-", "___")

        user = authenticate(username=username, password=password)

        if user:
            TOKEN_CHECK_ACTIVE_USER = getattr(
                settings, 
                "TOKEN_CHECK_ACTIVE_USER", 
                False
            )

            if TOKEN_CHECK_ACTIVE_USER and not user.is_active:
                return json_response_forbidden("User account is disabled.")

            data = {
                "token": "{}:{}".format(
                            user.pk, token_generator.make_token(user)
                        ),
            }

            return json_response(data)
        else:
            return json_response_unauthorized(
                "Unable to log you in, please try again."
            )
    else:
        return json_error(
            "Must include 'username' and 'password' as POST parameters."
        )


def token_free(user):

    if user:
        TOKEN_CHECK_ACTIVE_USER = getattr(
            settings, 
            "TOKEN_CHECK_ACTIVE_USER", 
            False
        )

        if TOKEN_CHECK_ACTIVE_USER and not user.is_active:
            return json_response_forbidden("User account is disabled.")

        #data = {
            #'token': token_generator.make_token(user),
            #'user': user.pk,
        #}
        data = {
            'token': str(user.pk) + ":" + token_generator.make_token(user),
        }

        return json_response(data)
    else:
        return json_response_unauthorized(
            "Unable to log you in, please try again."
        )


# Checks if a given token and user pair is valid
# token/:token/:user.json
# Required: user
# Returns: success
def token(request, token, user):
    try:
        user = User.objects.get(pk=user)
    except User.DoesNotExist:
        return json_error("User does not exist.")

    TOKEN_CHECK_ACTIVE_USER = getattr(
        settings, 
        "TOKEN_CHECK_ACTIVE_USER", 
        False
    )

    if TOKEN_CHECK_ACTIVE_USER and not user.is_active:
        return json_error("User account is disabled.")

    if token_generator.check_token(user, token):
        return json_response({})
    else:
        return json_error("Token did not match user.")
