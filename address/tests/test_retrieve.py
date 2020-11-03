import json

from rest_framework.views import status
from rest_framework.test import APIClient

from .setup import TestSetup, create_address, get_url_by_key


class RetrieveAddressTestsNotAuthenticated(TestSetup):
    def test_returns_404_not_authorized(self):
        address = create_address()

        url = get_url_by_key(address.id)
        client = APIClient()
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RetrieveAddressTestsAuthenticated(TestSetup):
    def test_retrieves_an_address(self):
        address = create_address()

        url = get_url_by_key(address.id)
        response = self.client.get(url)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["address"], address.address)
