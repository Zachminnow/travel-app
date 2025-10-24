from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Destination(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    country = models.CharField(max_length=200)
    description = models.TextField(
        help_text='Explain the center on attraction.')
    image = models.ImageField(upload_to='dest_pics/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'Destination'
        verbose_name_plural = 'Destinations'

    def __str__(self):
        return f"{self.name} , {self.country}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("destination_detail", kwargs={"slug": self.slug})


class Tour(models.Model):
    """Travel packages/ tours"""
    TOUR_TYPES = [
        ('adventure', 'Adventure'),
        ('beach', 'Beach'),
        ('cultural', 'Cultural'),
        ('family', 'Family'),
        ('luxury', 'Luxury'),
        ('budget', 'Budget'),
        ('honeymoon', 'Honeymoon'),
        ('group', 'Group Tour'),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='tours')
    tour_type = models.CharField(
        max_length=20, choices=TOUR_TYPES, default='adventure')
    description = models.TextField()
    currency = models.CharField(  # ADD THIS FIELD
        max_length=3,
        default='USD',
        choices=[
            ('USD', 'US Dollar'),
            ('EUR', 'Euro'),
            ('GBP', 'British Pound'),
            ('KES', 'Kenyan Shilling'),
            ('TZS', 'Tanzanian Shilling'),
            ('UGX', 'Ugandan Shilling'),
        ],
        help_text="3-letter currency code"
    )
    pricing = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    tour_organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    travel_guide = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200)
    duration_dates = models.PositiveIntegerField(default=1)
    available_from = models.DateField(default=timezone.now)
    available_until = models.DateField(default=timezone.now)
    max_participants = models.PositiveIntegerField(default=1)
    main_image = models.ImageField(upload_to='tour_pics')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Tour'
        verbose_name_plural = 'Tours'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tour_detail", kwargs={"slug": self.slug})
