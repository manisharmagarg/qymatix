"""
Suggestions class return the suggestion for customer as per
their calculations
"""
# pylint: disable=too-few-public-methods


class Suggestions(object):
    """return: suggestions as per calculations"""

    def __init__(self, customers, customer_id):
        super(Suggestions, self).__init__()

        self.customers = customers
        self.customer_id = customer_id

    def get_suggestions(self):
        """
        return: suggestions for particular customer
        """
        customer_actions = 0.0
        suggestions = list()

        if int(self.customer_id) in self.customers["actions_per_account"]:
            customer_actions = self.customers["actions_per_account"][int(
                self.customer_id)]
        else:
            customer_actions = 0.0

        if not customer_actions > self.customers.get("actions_active_accounts_ratio"):
            suggestions.append(
                {
                    "suggestion": "cerebro_msg_active",
                    "customer_name": self.customers[self.customer_id]['name']
                }
            )

        ppb = self.customers[self.customer_id]['scales'][3]["label"]
        if ppb == 'bad':
            suggestions.append(
                {"suggestion": "cerebro_msg_price"}
            )

        risk = self.customers[self.customer_id]['scales'][2]["label"]
        if risk == 'high':
            suggestions.append(
                {"suggestion": "cerebro_msg_churn"}
            )
        if self.customers["insights"]["sales_growth_QTD"] <= 100:
            suggestions.append(
                {
                    "suggestion": "cerebro_msg_grow",
                    "customer_name": self.customers[self.customer_id]['name']
                }
            )
        products_with_potential = self.customers[
            self.customer_id]["product_cross_selling"]
        products_type_with_potential = self.customers[
            self.customer_id]["product_type_cross_selling"]

        if products_type_with_potential:
            suggestions.append(
                {
                    "suggestion": "cerebro_msg_pot_pr"
                }
            )
        if products_with_potential:
            suggestions.append(
                {
                    "suggestion": "cerebro_msg_pot"
                }
            )

        if not suggestions:
            suggestions.append(
                {
                    "suggestion": "cerebro_msg_fine",
                    "customer_name": self.customers[self.customer_id]['name']
                }
            )
        return suggestions
