from django.shortcuts import render
from .serializers import Offer, OfferSerializer
from rest_framework import viewsets

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('-created_at')
    serializer_class = OfferSerializer

# 4. Recherche et filtrage des offres (Acheteurs)

class OfferSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all().order_by('-created_at')
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price', 'state', 'target', 'farmer']
    search_fields = ['description']
    ordering_fields = ['price', 'created_at']
