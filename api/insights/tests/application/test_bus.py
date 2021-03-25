from api.insights.insights.application.bus import Bus
from api.insights.insights.application.query.get_price_suggestion_query import GetPriceSuggestionQuery
import pytest
from unittest.mock import patch


# @pytest.fixture(autouse=True)
def test_bus_finds_handler():

    query = GetPriceSuggestionQuery(1)
    bus = Bus(query)

    class_to_mock = 'api.insights.insights.application.handler.get_price_suggestion_handler.GetPriceSuggestionHandler'
    with patch(class_to_mock) as mocked_handler:
        bus.dispatch()
        mocked_handler.assert_called_once()
