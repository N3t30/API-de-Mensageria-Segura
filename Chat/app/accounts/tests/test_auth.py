from axes.models import AccessAttempt
from django.contrib.auth.models import User
from django.test import TestCase  # noqa: F401
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestAuth(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("token_obtain_pair")

    def test_register_user(self):
        response = self.client.post(
            self.register_url, {"username": "testuser", "password": "testpassword123"}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login_with_valid_credentials_returns_token(self):
        url = reverse("register")
        self.client.post(
            url,
            {
                "username": "testuser",
                "password": "strongpassword123",
            },
        )

        url = reverse("login")
        response = self.client.post(
            url,
            {
                "username": "testuser",
                "password": "strongpassword123",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_wrong_password_resturns_401(self):
        url = reverse("login")
        response = self.client.post(
            url,
            {
                "username": "testuser",
                "password": "wrongpassword",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rate_limit_is_in_based(self):
        url = reverse("login")
        for _ in range(5):
            response = self.client.post(
                url,
                {
                    "username": "someuser",
                    "password": "wrongpassword",
                },
            )

        self.assertNotEqual(response.status_code, 429)

    def test_axes_blocks_after_multiple_failed_logins(self):
        url = reverse("login")

        for _ in range(10):
            self.client.post(
                url,
                {
                    "username": "testuser",
                    "password": "wrongpassword",
                },
            )

        self.assertTrue(AccessAttempt.objects.exists())
