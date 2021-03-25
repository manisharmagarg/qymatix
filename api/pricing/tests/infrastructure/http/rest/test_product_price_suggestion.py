from api.pricing.pricing.infrastructure.http.rest import product_price_suggestion_request
from unittest.mock import Mock, PropertyMock, patch
from unittest import mock
from django.http import HttpRequest
from django.http import HttpResponse
import pytest
import json


class HttpResponseGetMock():
    method = 'GET'
    body = json.dumps({"product_id": 1})
    content = json.dumps({"product_id": 1})
    data = json.dumps({"product_id": 1})


class HttpRequestMock():

    @property
    def method():
        return 'GET'

    @property
    def body():
        return json.dumps({ "product_id": 1})

    @property
    def content():
        return json.dumps({ "product_id": 1})


def test_get_price_suggestion_for_product():

    response = HttpResponseGetMock()
    isinstance(product_price_suggestion_request.request_suggested_price_for_product(response), HttpResponse)


@pytest.mark.skip(reason=None)
def test_get_price_suggestion_for_product_alternative():

    mock_request = Mock(spec=HttpRequest)
    mock_request.method = 'GET'
    mock_request.data = {
        "product_id": 1
    }

    response = product_price_suggestion_request.request_suggested_price_for_product(mock_request)

    assert response.content['suggested_price'] == 1