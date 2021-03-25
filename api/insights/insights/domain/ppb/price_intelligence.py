class PriceIntelligence:  # pylint: disable=too-few-public-methods
    def __init__(self, price_intelligence, last_year_sale):
        super().__init__()

        self.price_intelligence = price_intelligence
        self.last_year_sale = last_year_sale

    def get_indicators(self):
        count = len(self.price_intelligence.get('ppb'))

        good = len(
            list(
                filter(
                    lambda x: x == 2.0,
                    self.price_intelligence.get('ppb')
                )
            )
        )

        normal = len(
            list(
                filter(
                    lambda x: x == 0,
                    self.price_intelligence.get('ppb')
                )
            )
        )

        bad = len(
            list(
                filter(
                    lambda x: x == 1.0,
                    self.price_intelligence.get('ppb')
                )
            )
        )

        unknown = len(
            list(
                filter(
                    lambda x: x == 4.0,
                    self.price_intelligence.get('ppb')
                )
            )
        )

        impact_num_price = ((0.15 * bad) + (0.07 * normal) + (0.01 * good)) / (bad + normal + good)
        impact = round(
            impact_num_price * self.last_year_sale.get('last_year_sale'), 2
        )
        intelligence_data = {
            'count': count,
            'good': good,
            'normal': normal,
            'bad': bad,
            'unknown': unknown,
            'impact': impact,
        }

        return intelligence_data
