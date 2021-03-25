"""
Script to recover the user password
"""
# pylint: disable=import-error
# pylint: disable=too-many-format-args
# pylint: disable=unused-argument
import os
import json
import logging
import traceback
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


@csrf_exempt
def validate_password_recovery(request):
    """
    User validate password and recover
    """
    email = request.POST.get('email')
    data = dict()
    if User.objects.filter(email=email).exists():
        user_ = User.objects.get(email=email)
        fullname = user_.get_full_name()
        username = user_.username
        try:
            link = os.getenv('WEBAPP_LINK') + "/generate_new_password"\
                "?email={}".format(user_.email)
            send_mail_status = send_password_recovery_validation_email(
                user_.email,
                username,
                link,
                fullname
            )
            if send_mail_status:
                data["message"] = "Login into you email and " \
                                  "change your password"

            else:
                data["message"] = "Email is not send Successfully"
                data = json.dumps(data)
                return HttpResponse(
                    data,
                    content_type="application/json",
                    status=500
                )
        except (
                NameError,
                TypeError,
                KeyError,
                ValueError,
                AttributeError,
                IndexError
        ) as exception:
            logger.error(
                "message %s, error %s",
                exception,
                traceback.format_exc(),
                extra={
                    'type': 'Login'
                }
            )
            data["message"] = "Internal Server Error"
            data = json.dumps(data)
            return HttpResponse(
                data,
                content_type="application/json",
                status=500
            )
    else:
        data["message"] = "User doesn't exists"

    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")


def send_password_recovery_validation_email(email, username, link, fullname):
    """
    function: send the email to user to recover their password
    """
    email_subject = 'Qymatix - You have requested a new password.'.format(
        fullname
    )

    email_body = "Hi {fullname}!\n\nYou have requested a password change. "\
        "If you didn't, ignore this E-Mail.\n\n"\
        "If you want to change your password click on the "\
        "following link. After you click on the link you will "\
        "receive an email with the new password."\
        "\n\nLink: {link} "\
        "\n\n\nIf you want to know how Qymatix can make your life "\
        "easier, please visit our online support: "\
        "\nhttps://qymatix.de/en/predictive-sales-analytics-"\
        "qymatix-welcome/\n\nIf you want to give us "\
        "feedback or need help please fill this "\
        "formulary:\nhttps://qymatix.de/en/qymatix-support-"\
        "contact-en/\n\n\n"\
        "Best Regards,\n\n Qymatix team.\n\n\n".format(
            fullname=fullname,
            link=link
        )
    try:
        send_mail(
            email_subject,
            email_body,
            os.getenv('HOST_MAIL'),
            [email]
        )
        logger.info("Email Sent Successfully", extra={'type': 'Login'})
        return True
    except (
            NameError,
            TypeError,
            KeyError,
            ValueError,
            AttributeError,
            IndexError
    ) as exception:
        logger.error(
            "message %s, error %s",
            exception,
            traceback.format_exc(),
            extra={
                'type': 'Login'
            }
        )
        return False


@csrf_exempt
def generate_new_password(request):
    """function: Generate new password"""
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    data = dict()
    if password == confirm_password:
        if User.objects.filter(email=email).exists():
            user_ = User.objects.get(email=email)
            user_.set_password(password)
            user_.save()
            data["message"] = "Password changed Successfully"
            data["status_code"] = 200
        else:
            data["message"] = "User doesn't exists"
            data["status_code"] = 201
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")
    else:
        data["message"] = "Password do not Match"
        data["status_code"] = 202
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")
