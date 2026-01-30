import os

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import Message


class MessageEncryptionTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="12345678"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="12345678"
        )

        self.message = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content="mensagem secreta"

        )

    def test_message_is_encrypted_in_db(self):
        msg = Message.objects.get(id=self.message.id)

        self.assertNotEqual(msg.content, "mensagem secreta")

    def test_message_can_be_decrypted(self):
        msg = Message.objects.get(id=self.message.id)

        self.assertEqual(msg.decrypted_content(), "mensagem secreta")

    def test_message_is_not_double_encrypted(self):
        msg = Message.objects.get(id=self.message.id)

        encrypted = msg.content
        msg.save()

        self.assertEqual(msg.content, encrypted)

    def test_encryption_key_loaded_from_env(self):
        self.assertIsNotNone(os.getenv("MESSAGE_ENCRYPTION_KEY"))
