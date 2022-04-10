from django.contrib import admin
from .models import FoodDonare, FoodAcceptor, Notification

# Register your models here.

admin.site.register(FoodDonare)
admin.site.register(FoodAcceptor)
admin.site.register(Notification)
