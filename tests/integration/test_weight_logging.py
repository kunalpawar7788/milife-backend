import json
import pytest

from django.urls import reverse

from .. import factories as f

pytestmark = pytest.mark.django_db


# def test_get_weight_list(client):
#     url = reverse('user_weight:get')
#     user = f.create_user(email='test@example.com')
#     # admin = f.create_user(email='admin@mi-life.co.uk', is_staff=True)
#     # should require auth
#     response = client.get(url)
#     assert response.status_code == 401

#     client.login(user)
#     response = client.get(url)

#     # assert response is None
#     assert response.status_code == 200
#     # expected_keys = [
#     #     'id', 'email', 'first_name', 'last_name'
#     # ]
#     # assert set(expected_keys).issubset(response.data.keys())
#     # assert response.data['id'] == str(user.id)

def test_get_weight_list(apiclient):
    user = f.create_user(email='test@example.com')
    url = reverse("user_weight-list", kwargs={'user_pk': str(user.id)})
    response = apiclient.get(url)
    assert response.status_code == 401

    apiclient.force_authenticate(user=user)
    response = apiclient.get(url)
    assert response.status_code == 200

