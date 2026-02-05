from celery import shared_task
from django.utils import timezone
from .models import Message, MessageEvent
from django.db import transaction

@shared_task
def expire_messages():
    msg = Message.objects.filter(
        is_expired=False,
        expires_at__lte=timezone.now()
    )

    with transaction.automic():
        msg.is_expired = True
        msg.save()
        MessageEvent.objects.create(
            message=msg,
            event_type="MESSAGE_EXPIRED"
        )