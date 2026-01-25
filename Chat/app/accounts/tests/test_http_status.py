from django.contrib.auth.models import User
from django.db.models import Max
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import AuditLog, Message


class TestHTTPStatus(APITestCase):

    def setUp(self):
        self.user_a = User.objects.create_user(
            username="user_a", password="12345678"
        )
        self.user_b = User.objects.create_user(
            username="user_b", password="12345678"
        )
        self.user_c = User.objects.create_user(
            username="user_c", password="12345678"
        )

        self.admin = User.objects.create_user(
            username="admin", password="12345678", is_staff=True
        )

        self.message = Message.objects.create(
            sender=self.user_a,
            recipient=self.user_b,
            content="mensagem secreta"
        )

    def test_create_message_return_201(self):
        self.client.force_authenticate(user=self.user_a)

        response = self.client.post(
            "/api/auth/messages/",
            {
                "recipient": self.user_b.id,
                "content": "Olá"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creatE_message_invalid_payload_returns_400(self):
        self.client.force_authenticate(user=self.user_a)

        response = self.client.post(
            "/api/auth/messages/",
            {
                'content': "Para niguém"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_participant_can_read_message_retuns_200(self):
        self.client.force_authenticate(user=self.user_b)

        response = self.client.get(f"/api/auth/messages/{self.message.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anauthenticate_access_returns_401(self):
        response = self.client.get(f"/api/auth/messages/{self.message.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_participant_gets_403_and_creates_audit_log(self):
        self.client.force_authenticate(user=self.user_c)

        response = self.client.get(f"/api/auth/messages/{self.message.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            AuditLog.objects.filter(
                user=self.user_c,
                action="UNAUTHORIZED_ACCESS",
                target=f"message:{self.message.id}"
            ).exists()
        )

    def test_get_nonexistent_message_returns_404(self):
        self.client.force_authenticate(user=self.user_a)

        max_id = Message.objects.aggregate(max_id=Max('id'))['max_id']
        nonexistent_id = (max_id or 0) + 1

        response = self.client.get(f"/api/auth/messages/{nonexistent_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_read_any_message_returns_200(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(f"/api/auth/messages/{self.message.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
