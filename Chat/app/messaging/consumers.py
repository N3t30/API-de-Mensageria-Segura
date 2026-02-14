import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser, User
from asgiref.sync import sync_to_async
from app.accounts.models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        print(f"Tentando conectar usuário: {self.user}")

        if not self.user or isinstance(self.user, AnonymousUser):
            print("Usuário não autenticado, fechando conexão")
            await self.close()
            return
        
        await self.accept()
        print(f"Usuário {self.user.username} conectado")

        self.group_name = f"user_{self.user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        print(f"Usuário {getattr(self, 'user', 'Unknown')} desconectado")

    async def receive(self, text_data):
        data = json.loads(text_data)

        recipient_username = data.get("recipient")
        content = data.get("content")

        if not recipient_username or not content:
            return

        recipient = await self.get_user(recipient_username)

        if not recipient:
            return

        await self.save_message(self.user, recipient, content)

        await self.channel_layer.group_send(
            f"user_{recipient.id}",
            {
                "type": "chat_message",
                "sender": self.user.username,
                "message": content,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "sender": event["sender"],
            "message": event["message"]
        }))

    @sync_to_async
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @sync_to_async
    def save_message(self, sender, recipient, content):
        return Message.objects.create(
            sender=sender,
            recipient=recipient,
            content=content
        )