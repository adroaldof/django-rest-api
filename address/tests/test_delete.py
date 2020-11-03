from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APIClient, APITestCase

from .setup import TestSetup, create_address


def get_url(key):
    return reverse("address:retrieve_update_destroy", kwargs={"pk": key})


class DeleteAddressTestsNotAuthenticated(APITestCase):
    def test_returns_not_authorized(self):
        address = create_address()
        url = get_url(address.id)

        client = APIClient()
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteAddressTestsAuthenticated(TestSetup):
    def test_returns_404_not_found(self):
        url = get_url(999)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deletes_an_existing_address(self):
        address = create_address()
        url = get_url(address.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
