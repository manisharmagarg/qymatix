"""JSON helper functions"""
try:
    import simplejson as json
except ImportError:
    import json

from django.http import HttpResponse


def json_response(data, dump=True, status=200):
    try:
        data['errors']
    except KeyError:
        data['success'] = True
    except TypeError:
        pass

    return HttpResponse(
        json.dumps(data) if dump else data,
        content_type='application/json',
        status=status,
    )


def json_error(error_string, status=200):
    data = {
        'success': False,
        'errors': error_string,
    }
    return JSONResponse(data)


def json_response_bad_request(error_string):
    return json_error(error_string, status=400)


def json_response_unauthorized(error_string):
    return json_error(error_string, status=401)


def json_response_forbidden(error_string):
    return json_error(error_string, status=403)


def json_response_not_found(error_string):
    return json_error(error_string, status=404)


def json_response_not_allowed(error_string):
    return json_error(error_string, status=405)


def json_response_not_acceptable(error_string):
    return json_error(error_string, status=406)


# For backwards compatability purposes
JSONResponse = json_response
JSONError = json_error
