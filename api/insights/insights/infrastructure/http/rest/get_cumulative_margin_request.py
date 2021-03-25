"""
API is responsible to get get cumulative margin
"""
# pylint: disable=import-error
import json
import logging
import traceback
from django.http import HttpResponse
from ...mysql.read.cumulative_sales import CumulativeSales

logger = logging.getLogger(__name__)


def request_get_cumulative_margin(request):
    """
    function: request for get cumulative margin
    """
    if request.method == 'GET':

        try:
            group_name = request.user.groups.all()[0]
            margin_obj = CumulativeSales(group_name, _type="margin")
            response = margin_obj.as_array()
            status = 200
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
            response = json.dumps({
                "status_code": 500,
                "message": "Internal Server Error"
            })
            status = 500

    else:
        response = ''
        status = 400

    return HttpResponse(
        response,
        content_type="application/json",
        status=status
    )
