import json

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

from address.models import Address
from .setup import TestSetup

ADDRESS_CREATE_URL = reverse("address:list_create")

address = {
    "address": "3972S 3075E",
    "number": 123,
    "complement": "Apt 123",
    "zip_code": 84124,
    "neighborhood": "Holladay",
    "city": "Salt Lake City",
    "state": "UT",
    "country": "US",
}


class CreateAddressTestsNotAuthenticated(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_returns_not_authorized(self):
        data = address.copy()
        response = self.client.post(ADDRESS_CREATE_URL, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateAddressTestsAuthenticated(TestSetup):
    def test_returns_404_without_required_fields(self):
        data = address.copy()
        del data["country"]

        response = self.client.post(ADDRESS_CREATE_URL, data=data)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content["country"], ["This field is required."])

    def test_creates_without_optional_key(self):
        data = address.copy()
        del data["complement"]

        response = self.client.post(ADDRESS_CREATE_URL, data=data)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(content["complement"])

    def test_creates_with_full_address(self):
        data = address.copy()

        response = self.client.post(ADDRESS_CREATE_URL, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_address = Address.objects.get(id=response.data["id"])

        for key in address:
            self.assertEqual(address[key], getattr(created_address, key))
