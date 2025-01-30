from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

# Definition du nouveau manager d'utilisateur / Pour la creation des utilisateurs simple et des superuser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est requis")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

# Definition du nouvel utilisateur par défaut
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=11, blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='profile_pictures')
    is_acheteur = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
class Agriculteurs(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='agriculteurs')
    localisation = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'Agriculteur: {self.user.get_full_name()}'
    
class Acheteurs(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='acheteurs')
    type = models.CharField(
        max_length=50,
        choices=[
            ('entreprise', 'Entreprise'),
            ('particulier', 'Particulier'),
            ('ong', 'ONG')
        ],
        default='particulier'
    )
    
    def __str__(self):
        return f'Acheteur: {self.user.get_full_name()} ({self.type})'