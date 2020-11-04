from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APIClient, APITestCase

from .setup import TestSetup, create_address, get_url_by_key


class DeleteAddressTestsNotAuthenticated(APITestCase):
    def test_returns_not_authorized(self):
        address = create_address()
        url = get_url_by_key(address.id)

        client = APIClient()
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteAddressTestsAuthenticated(TestSetup):
    def test_returns_404_not_found(self):
        url = get_url_by_key(999)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deletes_an_existing_address(self):
        address = create_address()
        url = get_url_by_key(address.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
