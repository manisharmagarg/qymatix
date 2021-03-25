import json
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.http import HttpResponse

from api.insights.insights.infrastructure.http.rest import active_accounts_history_request
from api.insights.insights.infrastructure.mysql.read.accounts_history import ActiveAccountsHistory


@pytest.fixture
def mock_active_account():
    # pylint: disable=fixme, too-few-public-methods
    class ActiveAccountMock:
        customer_id = 1
        sales = 200

    return ActiveAccountMock()


@pytest.fixture
def mock_active_account2():
    # pylint: disable=fixme, too-few-public-methods
    class ActiveAccountMock:
        customer_id = 2
        sales = 1000

    return ActiveAccountMock()


@pytest.fixture
def mock_customer1():
    # pylint: disable=fixme, too-few-public-methods
    class CustomerMock():
        customer_id = 1
        customer_name = 'Customer Name'
        sales = 200

    return CustomerMock()


@pytest.fixture
def mock_customer2():
    # pylint: disable=fixme, too-few-public-methods
    class CustomerMock:
        customer_id = 3
        customer_name = 'Inactive Customer'

    return CustomerMock()


def test_get_request_account_history_returns_httpresponse():
    mock_request = Mock(spec=HttpRequest)
    mock_request.method = 'GET'
    isinstance(active_accounts_history_request.request_account_history(mock_request), HttpResponse)


# pylint: disable=too-many-arguments
@pytest.mark.django_db
@patch.object(ActiveAccountsHistory, 'read_active_accounts_history')
@patch.object(ActiveAccountsHistory, 'get_all_customer')
def test_request_accout_history_returns_correct_serialized_object(
        get_all_customer,
        read_active_accounts_history,
        # pylint: disable=fixme, redefined-outer-name
        mock_active_account,
        # pylint: disable=fixme, redefined-outer-name
        mock_active_account2,
        mock_customer1,
        mock_customer2
):
    read_active_accounts_history.return_value = [mock_active_account, mock_active_account2]
    get_all_customer.return_value = [mock_customer1, mock_customer2]

    user = User.objects.create_user('user-name', 'user-name@qymatix-test.com', 'password')
    group = Group.objects.get_or_create(name='qymatix___test_com')[0]
    group.user_set.add(user)

    mock_request = Mock(spec=HttpRequest)
    mock_request.method = 'GET'
    mock_request.user = user
    response = active_accounts_history_request.request_account_history(mock_request)

    data = {
        "active_accounts": {"1": 200, "2": 1000},
        "lost_accounts": [3]
    }

    assert response.content == json.dumps(data).encode('utf-8')


def test_request_account_history_returns_correct_error_response():
    mock_request = Mock(spec=HttpRequest)
    mock_request.method = 'GET'

    expected_response_content = b'{"status_code": 500, "message": "Internal Server Error"}'

    response = active_accounts_history_request.request_account_history(mock_request)

    assert response.status_code == 500
    assert expected_response_content == response.content
