from api.importer.importer.domain.customer import Customer
import pytest

@pytest.fixture
def customer():
    customer = Customer()
    customer.name = None
    customer.a= None


def test_customer_raise_exception_when_no_name():

    with pytest.raises(TypeError, match=r".*missing 1 required positional argument.*"):
        customer = Customer()