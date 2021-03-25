import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
#import db
import os
# from webapp.models import Activity
# from webapp.models import Contact
# from webapp.models import Configuration

from core.models import Activity
from core.models import Contact
from core.models import Configuration
from core.models import Currency

from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import authenticate

from django.http import Http404
#import logging

from ast import literal_eval

from django.contrib.auth.models import User
from core.models import *
import pdb
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import logging
import traceback

_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path,'../../..'))
_basepath = settings.BASE_DIR


logger = logging.getLogger('django.request')

class PageView(TemplateView):
    page_slug = None
    page_title = None
    page_lead = None
    page_nav = None

    def get_page_data(self):
        return {
            u"slug": self.page_slug,
            u"title": self.page_title,
            u"lead": self.page_lead,
            u"nav": self.page_nav,
            #u"base_url": u"/"
        }

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context[u'page'] = self.get_page_data()
        return context


class ApiDocUsersView(PageView):
    template_name = u"api/docs/users_api.html"
    page_slug = u"home"
    page_title = u"Qymatix API doc"

    def get(self, request, *args, **kwargs):

        context = {}

        return render(request, "api/docs/users_api.html", context )

apidoc_users_api = ApiDocUsersView.as_view()


#@ensure_csrf_cookie
def register_user(request):
    '''
    '''
    return Http404('Function not available')


@ensure_csrf_cookie
def getUserProfile(request, username='', workspace=0):
    '''
    '''
    #return Http404('Soon this function')
    if request.method == 'GET':
        #from django.contrib.auth.models import User
        #data = request.user.username
        data = request.user.email
        #u = User.objects.get(username=request.user.id)
        try:
            conf = Configuration.objects.create(user_id=request.user.id)
        except:
            pass
        try:
            activity = Activity.objects.create(user_id=request.user.id)
        except:
            pass
        try:
            contact = Contact.objects.create(user_id=request.user.id)
        except:
            pass
        try:
            avatar = Avatar.objects.create(user_id=request.user.id)
        except:
            avatar = None
        try:
            currency_obj = Group.objects.filter(user=request.user)
        except:
            currency_obj = None

        #logging.debug(request.user.configuration.language)
        #logging.debug(request.user.configuration.plan)
        #logging.debug(request.user.activity.lastUpload)
        #logging.debug(request.user.activity.lastFileUploaded)
        #logging.debug(request.user.contact.company)
        #logging.debug(request.user.contact.address)
        try:
            data = dict()
            data['language'] = request.user.configuration.language 
            data['plan'] = request.user.configuration.plan
            # data['comment'] = request.user.configuration.comment   ******* Fix Me******
            data['lastUpload'] = request.user.activity.lastUpload
            data['lastFileUploaded'] = request.user.activity.lastFileUploaded
            data['company'] = request.user.contact.company
            data['phone'] = request.user.contact.telephone
            data['address'] = request.user.contact.address
            data['postcode'] = request.user.contact.postcode
            data['city'] = request.user.contact.city
            data['country'] = request.user.contact.country
            data['vat'] = request.user.contact.vat
            data['email'] = request.user.email
            data['firstName'] = request.user.first_name
            data['lastName'] = request.user.last_name
            data["currency"] = currency_obj[0].currencies_name
            # if currency_obj:
            #     data["currency"] = currency_obj[0].currencies_name
            # else:
            #     data["group_status"] = "No Group found related to "\
            #                             "this '{}' username".format(
            #                                 request.user.username
            #                             )
            #     data["currency"] = "No Currency Found due to No group exist"

            try:
                if request.user.avatar.Avatar_image:
                    data['image'] = str(request.user.avatar.Avatar_image)
            except:
                pass

            data = json.dumps(data, ensure_ascii=False)
            response = HttpResponse(data, content_type="application/json")
            #response["Access-Control-Allow-Origin"] = "*"
            #response["Access-Control-Allow-Origin"] = "http://192.168.1.97:9000"
            #response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            #response["Access-Control-Max-Age"] = "1000"
            #response["Access-Control-Allow-Headers"] = "*"
            return response
            #return HttpResponse(data, content_type="application/json")
        except Exception as e:
            data = {
                "message": "We encountered an error while loading your data, please contact us.",
                "error_status": 500
            }
            data = json.dumps(data, ensure_ascii=False)
            response = HttpResponse(data, content_type="application/json")
            return response



@csrf_exempt
def getUserToken(request, username='', workspace=0):
    '''
    '''
    #return Http404('Soon this function')
#    if request.method == 'POST':
    if True:

        email = request.POST.get('username')
        password = request.POST.get('password')

        logger.info("{}".format(email), extra={'type': 'Login'})

        data = dict()

        response = ''

        try:
            if email and password:
                username = email.replace("@", "__")
                username = username.replace("-", "___")
                username = username.replace(".", "_")

                logger.info("{}".format(username), extra={'type': 'Login'})

                user = authenticate(username=username, password=password)
                logger.info("{}".format(user), extra={'type': 'Login'})

                conf = Configuration.objects.get(user_id=user.id)
                data['token'] = conf.token
                data['success'] = True

            logger.info("{}".format(conf.token), extra={'type': 'Login'})
            data = json.dumps(data)
            response = HttpResponse(data, content_type="application/json")

        except Exception as e:
            logger.info("{}".format(e), extra={'type': 'Login'})

        return response

