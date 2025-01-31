from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
]
