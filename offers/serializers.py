from rest_framework import serializers
from .models import Offer

# 3. CRUD sur des offres (Agriculteurs)

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
