# from django.db import models
# from django.conf import settings
# from decimal import Decimal
# from django.urls import reverse
# from django.db.models import Sum, Q
# from datetime import timedelta
# from django.utils import timezone
# import logging

# logger = logging.getLogger('bookings')


# class BookingManager(models.Model):
#     """
#     LEARNING: Custom Manager - Adds reusable querysets
#     """

#     def upcoming(self):
#         """Get all upcoming bookings"""
#         return self.filter(
#             travel_time__gte=timezone.now().date(),
#             status__in=['pending', 'confirmed']
#         )

#     def past(self):
#         return self.filter(travel_date__lt=timezone.now().date())

#     def confirmed(self):
#         return self.filter(status='confirmed', payment_status='paid')

#     def pending_payment(self):
#         return self.filter(status='pending', payment_status='pending')

#     def for_user(self, user):
#         # Get bookings for specific user
#         return self.filter(user=user)

#     def revenue_by_month(self, year, month):
#         # Calculate revenue for a specific month
#         return self.filter(
#             created_at__year=year,
#             created_at__month=month,
#             payment_status='paid'
#         ).aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')


# class Booking(models.Model):
#     """
#     Main booking model
#     """

#     STATUS_CHOICES = [
#         ('draft', 'Draft'),
#         ('pending', 'Pending Confirmation'),
#         ('confirmed', 'Confirmed'),
#         ('cancelled', 'Cancelled'),
#         ('completed', 'Completed'),
#         ('refunded', 'Refunded'),
#     ]

#     PAYMENT_STATUS_CHOICES = [
#         ('pending', 'Payment Pending'),
#         ('processing', 'Processing'),
#         ('paid', 'Paid'),
#         ('failed', 'Payment Failed'),
#         ('refunded', 'Refunded'),
#         ('partial', 'Partially Paid'),
#     ]

#     objects = BookingManager()

#     # Reference
#     booking_reference = models.CharField(
#         max_length=20,
#         unique=True,
#         editable=False,
#         db_index=True
#     )
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE, related_name='bookings')
#     tour = models.ForeignKey(
#         'destinations.Tour', on_delete=models.PROTECT, related_name='bookings')
#     travel_date = models.DateField(db_index=True)
#     from django.core.validators import MinValueValidator, MaxValueValidator
#     num_adults = models.IntegerField(
#         validators=[MinValueValidator(1)],
#         default=1,
#         help_text='Number of adult travelers (18+)'
#     )
#     num_children = models.IntegerField(
#         validators=[MinValueValidator(0)],
#         default=0,
#         help_text='Number of children (2-17 years)'
#     )
#     num_infants = models.IntegerField(
#         validators=[MinValueValidator(0)],
#         default=0,
#         help_text='Number of infants (under 2 years)'
#     )

#     # pricing
#     price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
#     discount_amount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=Decimal('0.00')
#     )
#     tax_amount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=Decimal('0.00')
#     )
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)

#     coupon_code = models.CharField(max_length=50, blank=True)
#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='draft',
#         db_index=True
#     )
#     payment_status = models.CharField(
#         max_length=20,
#         choices=PAYMENT_STATUS_CHOICES,
#         default='pending',
#         db_index=True
#     )

#     special_requests = models.TextField(
#         blank=True,
#         help_text='Dietary requirements, accessibility needs, etc.'
#     )
#     internal_notes = models.TextField(
#         blank=True,
#         help_text='Internal staff notes'
#     )

#     contact_name = models.CharField(max_length=200)
#     contact_email = models.EmailField()
#     contact_phone = models.CharField(max_length=20)
#     emergency_contact = models.CharField(
#         max_length=200,
#         blank=True
#     )
#     emergency_phone = models.CharField(
#         max_length=20,
#         blank=True
#     )

#     booking_source = models.CharField(
#         max_length=50,
#         choices=[
#             ('website', 'Website'),
#             ('mobile', 'Mobile'),
#             ('phone', 'Phone Call'),
#             ('email', 'Email'),
#             ('agent', 'Travel Agent'),
#         ],
#         default='website'
#     )

#     ip_address = models.GenericIPAddressField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     confirmed_at = models.DateTimeField(null=True, blank=True)
#     cancelled_at = models.DateTimeField(null=True, blank=True)
#     completed_at = models.DateTimeField(null=True, blank=True)

#     expires_at = models.DateTimeField(null=True, blank=True)

#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = 'Booking'
#         verbose_name_plural = 'Bookings'
#         indexes = [
#             models.Index(fields=['booking_reference']),
#             models.Index(fields=['user', 'status']),
#             models.Index(fields=['travel_date', 'status']),
#             models.Index(fields=['created_at', 'payment_status']),
#         ]
#         permissions = [
#             ("view_all_bookings", "can view all bookings"),
#             ("cancel_any_booking", "Can cancel any booking"),
#             ("refund_booking", "Can process refunds"),
#         ]

#     def __str__(self):
#         return f"{self.booking_reference} - {self.user.username} - {self.tour.title}"

#     def save(self, *args, **kwargs):
#         is_new = self.pk is None

#         # Generate booking reference
