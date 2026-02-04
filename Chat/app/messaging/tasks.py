from celery import shared_task
from django.utils import timezone
from .models import Message, MessageEvent

def expire_message():
    messages = Message.objects.filter(
        is_expired=False,
        expires_at__lte=timezone.now()
    )

    for msg in messages:
        msg.is_expired = True
        msg.save()

        MessageEvent.objects.create(
            message=msg,
            event_type="MESSAGE_EXPIRED"
        )