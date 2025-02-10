from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.
# messaging/models.py

User = get_user_model()

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    last_message = models.ForeignKey('Message', related_name='conversation_last_message', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation with {", ".join([str(participant) for participant in self.participants.all()])}'

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.content[:20]}...'