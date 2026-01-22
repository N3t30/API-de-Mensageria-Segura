from django.contrib.auth.models import User
from django.db import models  # noqa F401


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", onde_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
