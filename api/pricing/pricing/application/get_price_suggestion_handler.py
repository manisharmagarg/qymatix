from api.pricing.pricing.application.handler_interface import HandlerInterface
from api.pricing.pricing.domain.ppb.ppb import PPB


class GetPriceSuggestionHandler(HandlerInterface):

    def __init__(self, query):
        super().__init__()
        self.query = query

    def handle(self):
        ppb = PPB()
        ppb.calculate()
