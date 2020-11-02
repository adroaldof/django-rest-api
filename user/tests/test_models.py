from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "john.doe@dev.com"
        password = "@Test123"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_is_normalized(self):
        email = "john.doe@DEV.COM"
        password = "@Test123"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email.lower())

    def test_throws_with_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "@Test123")

    def test_create_super_user(self):
        email = "super.user@DEV.COM"
        password = "@Test123"

        user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
