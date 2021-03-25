import json
from django.http import HttpResponse
from api.insights.insights.infrastructure.mysql.read.customer_product_article_history \
    import CustomerProductsArticleHistory


def request_get_customer_by_products_articles(request):
    if request.method == 'GET':

        if hasattr(request, 'data'):
            data = request.data
        if hasattr(request, 'body'):
            data = request.body

        group_name = request.user.groups.all()[0]

        if 'customer_id' in request.GET.keys() \
                and 'product_id' in request.GET.keys():
            article_customer_history = CustomerProductsArticleHistory(
                group_name,
                request.GET.get('customer_id'),
                request.GET.get('product_id')
            )
            response = article_customer_history.as_json()

            return HttpResponse(response, content_type="application/json")
        else:
            data = {
                "msg": "parameters are wrong or missing."
            }
            response = json.dumps(data)
            return HttpResponse(
                response,
                content_type="application/json",
                status=400
            )
