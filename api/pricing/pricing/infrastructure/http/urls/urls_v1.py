from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from tokenapi.decorators import token_required_v1

from api.pricing.pricing.infrastructure.http.rest import product_price_suggestion_request


urlpatterns = [
    # Pricing
    re_path(
        r'^product-price-suggestion$',
        token_required_v1(product_price_suggestion_request.request_suggested_price_for_product),
        name=u"product-price-suggestion"
    ),
]