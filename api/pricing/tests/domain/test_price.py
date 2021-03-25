import pytest
from api.pricing.pricing.domain.price import Price


def test_suggested_price_is_positive():

    value = -1
    with pytest.raises(ValueError, match=r".*Price cannot be negative.*"):
        price = Price(value)
