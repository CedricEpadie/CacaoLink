# messaging/urls.py

from django.urls import path
from .views import send_message, get_messages, mark_message_as_read

urlpatterns = [
    path('send/', send_message, name='send_message'),
    path('messages/<int:user_id>/', get_messages, name='get_messages'),
    path('messages/read/<int:message_id>/', mark_message_as_read, name='mark_message_as_read'),
]