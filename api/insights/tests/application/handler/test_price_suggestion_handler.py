from api.insights.insights.application.handler.get_price_suggestion_handler import GetPriceSuggestionHandler
from api.insights.insights.application.query.get_price_suggestion_query import GetPriceSuggestionQuery
import pytest
from unittest.mock import patch


def test_handler_initializes():

    query = GetPriceSuggestionQuery(1)
    handler = GetPriceSuggestionHandler(query)

    isinstance(handler.query, GetPriceSuggestionQuery)
    assert handler.query.product_id == 1


def test_handler_handle():

    query = GetPriceSuggestionQuery(1)
    handler = GetPriceSuggestionHandler(query)

    class_to_mock = 'api.insights.insights.domain.ppb.ppb.PPB.calculate'
    with patch(class_to_mock) as mocked_ppb:
        handler.handle()
        mocked_ppb.assert_called_once()
