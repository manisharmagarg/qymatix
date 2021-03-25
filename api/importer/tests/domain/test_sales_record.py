import pytest
from api.importer.importer.domain.sales_record import SalesRecord
from datetime import datetime

@pytest.fixture
def sales_record():
    record = SalesRecord()

    record.invoice = '001'
    record.price = 1.
    record.margin = 1.
    record.cost = 1.
    record.quantity = 1
    record.date = datetime.now()
    record.product_id = 'p1'
    record.customer_id = 'customer name'
    record.kam_id = '1'

    return record


@pytest.fixture
def column_mapping():
    cols = {
            'Auftragsnr.': 'invoice',
            'Re-/Gu-Datum': 'Date',
            'Artikelnr.': 'product',
            'Artikelgruppennr.': 'product type',
            'Umsatz VK': 'price',
            'Marge': 'margin',
            'Warengruppennr.': 'product line',
            'Menge': 'quantity',
            'MC Kunde': 'account name',
            'Branchennr.': 'product class',
            'Branchenbez.': 'industry',
            'Vertretername': 'kam',
        }

    return cols


def test_sales_record_margin_is_set_when_price_is_set(sales_record):

    sales_record.price = 1.0
    assert sales_record.margin == sales_record.price


def test_sales_record_margin_value_exception(sales_record):

    with pytest.raises(ValueError, match=r".*Price cannot be smaller than margin.*"):
        sales_record.price = 1.0
        sales_record.margin = 1.1


def test_sales_record_cost_value_exception(sales_record):

    with pytest.raises(ValueError, match=r".*Cost does not match price and margin.*"):
        sales_record.price = 1.0
        sales_record.margin = 1.0
        sales_record.cost = 0.1
