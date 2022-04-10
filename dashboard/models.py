from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class FoodDonare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=12)
    address = models.CharField(max_length=400)
    food_details = models.TextField()
    donate_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user}"


class FoodAcceptor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=12)
    any_message = models.TextField()
    donate_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user}"


class Notification(models.Model):
    user = models.ForeignKey(
        User, related_name="notification", on_delete=models.CASCADE
    )
    notification = models.CharField(max_length=500, default=None)
    