@ensure_csrf_cookie
def setUserContactInfo(request, info, workspace=0):
    '''
    '''
    #return Http404('Soon this function')
    info = literal_eval(info)

    #if request.method == 'GET':
    if request.method == 'POST':

        try:
            contact = Contact.objects.create(user_id=request.user.id)
        except:
            pass
        try:
            images_info = AvatarImage.objects.all()
        except:
            images_info = None

        if not images_info:

            av_ = [
                        "images/avatar/avatar1.jpg", 
                        "images/avatar/avatar2.jpg", 
                        "images/avatar/avatar3.jpg", 
                        "images/avatar/avatar4.jpg", 
                        "images/avatar/avatar5.png", 
                        "images/avatar/avatar6.png"
            ]
            for im in av_:
                AvatarImage.objects.create(images=im)

        try:

            user = User.objects.get(id=request.user.id)
            if 'firstName' in info.keys():
                user.first_name = info['firstName']
            if 'lastName' in info.keys():
                user.last_name = info['lastName']
            user.save()

            contact = Contact.objects.get(user_id=request.user.id)
            if 'company' in info.keys():
                contact.company = info['company']
            if 'phone' in info.keys():
                contact.telephone = info['phone']
            if 'address' in info.keys():
                contact.address = info['address']
            if 'city' in info.keys():
                contact.city = info['city']
            if 'postcode' in info.keys():
                contact.postcode = info['postcode']
            if 'country' in info.keys():
                contact.country = info['country']
            if 'vat' in info.keys():
                contact.vat = info['vat']
            contact.save()

            if info.get('image'):
                img = 'images/avatar/' + info.get('image')
                av_img = AvatarImage.objects.get(images=img)
                try:
                    avatar = Avatar.objects.get(user=user)
                except:
                    avatar = None
                if avatar:
                    avatar.Avatar_image = av_img
                    avatar.save()
                else:
                    Avatar.objects.create(user=user, Avatar_image=av_img)

            data = dict()
            data['language'] = request.user.configuration.language 
            data['plan'] = request.user.configuration.plan
            # data['comment'] = request.user.configuration.comment  **** fix me *****
            data['lastUpload'] = request.user.activity.lastUpload
            data['lastFileUploaded'] = request.user.activity.lastFileUploaded
            data['company'] = request.user.contact.company
            data['phone'] = request.user.contact.telephone
            data['address'] = request.user.contact.address
            data['postcode'] = request.user.contact.postcode
            data['city'] = request.user.contact.city
            data['country'] = request.user.contact.country
            data['vat'] = request.user.contact.vat
            data['firstName'] = request.user.first_name
            data['lastName'] = request.user.last_name


            data = json.dumps(data)
        except Exception as e:
            data = str(traceback.format_exc())

        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def setUserActivityInfo(request, info, workspace=0):
    '''
    '''
    #return Http404('Soon this function')

    if request.method == 'POST':

        try:
            activity = Activity.objects.create(user_id=request.user.id)
        except:
            pass

        activity = Activity.objects.get(user_id=request.user.id)
        activity.lastUpload = info['lastUpload']
        activity.lastFileUploaded = info['lastFileUploaded']
        activity.save()

        data = dict()
        data['language'] = request.user.configuration.language 
        data['plan'] = request.user.configuration.plan
        # data['comment'] = request.user.configuration.comment   **** fix me *****
        data['lastUpload'] = request.user.activity.lastUpload
        data['lastFileUploaded'] = request.user.activity.lastFileUploaded
        data['company'] = request.user.contact.company
        data['phone'] = request.user.contact.telephone
        data['address'] = request.user.contact.address
        data['postcode'] = request.user.contact.postcode
        data['city'] = request.user.contact.city
        data['country'] = request.user.contact.country
        data['vat'] = request.user.contact.vat

        data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def setUserConfigInfo(request, language='en', workspace=0):
    '''
    '''
    #return Http404('Soon this function')

    if request.method == 'POST':

        try:
            config = Configuration.objects.create(user_id=request.user.id)
        except:
            pass

        config = Configuration.objects.get(user_id=request.user.id)
        config.language = language
        #config.plan = plan
        config.save()

        data = dict()
        data['language'] = request.user.configuration.language 
        data['plan'] = request.user.configuration.plan
        # data['comment'] = request.user.configuration.comment   **** fix me *****
        data['lastUpload'] = request.user.activity.lastUpload
        data['lastFileUploaded'] = request.user.activity.lastFileUploaded
        data['company'] = request.user.contact.company
        data['phone'] = request.user.contact.telephone
        data['address'] = request.user.contact.address
        data['postcode'] = request.user.contact.postcode
        data['city'] = request.user.contact.city
        data['country'] = request.user.contact.country
        data['vat'] = request.user.contact.vat

        data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")

import base64
@ensure_csrf_cookie
def setavatarImages(request, language='en', workspace=0):
    if request.method == 'GET':
        images = AvatarImage.objects.all()
        my_avatar = list()
        for img in images:
            item = dict()
            print(img.images)
            path = 'media/' + str(img.images)
            with open(path, 'rb') as bites:
                item['avatar'] = base64.b64encode(img.images.read())
                item['path'] = img.images
                my_avatar.append(item)
        print(my_avatar)
        data = json.dumps(str(my_avatar))
        return HttpResponse(data, content_type="application/json")


@ensure_csrf_cookie
def change_password(request, password_info, workspace=0):
    password_info = literal_eval(password_info)

    if request.method == 'POST':
        try:
            username = request.user.username
            password = password_info.get('password')
            confirm_password = password_info.get('confirm_password')

            if password != confirm_password:
                data = {
                    "message": "Password does not match",
                    "error_status": 1

                }
                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
            if User.objects.filter(username=username).exists():
                user_ = User.objects.get(username=username)
                user_.set_password(password)
                user_.save()
                data = {
                    "message": "Password Changed Succssfully",
                    "error_status": 0
                }

                data = json.dumps(data)
                return HttpResponse(data, content_type="application/json")
        except Exception as e:
                logger.error("message {}, error {}".format(
                        e, 
                        traceback.format_exc()
                    ), 
                    extra={
                        'type': 'Login'
                    }
                )
