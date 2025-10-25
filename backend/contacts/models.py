from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class Contact(models.Model):
    """Model for storing contact form submissions"""

    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('contacted', 'Contacted'),
        ('closed', 'Closed'),
    ]

    phone_regex = RegexValidator(
        regex=r'^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$',
        message="Phone number must be in valid format"
    )

    full_name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(
        validators=[EmailValidator()], verbose_name="Email Address")
    phone = models.CharField(
        validators=[phone_regex], max_length=20, verbose_name="Phone Number")
    address = models.CharField(max_length=200, verbose_name="Address")
    message = models.TextField(max_length=1000, verbose_name="Message")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new')

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.email}"


class OfficeLocation(models.Model):
    """Model for managing office locations"""

    name = models.CharField(max_length=100, verbose_name="Location Name")
    address_line1 = models.CharField(
        max_length=200, verbose_name="Address Line 1")
    address_line2 = models.CharField(
        max_length=200, blank=True, verbose_name="Address Line 2")
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Latitude for map marker"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Longitude for map marker"
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    order = models.IntegerField(
        default=0, help_text="Display order (lower numbers first)")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Office Location"
        verbose_name_plural = "Office Locations"

    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"
