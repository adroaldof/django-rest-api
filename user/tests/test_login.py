from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


AUTHENTICATE_URL = reverse("user:login")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicLoginUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_returns_error_when_user_does_not_exists(self):
        payload = {"email": "john.doe@dev.com", "password": "@Super123"}

        res = self.client.post(AUTHENTICATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.content,
            b'{"non_field_errors":["Unable to authenticate with provided credentials"]}',
        )

    def tests_return_error_on_authenticate_with_wrong_password(self):
        user = {"email": "john.doe@dev.com", "password": "@Super123"}
        create_user(**user)

        payload = {"email": "john.doe@dev.com", "password": "wrong-password"}
        res = self.client.post(AUTHENTICATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.content,
            b'{"non_field_errors":["Unable to authenticate with provided credentials"]}',
        )

    def tests_return_error_on_authenticate_with_invalid_fields(self):
        user = {"email": "john.doe@dev.com", "password": "@Super123"}
        create_user(**user)

        payload = {"email": "", "password": ""}
        res = self.client.post(AUTHENTICATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.content,
            b'{"email":["This field may not be blank."],"password":["This field may not be blank."]}',
        )

    def test_returns_authenticated_user(self):
        payload = {"email": "john.doe@dev.com", "password": "@Super123"}

        create_user(**payload)

        res = self.client.post(AUTHENTICATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)
