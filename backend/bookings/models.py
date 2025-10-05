from django.db import models
from django.conf import settings
from decimal import Decimal
from django.urls import reverse
from django.db.models import Sum, Q
from datetime import timedelta
from django.utils import timezone
import logging

logger = logging.getLogger('bookings')


class BookingManager(models.Model):
    """
    LEARNING: Custom Manager - Adds reusable querysets
    """

    def upcoming(self):
        """Get all upcoming bookings"""
        return self.filter(
            travel_time__gte=timezone.now().date(),
            status__in=['pending', 'confirmed']
        )

    def past(self):
        return self.filter(travel_date__lt=timezone.now().date())

    def confirmed(self):
        return self.filter(status='confirmed', payment_status='paid')

    def pending_payment(self):
        return self.filter(status='pending', payment_status='pending')

    def for_user(self, user):
        # Get bookings for specific user
        return self.filter(user=user)

    def revenue_by_month(self, year, month):
        # Calculate revenue for a specific month
        return self.filter(
            created_at__year=year,
            created_at__month=month,
            payment_status='paid'
        ).aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')


class Booking(models.Model):
    """
    Main booking model
    """

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Payment Pending'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('failed', 'Payment Failed'),
        ('refunded', 'Refunded'),
        ('partial', 'Partially Paid'),
    ]

    objects = BookingManager()

    # Reference
    booking_reference = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        db_index=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='bookings')
    tour = models.ForeignKey(
        'destinations.Tour', on_delete=models.PROTECT, related_name='bookings')
    travel_date = models.DateField(db_index=True)
