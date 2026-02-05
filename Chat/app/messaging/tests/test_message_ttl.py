import os
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from app.accounts.models import Message, MessageEvent


from app.messaging.tasks import expire_messages

class MessageTTLTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="123456"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="123456"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    

    def test_message_creates_expires_at_from_ttl(self):

        msg = Message.objects.create(
            sender=self.user,
            recipient=self.user2,
            content="Teste de TTL",
            ttl_seconds=60
        )

        self.assertIsNotNone(msg.expires_at)

    def test_expired_message_not_returned(self):

        msg =Message.objects.create(
            sender=self.user,
            recipient=self.user2,
            content="expirada",
            expires_at=timezone.now() - timedelta(minutes=1),
            is_expired=True
        )

        response = self.client.get(reverse("message-detail", args=[msg.id]))
        self.assertEqual(response.status_code, 404)

    def test_expire_task_marks_message(self):

        msg = Message.objects.create(
            sender=self.user,
            recipient=self.user2,
            content="ttl",
            expires_at=timezone.now() - timedelta(minutes=1),
            is_expired=False
        )

        expire_messages()

        msg.refresh_from_db()
        self.assertTrue(msg.is_expired)

    def test_event_created_on_message_expiration(self):

        msg = Message.objects.create(
            sender=self.user,
            recipient=self.user2,
            expires_at=timezone.now() - timedelta(minutes=1)
        )

        expire_messages()

        self.assertTrue(
            MessageEvent.objects.filter(
                message=msg,
                event_type="MESSAGE_EXPIRED"
            )  .exists()
        )

    def test_cannot_retrieve_expired_message_by_id(self):

        msg = Message.objects.create(
            sender=self.user,
            recipient=self.user2,
            content="expirado",
            expires_at=timezone.now() - timedelta(minutes=1),
            is_expired=True
        )

        response = self.client.get(
            reverse("message-detail", args=[msg.id])
        )

        self.assertEqual(response.status_code, 404)


    def test_negative_ttl_is_rejected(self):

        response = self.client.post(
            reverse("create-message"),
            {
                'recipient':self.user2.id,
                'content':'teste',
                'ttl_seconds': -10
            }
        )

        self.assertEqual(response.status_code, 400)
