from django.db import models
from accounts.models import CustomUser


class Destination(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(
        help_text='Explain the center on attraction.')
    total_pricing = models.DecimalField(
        max_digits=10, decimal_places=2, default='0.00')
    slots = models.PositiveIntegerField(default=0)
    country = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    pickup_date = models.DateField()
    drop_date = models.DateField()
    travel_guide = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='dest_pics')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Tours(models.Model):
    name = models.CharField(max_length=100)
    days = models.DateField()
    description = models.TextField('Exploration')
    tour = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='tours')
    image = models.ImageField(upload_to='tour_pics')

    def __str__(self):
        return self.name
