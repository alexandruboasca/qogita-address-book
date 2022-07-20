import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Address
from .serializers import AddressSerializer


@pytest.mark.django_db
def test_list_addresses(client):
    username = 'testuser'
    password = 'testpassword'
    user_model = get_user_model()
    user = user_model.objects.create_user(username, password)
    client.force_login(user)
    url = reverse('address-list')
    response = client.get(url)

    addresses = Address.objects.all()
    expected_data = AddressSerializer(addresses, many=True).data

    assert response.status_code == 200
    assert response.data == expected_data
