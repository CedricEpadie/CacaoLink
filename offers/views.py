from django.shortcuts import render
from models import Offer

from rest_framework import viewsets

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import serializers


# 3. CRUD sur des offres (Agriculteurs)

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'



class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('-created_at')
    serializer_class = OfferSerializer



# 4. Recherche et filtrage des offres (Acheteurs)

class OfferSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all().order_by('-created_at')
    serializer_class = OfferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price', 'state', 'target']
    search_fields = ['description']
    ordering_fields = ['price', 'created_at']
