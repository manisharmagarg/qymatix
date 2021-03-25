from api.insights.insights.application.query.get_price_suggestion_query import GetPriceSuggestionQuery


def test_query_should_have_fqdn_method():
    command = GetPriceSuggestionQuery()
    fqdn = {
        "module": "api.insights.insights.application.handler.get_price_suggestion_handler",
        "handler_class": "GetPriceSuggestionHandler"
    }
    assert command.get_path_and_class_name == fqdn


def test_query_should_have_product_id():
    product_id = 1
    command = GetPriceSuggestionQuery(product_id)
    assert command.product_id == 1
