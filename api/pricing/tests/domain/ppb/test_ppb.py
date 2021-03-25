from api.pricing.pricing.domain.ppb.ppb import PPB



def test_calulate_returns_dict_with_keys():

    ppb = PPB()

    product_price = ppb.calculate()

    assert type(product_price) == dict
    assert 'ppb' in product_price
    assert 'max_price' in product_price
    assert 'min_price' in product_price
    assert 'mean_price' in product_price
    assert 'suggested_price' in product_price

# def test_calculate_takes_pd_dataframes():
    # data = 
    # ppb = PPB()