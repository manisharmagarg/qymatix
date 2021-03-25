class CrossSelling:  # pylint: disable=too-few-public-methods

    def __init__(self, cross_selling, last_year_sale):
        super().__init__()

        self.cross_selling = cross_selling
        self.last_year_sale = last_year_sale

    def get_indicators(self):
        ccbm = self.cross_selling.get('ccbm')
        ppb = self.cross_selling.get('ppb')
        risk = self.cross_selling.get('risk')
        impact = round(self.last_year_sale.get('last_year_sale') * ccbm, 2)

        selling_data = {
            'impact': impact,
            'ccbm': ccbm,
            'ppb': ppb,
            'risk': risk
        }
        return selling_data
