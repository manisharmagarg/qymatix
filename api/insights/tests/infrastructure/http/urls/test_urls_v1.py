import pytest
from django.urls import reverse

from tokenapi.tokens import token_generator


@pytest.fixture
@pytest.mark.django_db
def token(django_user_model):
    username = "test__test_com"
    email = "test@test.com"
    password = "test"

    user = django_user_model.objects.create_user(username, email, password)
    user.save()

    token_value = token_generator.make_token(user)

    return str(user.id) + ":" + token_value


# pylint: disable=redefined-outer-name
def test_active_accounts_url_returns_500_error(client, token):
    url = reverse('insights-active-accounts')
    header = {'api-token': token}
    data = ''
    response = client.get(url, content_type='application/json', data=data, **header)
    assert response.status_code == 500


# pylint: disable=redefined-outer-name
def test_active_accounts_url_returns_400_error(client, token):
    url = reverse('insights-active-accounts')
    header = {'api-token': token}
    data = ''
    response = client.post(url, content_type='application/json', data=data, **header)
    assert response.status_code == 400
