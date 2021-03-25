from django.views import View
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template.context_processors import csrf
import json
from ..models import Activity
from ..models import Configuration
from ..models import Contact
from ..forms import MyRegistrationForm
from django.core.mail import send_mail

from tokenapi.views import token_, token_free
import logging
from django.contrib.auth import authenticate
from .config_user import ConfigUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.conf import settings
from tokenapi.http import json_response, json_error, json_response_forbidden, json_response_unauthorized


django_logger = logging.getLogger('django.request')


class RegisterView(View):

    def get(self, request, *args, **kwargs):
        form = MyRegistrationForm()
        args = {}
        args.update(csrf(request))
        # args['alert'] = True
        args['form'] = form
        return render_to_response('authentication/register.html', args)

    def post(self, *args, **kwargs):
        form = MyRegistrationForm(request.POST)

        if form.is_valid():
            try:
                user = form.save()
            except Exception as e:
                django_logger.error(e)

                form = MyRegistrationForm()
                args = {}
                args.update(csrf(request))
                args['form'] = form
                # args['alert'] = True
                args.update(e.args[0])

                return render_to_response('authentication/register.html', args)

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['username']

            username = email.replace("@", "__")
            username = username.replace(".", "_").replace("-", "___")

            user.set_password(form.cleaned_data['password1'])
            user.save()

            #user = authenticate(request, username=username, password=form.cleaned_data['password1'])

            config_user = ConfigUser(user)
            config_user.generate_token(form.cleaned_data['password1'])

            fullname = first_name.title() + " " + last_name.title()

            try:
                link = 'https://localhost:9443/webapp/{}/1/v1.0/register/validate'.format(
                    config_user.get_token())
                self.send_validation_email(email, username, link, fullname)
            except Exception as e:
                django_logger.error("Error sending validation e-mail to user {}".format(fullname),
                                    extra={'Exception': e}
                                    )

            user.is_active = False
            user.save()

            c = {}
            return render(request, 'authentication/waiting-validation.html', c)

        else:
            form = MyRegistrationForm()
            args = {}
            args.update(csrf(request))
            args['form'] = form
            args['alert'] = True
            # args.update(e.args[0])

            return render_to_response('authentication/register.html', args)

    def send_validation_email(self, email, username, link, fullname=""):
        ''' 
        '''
        userName = username
        userName = userName.replace("___", "-")
        userName = userName.replace('__', '@')
        userName = userName.replace('_', '.')

        # userName = userName.replace('_', '@').title()
        email_subject = 'Welcome to Qymatix {}'.format(fullname)
        email_body = "Welcome {}!\n\nThanks for having registered in our service. You can now login and start saving time and money, while growing your sales. Qymatix is easy to use: connect, click, understand.\
        \n\n\nIf you want to know how Qymatix can make your life easier, please visit our online support:\
        \nhttps://qymatix.de/en/predictive-sales-analytics-qymatix-welcome/\n\
        \nIf you want to give us feedback or need help please fill this formulary:\
        \nhttps://qymatix.de/en/qymatix-support-contact-en/\n\
        \n\nBest Regards,\n\nQymatix team.\n\
        \n\nClick in the link below to validate your account:\n\n\n{}".format(fullname, link)

        try:
            send_mail(email_subject,
                      email_body,
                      'webmaster@qymatix.com',
                      # [email])
                      # ['martin.masip@qymatix.de'])
                      ['martinmasip@gmail.com'])
        except Exception as e:
            django_logger.error("Exception", extra={
                                'Exception': e, 'Link': link})

        try:
            send_mail("New user registered",
                      "{}\n\n{}\n\n{}".format(fullname, email, email_body),
                      'webmaster@qymatix.com',
                      # ['lucas.pedretti@qymatix.de', 'martin.masip@qymatix.de'])
                      ['martin.masip@qymatix.de'])
        except Exception as e:
            django_logger.error("Exception", extra={'Exception': e})


@csrf_exempt
def register_view(request):
    email = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    password = request.POST.get('password')
    username = email.replace("@", "__")
    username = username.replace(".", "_").replace("-", "___")

    domain_name = email.split('@')[1]
    try:
        if not (domain_name == "gmail.com" or domain_name == "yahoo.com" or domain_name == "hotmail.com"):
            if email and password:

                """ 
                try: 
                    link = 'https://localhost:9443/webapp/{}/1/v1.0/register/validate'.format(config_user.get_token()) 
                    self.send_validation_email(email, username, link, fullname) 
                except Exception as e: 
                    django_logger.error( 
                        "Error sending validation e-mail to user {}".format( 
                            fullname 
                        ), 
                        extra={'Exception': e} 
                    ) 

                """
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.set_password(password)
                user.save()
                config_user = ConfigUser(user)
                config_user.generate_token(password)
                config_user.create_group()
                fullname = first_name.title() + " " + last_name.title()

                try:
                    link = "https://localhost:9443/webapp/{}/1/v1.0/register/validate".format(
                        config_user.get_token()
                    )

                    # send_validation_email(
                    #     email,
                    #     username,
                    #     link,
                    #     fullname
                    # )
                except Exception as e:
                    django_logger.error(
                        "Error sending validation e-mail to user {}".format(
                            fullname
                        ),
                        extra={'Exception': e}
                    )

                data = {
                    'success': True,
                    "message": 'User Register Successfully'
                }
            else:
                data = {
                    'success': False
                }
        else:
            data = {
                "success": False,
                "message": "Only Business Emails are Allowed"
            }
        data = json.dumps(data)
        return HttpResponse(data, content_type="application/json")
    except Exception as e:
        data = {
            "message": "Inter Server Error"
        }
        return HttpResponse(data, content_type="application/json", status=500)


def send_validation_email(email, username, link, fullname=""):
    ''' 
    '''
    userName = username
    userName = userName.replace("___", "-")
    userName = userName.replace('__', '@')
    userName = userName.replace('_', '.')

    # userName = userName.replace('_', '@').title()
    email_subject = 'Welcome to Qymatix {}'.format(fullname)

    email_body = "Welcome {}!\n\nThanks for having registered in our service. You can now login and start saving time and money, while growing your sales. Qymatix is easy to use: connect, click, understand.\
        \n\n\nIf you want to know how Qymatix can make your life easier, please visit our online support:\
        \nhttps://qymatix.de/en/predictive-sales-analytics-qymatix-welcome/\n\
        \nIf you want to give us feedback or need help please fill this formulary:\
        \nhttps://qymatix.de/en/qymatix-support-contact-en/\n\
        \n\nBest Regards,\n\nQymatix team.\n\
        \n\nClick in the link below to validate your account:\n\n\n{}".format(fullname, link)

    try:
        send_mail(
            email_subject,
            email_body,
            'webmaster@qymatix.com',
            ['martinmasip@gmail.com']
        )
    except Exception as e:
        django_logger.error(
            "Exception",
            extra={
                'Exception': e,
                'Link': link
            }
        )

    try:
        send_mail(
            "New user registered",
            "{}\n\n{}\n\n{}".format(
                fullname,
                email,
                email_body
            ),
            'webmaster@qymatix.com',
            ['martinmasip@gmail.com']
        )
    except Exception as e:
        django_logger.error("Exception", extra={'Exception': e})
        django_logger.error("Exception", extra={'Exception': e})
