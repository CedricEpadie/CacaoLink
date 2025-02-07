import json
import time
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Récupère l'ID de l'utilisateur connecté
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            # Crée un groupe pour l'utilisateur
            self.room_group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Retire l'utilisateur du groupe
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Reçoit un message du WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        receiver_id = data['receiver_id']
        content = data['content']

        # Enregistre le message dans la base de données
        receiver = await User.objects.aget(id=receiver_id)
        message = await Message.objects.acreate(
            sender=self.user,
            receiver=receiver,
            content=content
        )

        # Récupérer ou créer la conversation
        conversation, created = await sync_to_async(Conversation.objects.get_or_create)(
            participants__in=[self.user, receiver]
        )
        if created:
            conversation.participants.add(self.user, receiver)

        conversation.last_message = message
        conversation.updated_at = time.time()
        await sync_to_async(conversation.save)()

        # Envoie le message au destinataire via WebSocket
        await self.channel_layer.group_send(
            f"user_{receiver_id}",
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'sender': self.user.username,
                    'content': content,
                    'timestamp': str(message.timestamp),
                }
            }
        )

    # Envoie un message au WebSocket
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))