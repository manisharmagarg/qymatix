import pytest
from api.importer.importer.domain.product import Product


def test_product_has_name():

    with pytest.raises(TypeError, match=r".*missing 1 required positional argument.*"):
        product = Product()