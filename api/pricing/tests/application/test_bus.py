from api.pricing.pricing.application.bus import Bus
from api.pricing.pricing.application.get_price_suggestion_query import GetPriceSuggestionQuery
import pytest
from unittest.mock import patch


# @pytest.fixture(autouse=True)
def test_bus_finds_handler():

    query = GetPriceSuggestionQuery(1)
    bus = Bus(query)

    class_to_mock = 'api.pricing.pricing.application.get_price_suggestion_handler.GetPriceSuggestionHandler'
    with patch(class_to_mock) as mocked_handler:
        bus.dispatch()
        mocked_handler.assert_called_once()
