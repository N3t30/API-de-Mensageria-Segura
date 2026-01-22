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
        response = self.client.post(self.register_url, {
            "username": "testuser",
            "password": "testpassword123"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login_user(self):
        User.objects.create_user(username="testuser", password="testpassword123")

        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpassword123"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
