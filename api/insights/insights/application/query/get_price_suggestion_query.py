from api.insights.insights.application.query_interface import QueryInterface


class GetPriceSuggestionQuery(QueryInterface):

    def __init__(self, product_id=None):
        super().__init__()
        self.id_product = product_id

    @property
    def product_id(self):
        return self.id_product

    def get_path_and_class_name(self):
        module = "api.insights.insights.application.handler.get_price_suggestion_handler"
        handler_class = "GetPriceSuggestionHandler"

        return {'module': module, 'handler_class': handler_class}
