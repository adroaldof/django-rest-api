import json

from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APIClient, APITestCase

from .setup import TestSetup, create_address


def get_url(key):
    return reverse("address:retrieve_update_destroy", kwargs={"pk": key})


class UpdateAddressTestsNotAuthenticated(APITestCase):
    def test_returns_401_not_authorized(self):
        client = APIClient()
        data = {"address": "new address"}
        response = client.patch(get_url(1), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateAddressTestsAuthenticated(TestSetup):
    def test_returns_404_not_found_when_address_not_exists(self):
        data = {"address": "new address"}
        url = get_url(999)
        response = self.client.patch(url, data=data)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(content["detail"], "Not found.")

    def test_partially_updates_an_address(self):
        address = create_address()

        url = get_url(address.id)
        data = {"address": "new address"}
        response = self.client.patch(url, data=data)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["address"], data["address"])
