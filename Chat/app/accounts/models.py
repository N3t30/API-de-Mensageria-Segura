from django.contrib.auth.models import User
from django.db import models  # noqa F401
from app.messaging.utils.crypto import decrypt_message, encrypt_message
from django.utils import timezone


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    ttl_seconds = models.PositiveIntegerField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        creating = self.pk is None 
        super().save(*args, **kwargs)

        if creating and self.ttl_seconds and not self.expired_at:
            self.expired_at = self.created_at + timezone.timedelta(
                seconds=self.ttl_seconds
            )
            
            super().save(update_fields=["expired_at"])


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
