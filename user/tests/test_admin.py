from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            email="joan.doe@dev.com", password="@Super123"
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="john.doe@dev.com", password="@Super123", name="Joan Doe"
        )

    def test_users_listed(self):
        url = reverse("admin:user_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        url = reverse("admin:user_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        url = reverse("admin:user_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
