import pytest
from api.importer.importer.domain.product_class import ProductClass


def test_product_class_has_name():

    with pytest.raises(TypeError, match=r".*missing 1 required positional argument.*"):
        product = ProductClass()