# messaging/serializers.py

from rest_framework import serializers
from .models import Message, Conversation

class MessageSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'content', 'timestamp', 'is_read')

class ConversationSerializer(serializers.ModelSerializer):
   
    last_message = MessageSerializer(read_only=True)
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'last_message', 'updated_at']

    
    def get_participants(self, obj):
            return [participant.id for participant in obj.participants.all()]