from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from api.pricing.pricing.application.get_price_suggestion_query import GetPriceSuggestionQuery
from api.pricing.pricing.application.get_price_suggestion_handler import GetPriceSuggestionHandler


def request_suggested_price_for_product(request):

    if request.method == 'GET':
        # body = json.loads(request.body)
        # response = json.dumps(body)
        query = GetPriceSuggestionQuery(json.loads(request.data)['product_id'])
        handler = GetPriceSuggestionHandler(query)
        response = query
        return HttpResponse(response, content_type="application/json")