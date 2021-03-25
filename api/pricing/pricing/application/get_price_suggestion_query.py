from api.pricing.pricing.application.query_interface import QueryInterface


class GetPriceSuggestionQuery(QueryInterface):

    def __init__(self, product_id=None):
        super().__init__()
        self.id = product_id

    @property
    def product_id(self):
        return self.id

    @property
    def fqdn(self):
        module = "api.pricing.pricing.application.get_price_suggestion_handler"
        handler_class = "GetPriceSuggestionHandler"

        return {'module': module, 'handler_class': handler_class}
