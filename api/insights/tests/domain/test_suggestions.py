"""
Test case for Suggestions
"""
# pylint: disable=import-error
# pylint: disable=no-init
# pylint: disable=old-style-class
# pylint: disable=redefined-outer-name
# pylint: disable=unused-variable
import pytest
from api.insights.insights.domain.suggestions.get_customer_suggestions import Suggestions


@pytest.fixture
def mock_suggestions():
    """Mock data for suggestions"""
    # pylint: disable=fixme, too-few-public-methods
    mock_suggestion = dict()

    class MockCustomers:
        """Customer mock data for suggestions"""
        mock_suggestion['customers'] = {
            "customer_id": 1000,
            "actions_per_account": {1000: 4, 1006: 1},
            "actions_active_accounts_ratio": 0.0,
            "insights": {'sales_growth_QTD': 0.0},
            1000: {
                'name': "BRAHMS DIAGNOSTIKA",
                'product_cross_selling': '',
                'product_type_cross_selling': '',
                'scales': [
                    {'y': 0.0, 'value': 5580, 'label': 5580},
                    {'y': 0.0, 'value': 2389, 'label': 2389},
                    {'y': 1.0, 'value': 2.0, 'label': 'low'},
                    {'y': 0.25, 'value': 1, 'label': 'normal'},
                    {'y': 0.0, 'value': 0.0, 'label': 0.0}
                ]
            },
        }

    return mock_suggestion


@pytest.mark.django_db
def test_suggestions(mock_suggestions):
    """Test case for get suggestions"""
    response = Suggestions(
        mock_suggestions['customers'],
        mock_suggestions['customers']["customer_id"]
    )
    expected_response_content = [
        {
            "suggestion": "cerebro_msg_grow",
            "customer_name": "BRAHMS DIAGNOSTIKA"
        }
    ]
    assert response.get_suggestions() == expected_response_content
