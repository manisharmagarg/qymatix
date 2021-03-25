from api.pricing.pricing.domain.product import Product
from api.pricing.pricing.domain.price import Price


def test_product_id():
    id = 1
    product = Product()
    product.id = id

    assert product.id == 1


def test_price_suggested_returns_price_instance():

    id = 1
    product = Product(id)

    isinstance(product.suggested_price, Price)
