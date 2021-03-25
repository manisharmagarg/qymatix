from api.pricing.pricing.domain.price import Price


class Product():

    def __init__(self, id=None):
        super().__init__()
        self.product_id = id

    @property
    def id(self):
        return self.product_id

    @id.setter
    def id(self, id=None):
        self.product_id = id
    
    def suggested_price(self):
        return Price(1)