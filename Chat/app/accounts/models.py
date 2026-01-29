from django.contrib.auth.models import User
from django.db import models  # noqa F401
from messaging.utils.crypto import decrypt_message, encrypt_message


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.content.startswith("gAAAA"):
            self.content = encrypt_message(self.content)
        super().save(*args, **kwargs)

    def decrypted_content(self):
        return decrypt_message(self.content)


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    target = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
