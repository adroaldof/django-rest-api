from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from address.models import Address


class TestSetup(APITestCase):
    client = APIClient()

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("dev.user@dev.com", "@Test123")
        self.client.force_authenticate(self.user)


def get_url_by_key(key):
    return reverse("address:retrieve_update_destroy", kwargs={"pk": key})


def create_address(**params):
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
    address.update(**params)

    return Address.objects.create(**address)
