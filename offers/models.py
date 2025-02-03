from django.db import models
from auth_app.models import Agriculteurs

# 1. Gestion des utilisateurs (Agriculteurs & Acheteurs)

class Offer(models.Model):
    farmer = models.ForeignKey(Agriculteurs, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    state = models.CharField(max_length=50, choices=[('available', 'Disponible'), ('sold', 'Vendu')])
    target = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description[:20]} - {self.price} FCFA"

