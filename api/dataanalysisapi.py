import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
# import qymatix.util
from api.qymatix import util
import os
import logging
from django.http import Http404
#from extras.runAnalysis import runAnalysis
from django.conf import settings
import os

logger = logging.getLogger(__name__)

_path = os.path.abspath(__file__)
_basepath = os.path.abspath(os.path.join(_path,'../../..'))
_basepath = settings.BASE_DIR


@ensure_csrf_cookie
def analyzeData(request, workspace=1):
    '''
    '''

    if request.method == 'POST':
    #if request.method == 'GET':

        workspace = int(workspace)
        if workspace == 0:
            username = request.user.username
        else:
            username = request.user.email.split('@')[1].replace('.', '_').replace('-', '___')

        db_name = qymatix.util.getDatabaseName(_basepath, username)
        logging.debug("Running analysis for {}".format(db_name))

        try:
            data = runAnalysis(db_name)
            data = json.dumps(data)
            return HttpResponse(data, content_type="application/json")
        except:
            raise Http404('Function error')

