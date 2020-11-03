import json

from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APIClient

from address.models import Address
from address.serializers import AddressSerializer

from .setup import TestSetup, create_address

ADDRESS_LIST_URL = reverse("address:list_create")


class ListAddressTestsNotAuthenticated(TestSetup):
    def test_returns_404_not_authorized(self):
        client = APIClient()
        response = client.get(ADDRESS_LIST_URL)

        # TODO: check why it returns forbidden instead of not authorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListAddressTestsAuthenticated(TestSetup):
    def test_list_addresses(self):
        create_address()
        create_address(
            **{
                "address": "Av. Brasil",
                "number": 123,
                "complement": "Sala 123",
                "zip_code": 88111222,
                "neighborhood": "Centro",
                "city": "Florianópolis",
                "state": "SC",
                "country": "BR",
            }
        )
        response = self.client.get(ADDRESS_LIST_URL)

        expected = Address.objects.all()
        serialized = AddressSerializer(expected, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(len(json.loads(response.content)), 2)
