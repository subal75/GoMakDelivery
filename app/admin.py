from django.contrib import admin
from .models import GomakDelivery, DeliveryAddress, ThirdPartyCourierService, Shipment

admin.site.register(GomakDelivery)
admin.site.register(DeliveryAddress)
admin.site.register(ThirdPartyCourierService)
admin.site.register(Shipment)
