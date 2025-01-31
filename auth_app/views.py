from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model, logout, login

from . import models
from . import serializers
from .backends import EmailBackend

User = get_user_model()
        
class RegisterViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegisterSerializer
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializers.UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        return User.objects.none()
    
class AgriculteurViewSet(viewsets.ModelViewSet):
    queryset = models.Agriculteurs.objects.all()
    serializer_class = serializers.AgriculteurSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def partial_update(self, request, *args, **kwargs):
        agriculteur = self.get_object()
        serializer = self.get_serializer(agriculteur, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcheteurViewSet(viewsets.ModelViewSet):
    queryset = models.Acheteurs.objects.all()
    serializer_class = serializers.AcheteurSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def partial_update(self, request, *args, **kwargs):
        acheteur = self.get_object()
        serializer = self.get_serializer(acheteur, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request):
        try:
            logout(request)
            return Response({"message": "Déconnexion réussie"}, status=200)
        except Exception:
            return Response({"error": "Token invalide"}, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = EmailBackend().authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_acheteur:
                return Response({'Redirect': 'acheteur'}, status=status.HTTP_200_OK)
            else:
                return Response({'Redirect': 'agriculteur'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'email ou mot de passe incorrect'}, status=status.HTTP_400_BAD_REQUEST)