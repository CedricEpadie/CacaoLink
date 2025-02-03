# 5. Routes API
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'offers', views.OfferViewSet, basename='offers')  # CRUD pour agriculteurs
router.register(r'search_offers', views.OfferSearchViewSet, basename='search_offers')  # Recherche pour acheteurs

urlpatterns = [
    path('', include(router.urls)),
]


