import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
# import qymatix.util
# import qymatix.sales
from api.qymatix import util
from api.qymatix import sales
import os
import logging
from ast import literal_eval
from django.conf import settings


logger = logging.getLogger(__name__)

_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path,'../../..'))
_basepath = settings.BASE_DIR


@ensure_csrf_cookie
def insertSalesRecord(request, data='', workspace=1):

    try:
        data = literal_eval(data)

        if request.method == 'POST':
            # if request.method == 'GET':
            # data = json.dumps(data)
            # return HttpResponse(data, content_type="application/json")
            workspace = int(workspace)
            if workspace == 0:
                username = request.user.username
            else:
                username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')
            db_name = util.getDatabaseName(_basepath, username)

            ans = sales.insertSalesRecord(data, db_name)
            #print(ans)
            data = {
                "sales_id": ans
            }
            data = json.dumps(data)
            return HttpResponse(data, content_type="application/json")
    #except:
    except Exception as e:
        import sys
        print(sys.exc_info()[0])
        print(e.args)
        data = 'Cannot insert data'
        #return HttpResponse(data, content_type="application/json")
        raise


