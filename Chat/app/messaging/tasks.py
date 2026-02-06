from celery import shared_task
from django.utils import timezone
from app.accounts.models import Message, MessageEvent
from django.db import transaction

@shared_task
def expire_messages():
    messages = Message.objects.filter(
        is_expired=False,
        expires_at__lte=timezone.now()
    )

    with transaction.atomic():
        for message in messages:
            message.is_expired = True
            message.save(update_fields=["is_expired"])
    
            MessageEvent.objects.create(
                message=message,
                event_type="MESSAGE_EXPIRED"
            )