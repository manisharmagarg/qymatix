


class SalesRecord():

    def __init__(self):

        self._invoice = None
        self._price = None
        self._margin = None
        self._cost = 0
        self._quantity = None
        self._date = None
        self._customer_id = None
        self._product_id = None
        self._kam_id = None

    @property
    def invoice(self):
        return self._invoice

    @invoice.setter
    def invoice(self, value: float):
        self._invoice = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value: float):
        self._quantity = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value: float):
        if self._margin == None:
            self._margin = value
        self._price = value

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, value: float):
        # self.validate_margin(value)
        self._margin = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value: float):
        self.validate_cost(value)
        self._cost = value

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, value: int):
        self._product_id = value

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value: int):
        self._customer_id = value

    @property
    def kam_id(self):
        return self._kam_id

    @kam_id.setter
    def kam_id(self, value: int):
        self._kam_id = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    def validate_margin(self, value):
        if self._price != None and value != None:
            if self._price - value < 0:
                raise ValueError("Price cannot be smaller than margin")

    def validate_cost(self, value):
        if self._price != None and self._margin != None:
            if self._price - self._margin != self._cost:
                raise ValueError("Cost does not match price and margin")


