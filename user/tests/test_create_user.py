from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicCreateUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_with_valid_payload(self):
        payload = {
            "email": "john.doe@dev.com",
            "password": "@Super123",
            "name": "John Doe",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_returns_error_when_trying_duplicate_an_user(self):
        payload = {
            "email": "john.doe@dev.com",
            "password": "@Super123",
            "name": "John Doe",
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.content, b'{"email":["user with this email already exists."]}'
        )

    def test_password_should_be_greater_than_eight_chars(self):
        payload = {
            "email": "john.doe@dev.com",
            "password": "fwchars",
            "name": "John Doe",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(email=payload["email"])

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)
        self.assertEqual(
            res.content,
            b'{"password":["Ensure this field has at least 8 characters."]}',
        )
