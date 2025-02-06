from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'telephone', 'profile_picture', 'is_acheteur']
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'telephone', 'is_acheteur']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        if user.is_acheteur:
            models.Acheteurs.objects.create(user=user)
        else:
            models.Agriculteurs.objects.create(user=user)
            
        return user
            
class AgriculteurSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Agriculteurs
        fields = '__all__'
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for key, value in user_data.items():
                setattr(instance.user, key, value)
            instance.user.save()

        return super().update(instance, validated_data)

class AcheteurSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Acheteurs
        fields = '__all__'
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            for key, value in user_data.items():
                setattr(instance.user, key, value)
            instance.user.save()

        return super().update(instance, validated_data)