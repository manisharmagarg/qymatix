import pytest
from api.importer.importer.domain.product_line import ProductLine


def test_product_line_has_name():

    with pytest.raises(TypeError, match=r".*missing 1 required positional argument.*"):
        product = ProductLine()