from app.messaging.utils.crypto import decrypt_message, encrypt_message
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Message(models.Model):
    Conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        related_name="sent_message",
        on_delete=models.CASCADE
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    ttl_seconds = models.PositiveIntegerField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        creating = self.pk is None

        if self.ttl_seconds is not None and self.ttl_seconds < 0:
            raise ValidationError("TTL não pode ser negativo")

        if creating and self.content:
            self.content = encrypt_message(self.content)

        if creating and self.ttl_seconds and not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(
                seconds=self.ttl_seconds
            )

        super().save(*args, **kwargs)

    def decrypted_content(self):
        return decrypt_message(self.content)


class MessageEvent(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="events"
    )
    event_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - message {self.message.id}"


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    target = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"


class Conversation(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return " - ".join([u.username for u in self.participants.all()])
