class ChurnRisk:  # pylint: disable=too-few-public-methods

    def __init__(self, churn_risk, last_year_sale):
        super().__init__()

        self.churn_risk = churn_risk
        self.last_year_sale = last_year_sale

    def get_indicators(self):
        low_risk = len(
            list(
                filter(
                    lambda x: 1.3 < x <= 2,
                    self.churn_risk.get('rawRisk')
                )
            )
        )
        some_risk = len(
            list(
                filter(
                    lambda x: 0.7 <= x <= 1.3,
                    self.churn_risk.get('rawRisk')
                )
            )
        )
        high_risk = len(
            list(
                filter(
                    lambda x: 0 <= x < 0.7,
                    self.churn_risk.get('rawRisk')
                )
            )
        )
        unknown = len(
            list(
                filter(
                    lambda x: x > 2 or x < 0,
                    self.churn_risk.get('rawRisk')
                )
            )
        )
        count = len(
            self.churn_risk.get(
                'rawRisk'
            )
        )

        impact_num_risk = ((0.5 * high_risk) + (0.3 * some_risk) + (0.1 * low_risk)) / \
                          (high_risk + some_risk + low_risk)

        impact = round(impact_num_risk * self.last_year_sale.get('last_year_sale'), 2)

        risk_data = {
            'low': low_risk,
            'some': some_risk,
            'high': high_risk,
            'unknown': unknown,
            'count': count,
            'impact': impact
        }
        return risk_data
