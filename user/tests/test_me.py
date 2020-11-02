from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


ME_URL = reverse("user:me")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicMeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_returns_unauthorized_error_when_no_token_is_set(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMeApiTests(TestCase):
    def setUp(self):
        payload = {
            "email": "john.doe@dev.com",
            "password": "@Super123",
            "name": "John Doe",
        }
        self.client = APIClient()
        self.user = create_user(**payload)

        self.client.force_authenticate(user=self.user)

    def test_returns_profile_content(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email})
        self.assertNotIn("password", res.data)

    def test_returns_error_when_trying_to_post_on_me_url(self):
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_updates_name(self):
        payload = {"name": "John Doe Jr"}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"email": self.user.email, "name": payload["name"]})

    def test_updates_name_and_password(self):
        payload = {"password": "@NewPassword123"}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload["password"]))
