from django.shortcuts import render
from django.db import models
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model


# Create your views here.
# messaging/views.py

User = get_user_model()

@api_view(['POST'])
def send_message(request, user_id):
    try:
        receiver = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        # Assign the receiver to the message
        serializer.save(receiver=receiver, sender=User)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_messages(request, user_id):
    
    current_user = request.user

    messages = Message.objects.filter(
        (models.Q(sender=current_user) & models.Q(receiver_id=user_id)) |
        (models.Q(sender_id=user_id) & models.Q(receiver=current_user))
    )
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
def mark_message_as_read(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        return Response({'status': 'Message marked as read'}, status=status.HTTP_200_OK)
    except Message.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)