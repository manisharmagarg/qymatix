import pytest
from api.pricing.pricing.application.get_price_suggestion_query import GetPriceSuggestionQuery


def test_query_should_have_fqdn_method():

    command = GetPriceSuggestionQuery()
    fqdn = {
        "module": "api.pricing.pricing.application.get_price_suggestion_handler",
        "handler_class": "GetPriceSuggestionHandler"
    }
    assert command.fqdn == fqdn


def test_query_should_have_product_id():

    product_id = 1
    command = GetPriceSuggestionQuery(product_id)
    assert command.product_id == 1
