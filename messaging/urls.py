# messaging/urls.py

from django.urls import path
from .views import send_message, get_messages, mark_message_as_read, delete_message, get_conversations

urlpatterns = [
    path('<int:chat_id>/messages/send/', send_message, name='send_message'),
    path('<int:chat_id>/messages/read/', get_messages, name='get_messages'),
    path('<int:chat_id>/messages/<int:message_id>/mark_as_read/', mark_message_as_read, name='mark_message_as_read'),
    path('<int:chat_id>/messages/<int:message_id>/delete/', delete_message, name='delete_message'),
    path('', get_conversations, name='get_conversations')
]