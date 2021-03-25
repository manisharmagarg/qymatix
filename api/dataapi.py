import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
from webapp.models import Activity
from webapp.models import Contact
from webapp.models import Configuration

from django.views.generic import TemplateView
from django.shortcuts import render
from webapp.extras import dbTools
from webapp.extras import dbTasks


from django.http import Http404
#import logging


_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path,'../../..'))
_basepath = '/home/webuser'



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

@ensure_csrf_cookie
def getUserProfile(request, username=''):
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

        #logging.debug(request.user.configuration.language)
        #logging.debug(request.user.configuration.plan)
        #logging.debug(request.user.activity.lastUpload)
        #logging.debug(request.user.activity.lastFileUploaded)
        #logging.debug(request.user.contact.company)
        #logging.debug(request.user.contact.address)
        data = dict()
        data['language'] = request.user.configuration.language 
        data['plan'] = request.user.configuration.plan
        data['comment'] = request.user.configuration.comment
        data['lastUpload'] = request.user.activity.lastUpload
        data['lastFileUploaded'] = request.user.activity.lastFileUploaded
        data['company'] = request.user.contact.company
        data['phone'] = request.user.contact.telephone
        data['address'] = request.user.contact.address
        data['postcode'] = request.user.contact.postcode
        data['city'] = request.user.contact.city
        data['country'] = request.user.contact.country

        data = json.dumps(data)

        response = HttpResponse(data, content_type="application/json")
        #response["Access-Control-Allow-Origin"] = "http://192.168.1.97:9000"
        #response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        #response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
        #return HttpResponse(data, content_type="application/json")


@csrf_exempt
def upload(request, *args, **kwargs):

    #if request.method == 'POST' and request.is_ajax():
    if request.method == 'POST':

        if request.FILES['file']:
            f = request.FILES['file']
            files = f
            print(f)

            #data_dir = '/home/martin/Downloads'
            ##name = f._name + str(random.randint(1, 1000000))
            #name = f._name
            #with open(os.path.join(data_dir, name), 'wb+') as destination:
                #for chunk in f.chunks():
                    #destination.write(chunk)

            db_name = handle_uploaded_file(request.user, f)

            ''''
            if db_name == None:
                #messages.error = (request,"Error")
                #messages.add_message(request.REQUEST.get('next', '/webapp'), messages.ERROR, 'Hello world.')
                response["Access-Control-Allow-Headers"] = "*"
                return HttpResponse(request.REQUEST.get('next', '/webapp')) 
            else:
                return HttpResponse(request.REQUEST.get('next', '/webapp')) 
            '''

            data = dict()
            data['country'] = request.user.contact.country
            data = json.dumps(data)


            response = HttpResponse(data, content_type="application/json")
            #response["Access-Control-Allow-Origin"] = "http://192.168.1.97:9000"
            #response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            #response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "*"
            return response

    else:
        return render(request, 'webapp/my_drop_upload.html')
        #return render(request, 'webapp/creatures.html')


def handle_uploaded_file(user, f):
    #HOME_DIR = '/home/webuser/users/' + username
    HOME_DIR = os.path.join(_basepath, 'users', user.username)
    DATA_DIR = os.path.join(HOME_DIR, 'data')

    _filename = os.path.join(DATA_DIR, f._name)
    
    filename = _filename

    ##shutil.rmtree(DATA_DIR)
    #try:
    #import glob
    #filelist = glob.glob(os.path.join(DATA_DIR, "*"))
    #print(filelist)
    #for f in filelist:
        #os.remove(f)

        #if os.path.exists(DATA_DIR) != True:
            #print("Creating data directory: {}".format(DATA_DIR))
            ##os.mkdir(data_dir)
            #os.makedirs(DATA_DIR)
    #except Exception as e:
        #print(e)


    name, ext = os.path.splitext(_filename)
    if True:
        i = 1
        while os.path.isfile(filename):
            filename = name + "_{}".format(i) + ext
            i += 1

    if False:
        try:
            if os.path.isfile(filename):
                os.remove(filename)
        except Exception as e:
            print(e)

    name, ext = os.path.splitext(filename)
    name = os.path.split(name)[-1] + "_" + ext[1:]
    name = name.replace("-", "_")
    name = name.replace(".", "_")

    db_name = 'data_userID_{}_{}'.format(user.username, name)
    #if i > 5:
        #return db_name
            
    if os.path.exists(DATA_DIR) != True:
        print("Creating data directory: {}".format(DATA_DIR))
        os.makedirs(DATA_DIR)

    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    #from django.contrib.auth.models import User
    #print(User.objects.get(username='rober').id)
    #print(Contact.objects.get(user_id=User.objects.get(username='rober')))

    try:
        conf = Configuration.objects.create(user_id=user.id)
        conf.save()
    except:
        pass
    try:
        activity = Activity.objects.create(user_id=user.id)
        activity.save()
    except:
        pass
    try:
        contact = Contact.objects.create(user_id=user.id)
        contact.save()
    except:
        pass

    try:
        activity = Activity.objects.get(user_id=user.id)
        activity.lastUpload = str(datetime.now().replace(second=0, microsecond=0))
        activity.lastUpload = str(datetime.now().replace(microsecond=0))
        activity.lastFileUploaded = os.path.split(_filename)[1]
        activity.save()
    except:
        print("Could not set Last Activity data and time")

    if dbTools.checkDBexists(userName=user.username + "_{}".format(name)):
        print("Deleting old database...")
        dbTools.dropdb(userName=user.username + "_{}".format(name))

    if not dbTools.checkDBexists(userName=user.username + "_{}".format(name)):
        dbTools.createdb(userName=user.username + "_{}".format(name))
        dbname = "data_userID_" + user.username + "_{}".format(name)
        #try:
        dbTasks.createTasksDB(dbname)
        dbTasks.createTasksTable(dbname)
        dbTasks.initTasksTables(dbname, name=user.username)
        #except Exception as e:
            #print(e)

    if os.path.splitext(f._name)[1] == '.csv':
        dbTools.csv2mysql(data=filename, db_name=db_name)
    if os.path.splitext(f._name)[1] in ['.xlsx', '.xls']:
        try:
            dbTools.xls2mysql(data=filename, db_name=db_name)
        except:
            print("Not posible to upload data. Check your file.")
            return None
    # Run R analysis using data database
    runAnalysis(user.username + "_{}".format(name))

    files = [f for f in os.listdir(HOME_DIR) if os.path.isfile(os.path.join(HOME_DIR,f))]

    return db_name
 
