# auth_app/urls.py

from django.urls import path
from .views import register, login, profile

urlpatterns = [
    path('signup', register, name='register'),
    path('login', login, name='login'),
    path('profile/<int:user_id>/', profile, name='profile'),
]