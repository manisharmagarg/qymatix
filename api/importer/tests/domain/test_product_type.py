import pytest
from api.importer.importer.domain.product_type import ProductType


def test_product_type_has_name():

    with pytest.raises(TypeError, match=r".*missing 1 required positional argument.*"):
        product = ProductType()