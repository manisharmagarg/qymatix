"""
Script to Define the Urls in patterns
"""
# pylint: disable=import-error
# pylint: disable=invalid-name
from django.urls import re_path
from tokenapi.decorators import token_required_v1
from ...http.rest import product_price_suggestion_request
from ...http.rest import sales_history_request
from ...http.rest import margin_history_request
from ...http.rest import cross_selling_history_request
from ...http.rest import risk_history_request
from ...http.rest import price_intelligence_history_request
from ...http.rest import active_accounts_history_request
from ...http.rest import customers_request
from ...http.rest import customer_by_products_articles_request
from ...http.rest import get_accounts_list_request
from ...http.rest import get_suggestions_request
from ...http.rest import notes_api_request
from ...http.rest import get_cumulative_sales_request
from ...http.rest import get_cumulative_margin_request
from ...http.rest import customers_chart_data_request


urlpatterns = [
    re_path(
        r'^product-price-suggestion$',
        token_required_v1(
            product_price_suggestion_request.request_suggested_price_for_product
        ),
        name=u"product-price-suggestion"
    ),
    re_path(
        r'^insights-sales$',
        token_required_v1(
            sales_history_request.request_sales_history
        ),
        name=u"insights-sales"
    ),
    re_path(
        r'^insights-margin$',
        token_required_v1(
            margin_history_request.request_margin_history
        ),
        name=u"insights-margin"
    ),
    re_path(
        r'^insights-cross-selling$',
        token_required_v1(
            cross_selling_history_request.request_selling_history
        ),
        name=u"insights-cross-selling"
    ),
    re_path(
        r'^insights-churn-risk$',
        token_required_v1(
            risk_history_request.request_risk_history
        ),
        name=u"insights-churn-risk"
    ),
    re_path(
        r'^insights-price-intelligence$',
        token_required_v1(
            price_intelligence_history_request.request_price_intelligence_history
        ),
        name=u"insights-price-intelligence"
    ),
    re_path(
        r'^insights-active-accounts$',
        token_required_v1(
            active_accounts_history_request.request_account_history
        ),
        name=u"insights-active-accounts"
    ),
    re_path(
        r'^get-customers$',
        token_required_v1(
            customers_request.request_get_customers
        ),
        name=u"get-customers"
    ),
    re_path(
        r'^getCustomerByProductsArticles$',
        token_required_v1(
            customer_by_products_articles_request.request_get_customer_by_products_articles
        ),
        name=u"get-Customer-By-Products-Articles"
    ),
    re_path(
        r'^get-accounts$',
        token_required_v1(
            get_accounts_list_request.request_get_accounts_list
        ),
        name=u"get-accounts"
    ),
    re_path(
        r'^get-suggestions$',
        token_required_v1(
            get_suggestions_request.request_get_suggestions
        ),
        name=u"get-suggestions"
    ),
    re_path(
        r'^create-notes$',
        token_required_v1(notes_api_request.NotesAPI.as_view()),
        name=u"create-notes"
    ),
    re_path(
        r'^get-notes$',
        token_required_v1(
            notes_api_request.NotesAPI.as_view(),
        ),
        name=u"get-notes"
    ),
    re_path(
        r'^modify-notes$',
        token_required_v1(
            notes_api_request.NotesAPI.as_view(),
        ),
        name=u"modify-notes"
    ),
    re_path(
        r'^get-cumulative-sales',
        token_required_v1(
            get_cumulative_sales_request.request_get_cumulative_sales
        ),
        name=u"get-cumulative-sales"
    ),
    re_path(
        r'^get-cumulative-margin',
        token_required_v1(
            get_cumulative_margin_request.request_get_cumulative_margin
        ),
        name=u"get-cumulative-margin"
    ),
    re_path(
        r'^customers-chart-data',
        token_required_v1(
            customers_chart_data_request.request_customers_chart_data
        ),
        name=u"customers-chart-data"
    ),
]
