from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

# Definition du noveau model backend pour l'authentification (On utilise l'email)
class EmailBackend(ModelBackend):
    def authenticate(self, request, email = None, password = None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None