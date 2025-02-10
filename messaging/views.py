import time
from django.shortcuts import render
from django.db import models
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from django.contrib.auth import get_user_model


# Create your views here.
# messaging/views.py

User = get_user_model()



@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_conversations(request):
        # Récupère toutes les conversations de l'utilisateur connecté
        conversations = Conversation.objects.filter(participants__in=[request.user]).order_by('-updated_at')
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, chat_id):
    receiver_id = request.data.get('receiver_id')
    content = request.data.get('content')

    if not content:
        return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content
    )

    conversation = Conversation.objects.get(id=chat_id)
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, receiver) 
    
    conversation.last_message = message
    conversation.updated_at = time.timezone.now()
    conversation.save()

    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, chat_id=None):
    # recupere tous les messages d'une conversation specifique
    conversation = Message.objects.get(id=chat_id)
    messages = conversation.messages.all().order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_message_as_read(request, chat_id=None, message_id=None):
    
    message = Message.objects.get(id=message_id)
    message.is_read = True
    message.save()
    serializer = MessageSerializer(message)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_message(request, chat_id=None, message_id=None):
    message = Message.objects.get(id=message_id)
    message.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)