from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import User
from asgiref.sync import database_sync_to_async

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtenez l'identifiant de l'utilisateur depuis l'URL (par exemple, user1_user2)
        user1 = self.scope['user'].username
        
        if not self.scope['user'].is_authenticated:
            await self.close()  # Fermer la connexion si l'utilisateur n'est pas authentifié
        
        user2 = self.scope['url_route']['kwargs']['peer']

        # Vérifier si user2 est un utilisateur valide
        try:
            peer_user = await database_sync_to_async(User.objects.get)(username=user2)
        except User.DoesNotExist:
            # Fermer la connexion si user2 n'existe pas et envoyer un message d'erreur
            await self.close()
            return  # Sortir de la méthode

        # Créer un nom de salle unique en triant les identifiants
        self.room_name = "_".join(sorted([user1, user2]))
        self.room_group_name = f'chat_{self.room_name}'

        # Rejoindre le groupe de la conversation
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accepter la connexion WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe de la conversation
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Recevoir le message du client
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']  # Optionnel : qui envoie le message
        
        # Envoyer le message au groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender  # Envoyer également l'expéditeur
            }
        )

    async def chat_message(self, event):
        # Recevoir le message envoyé au groupe
        message = event['message']
        sender = event['sender']  # Recevoir l'expéditeur

        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender  # Inclure l'expéditeur dans le message
        }))