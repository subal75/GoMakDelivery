from django.db import models
from django.contrib.auth.models import User


class GomakDelivery(models.Model):
    location_name = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius_km = models.FloatField(help_text="Delivery radius in kilometers")

    def __str__(self):
        return self.location_name


class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.location_name} ({self.pincode})"


class ThirdPartyCourierService(models.Model):
    name = models.CharField(max_length=100)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    client_secret = models.CharField(max_length=255, blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    api_url = models.URLField()
    webhook_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('pickup_scheduled', 'Pickup Scheduled'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courier_service = models.ForeignKey(ThirdPartyCourierService, on_delete=models.SET_NULL, null=True)
    tracking_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    pickup_address = models.TextField()
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id
