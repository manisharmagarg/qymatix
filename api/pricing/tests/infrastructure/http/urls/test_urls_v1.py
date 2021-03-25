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

    token = token_generator.make_token(user)

    return str(user.id) + ":" + token


def test_view(client, token):
    url = reverse('product-price-suggestion')
    header = {'api-token': token} 
    data = {'product_id': 1}
    response = client.get(url, content_type='application/json', data=data, **header)
    assert response.status_code == 200
