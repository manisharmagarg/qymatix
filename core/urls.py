from django.urls import path, re_path

from tokenapi.decorators import token_required
from .views import authentication
from .views import healthcheck
from .views import login
from .views import logout
from .views import main
from .views import register
from .views import users
from .views import validate
from .views import recover_password

# csrf_exempt
TOKEN_URL = r'^(?P<user>\d+):(?P<token>[-\w\d-]+)/(?P<workspace>\d+)/'

urlpatterns = [
    path(
        'healthcheck',
        healthcheck.HealthCheckView.as_view(),
        name='login'
    ),
    path(
        'v1.0/login',
        login.LoginView.as_view(),
        name='login'
    ),
    path(
        'v1.0/logout',
        logout.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'v1.0/token',
        register.RegisterView.as_view(),
        name='register'
    ),
    path(
        'v1.0/register',
        register.register_view,
        name='register'
    ),
    path(
        'v1.0/recover_password_validation',
        recover_password.validate_password_recovery,
        name='validate-password-recovery'
    ),
    path(
        'v1.0/generate_new_password',
        recover_password.generate_new_password,
        name='generate-new-password'
    ),
    path(
        'v1.0',
        main.MainView.as_view(),
        name='main'
    ),
    path(
        'v1.0/auth',
        authentication.AuthenticationView.as_view(),
        name='auth'
    ),
    re_path(
        TOKEN_URL + r'v1.0/users/config',
        token_required(users.config),
        name='users_config'
    ),
    re_path(
        TOKEN_URL + r'v1.0/register/validate',
        token_required(validate.get),
        name='validate_register'
    ),
]
