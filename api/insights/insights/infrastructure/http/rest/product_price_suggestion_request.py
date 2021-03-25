import json

from django.http import HttpResponse

from api.insights.insights.application.bus import Bus
from api.insights.insights.application.query.get_price_suggestion_query import GetPriceSuggestionQuery


def request_suggested_price_for_product(request):
    if request.method == 'GET':
        # body = json.loads(request.body)
        # response = json.dumps(body)

        if hasattr(request, 'data'):
            data = request.data
        if hasattr(request, 'body'):
            data = request.body

        # query = GetPriceSuggestionQuery(json.loads(data)['product_id'])
        query = GetPriceSuggestionQuery(request.GET['product_id'])
        # handler = GetPriceSuggestionHandler(query)

        bus = Bus(query)

        response = bus.dispatch()

        return HttpResponse(json.dumps(response), content_type="application/json")
