
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestRateLimit(APITestCase):

    def test_login_allowed_before_rate_limit(self):
        url = reverse("login")

        for _ in range(5):
            response = self.client.post(
                url, {"username": "someuser", "password": "wrongpassword"}
            )

        self.assertNotEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
