import json

from sqlalchemy import func

from api.insights.insights.infrastructure.mysql.mysql_connection \
    import MySqlConnection
from api.insights.insights.infrastructure.mysql.orm.autogen_entities \
    import Sale


class CustomerProductsArticleHistory:

    def __init__(self, database, customer_id, product_id):
        super().__init__()
        self.data_db = "data_{}".format(database)
        connection = MySqlConnection(self.data_db)
        self.session = connection.session()
        self.results = self.read_customer_product_article_history(
            customer_id,
            product_id
        )

    def read_customer_product_article_history(self, customer_id, product_id):
        results = self.session.query(
            Sale.year,
            Sale.month,
            func.sum(Sale.price).label('total_price')
        ) \
            .filter_by(customer_id=customer_id, product_id=product_id) \
            .group_by(Sale.year, Sale.month) \
            .all()

        return results

    def as_json(self):
        article_customer = dict()
        modify_article_customer = dict()
        for result in self.results:
            year = int(result.year)
            month = int(result.month)
            total_price = round(result.total_price, 2)

            if year in article_customer:
                article_customer[year][month] = total_price
            else:
                article_customer[year] = {month: total_price}

        months_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for year_keys in article_customer:
            for list_months in months_list:
                months = article_customer.get(year_keys)
                if list_months in months.keys():
                    if year_keys in modify_article_customer:
                        modify_article_customer[year_keys] \
                            [list_months] = months.get(list_months)
                    else:
                        modify_article_customer[year_keys] = {
                            list_months: months.get(
                                list_months
                            )
                        }
                else:
                    if year_keys in modify_article_customer:
                        modify_article_customer[year_keys][list_months] = 0
                    else:
                        modify_article_customer[year_keys] = {list_months: 0}

        return json.dumps(modify_article_customer)
