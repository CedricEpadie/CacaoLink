# 5. Routes API
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'offers', views.OfferViewSet)  # CRUD pour agriculteurs
router.register(r'search_offers', views.OfferSearchViewSet)  # Recherche pour acheteurs

urlpatterns = [
    path('api/', include(router.urls)),
]


