from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    expiry_date = models.DateField()
    pickup_address = models.TextField()
    image = models.ImageField(upload_to='food_images/')


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    status_choices = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='pending')