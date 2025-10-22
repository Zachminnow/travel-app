from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
import logging
import uuid

from accounts.models import CustomUser
from destinations.models import Tour

logger = logging.getLogger(__name__)


class BookingQuerySet(models.QuerySet):
    """Custom queryset for common booking filters"""

    def confirmed(self):
        return self.filter(status='confirmed')

    def pending(self):
        return self.filter(status='pending')

    def completed(self):
        return self.filter(status='completed')

    def active(self):
        # Bookings that are confirmed or pending
        return self.filter(status__in=['confirmed', 'pending'])

    def for_user(self, user):
        return self.filter(status__in=['confirmed', 'pending'])

    def for_tour(self, tour):
        return self.filter(tour=tour)

    def upcoming(self):
        return self.filter(
            tour__available_from__gt=timezone.now().date(),
            status__in=['confirmed', 'pending']
        )


class BookingManager(models.Manager):
    """Custom manager for booking model"""

    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db)

    def confirmed(self):
        return self.get_queryset().confirmed()

    def pending(self):
        return self.get_queryset().pending()

    def active(self):
        return self.get_queryset().active()

    def create_booking(self, user, tour, num_participants, **kwargs):
        """Create a booking with validation"""
        try:
            booking = self.create(
                user=user,
                tour=tour,
                num_participants=num_participants,
                **kwargs
            )
            logger.info(
                f"Booking created: {booking.booking_reference} "
                f"for user {user.username} on tour {tour.title}"
            )
            return booking

        except Exception as e:
            logger.error(f"Failed to create booking: {e}", exc_info=True)
            raise


class Booking(models.Model):
    """Main booking model for tour reservations"""

    class BookingStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        CONFIRMED = 'confirmed', _('Confirmed')
        CANCELLED = 'cancelled', _('Cancalled')
        COMPLETED = 'completed', _('Completed')
        REFUNDED = 'refunded', _('Refunded')

    class PaymentStatus(models):
        UNPAID = 'unpaid', _('Unpaid')
        PARTIAL = 'partial', _('Partially Paid')
        PAID = 'paid', _('Paid')
        REFUNDED = 'refunded', _('Refunded')

    # Primary fields
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    booking_reference = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        db_index=True,
        help_text="Unique booking reference number"
    )

    # Relationships
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="User who made the booking"
    )
    tour = models.ForeignKey(
        Tour,
        on_delete=models.PROTECT,
        related_name='bookings',
        help_text="Tour being booked"
    )

    # Booking details
    num_participants = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of participants"
    )

    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
        db_index=True
    )
    PaymentStatus = models.CharField(
        max_length=20,
        choices=BookingStatus.PENDING,
        default=PaymentStatus.UNPAID,
        db_index=True
    )

    # Pricing
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Total booking price"
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="Currency code (ISO 4217)"
    )

    # Contact information (can differ from user profile)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

    special_request = models.TextField(
        blank=True,
        help_text="Any special requests or dietary requirements"
    )
    internal_notes = models.TextField(
        blank=True,
        help_text="Internal notes (not visible to customer)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    # Cancellation details
    cancellation_reason = models.TextField(blank=True)
    cancelled_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cancelled_bookings'
    )

    objects = BookingManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['tour', 'status']),
            models.Index(fields=['booking_reference']),
        ]
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')

    def __str__(self):
        return f"{self.booking_reference} - {self.user.username} - {self.tour.title}"

    def save(self, *args, **kwargs):
        # Generate booking reference if new
        if not self.booking_reference:
            self.booking_reference = self._generate_booking_reference()

        # Calculate total price if not set
        if not self.total_price:
            self.total_price = self.calculate_total_price()

        # Set contact info from user if not provided
        if not self.contact_email:
            self.contact_email = self.user.email
        if not self.contact_phone and hasattr(self.user, 'phone_number'):
            self.contact_phone = self.user.phone_number or ''

        super().save(*args, **kwargs)

    def clean(self):
        """Validate booking data"""
        super().clean()

        if not self.tour.is_active:
            raise ValidationError(
                "Cannot book tours that have already started.")

        if self.num_participants > self.tour.max_participants:
            raise ValidationError(
                f"Number of participants exceeds tour capacity "
                f"{self.tour.max_participants}"
            )

        if hasattr(self, 'pk') and self.pk:
            other_bookings = self.tour.bookings.active().exclude(pk=self.pk)
        else:
            other_bookings = self.tour.bookings.active()

        total_booked = sum(b.num_participants for b in other_bookings)
        available_spots = self.tour.max_participants - total_booked

        if self.num_participants > available_spots:
            raise ValidationError(
                f"Only {available_spots} spots remaining for this tour."
            )

    def calculate_total_price(self):
        """Calculate the total price based on tour pricing and participants"""
        if not self.tour.pricing:
            return Decimal('0.00')
        return self.tour.pricing * self.num_participants

    def _generate_booking_reference(self):
        """Generate unique booking reference"""
        import random
        import string

        prefix = 'BK'
        while True:
            date_part = timezone.now().strftime('%Y%m%d')
            random_part = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=4))
            reference = f"{prefix}-{date_part}-{random_part}"

            if not Booking.objects.filter(booking_reference=reference).exists():
                return reference

    def confirm(self, save=True):
        """Confirm the booking"""
        if self.status == self.BookingStatus.PENDING:
            self.status = self.BookingStatus.CONFIRMED
            self.confirmed_at = timezone.now()
            if save:
                self.save()
            logger.info(f"Booking {self.booking_reference} confirmed")
            return True
        logger.warning(
            f"Cannot confirm booking {self.booking_reference} "
            f"with status {self.status}"
        )
        return False

    def cancel(self, reason='', cancelled_by=None, save=True):
        """Cancel the booking"""
        if self.status in [self.BookingStatus.CONFIRMED,
                           self.BookingStatus.PENDING]:
            self.status = self.BookingStatus.CANCELLED
            self.cancelled_at = timezone.now()
            self.cancellation_reason = reason
            self.cancelled_by = cancelled_by or self.user
            if save:
                self.save()
            logger.info(
                f"Booking {self.booking_reference} cancelled. Reason: {reason}"
            )
            return True
        logger.warning(
            f"Cannot cancel booking {self.booking_reference} "
            f"with status {self.status}"
        )
        return False

    def complete(self, save=True):
        """Mark booking as completed after tour ends"""
        if self.status == self.BookingStatus.CONFIRMED:
            self.status = self.BookingStatus.COMPLETED
            if save:
                self.save()
            logger.info(
                f"Booking {self.booking_reference} marked as completed")
            return True
        return False

    @property
    def is_active(self):
        """Check if booking is active"""
        return self.status in [self.BookingStatus.PENDING,
                               self.BookingStatus.COMPLETED]

    @property
    def can_be_cancelled(self):
        """Check if booking can be cancelled"""
        if self.status not in [self.BookingStatus.CONFIRMED,
                               self.BookingStatus.PENDING]:
            return False

        days_until_tour = (self.tour.available_from -
                           timezone.now().date()).days
        return days_until_tour >= 2

    @property
    def days_until_tour(self):
        delta = self.tour.available_from - timezone.now().date()
        return max(0, delta.days)


class Payment(models.Model):
    """Payment trnasactions for bookings"""

    class PaymentMethod(models.TextChoices):
        CARD = 'card', _('Credit/Debit Card')
        MPESA = 'mpesa', _('M-Pesa')
        PAYPAL = 'paypal', _('Paypal')
        BANK_TRANSFER = 'bank_transfer', _('Bank Transfer')
        CASH = 'cash', _('Cash')

    class PaymentType(models.TextChoices):
        FULL = 'full', _('Full Payment')
        DEPOSIT = 'deposit', _('Deposit')
        BALANCE = 'balance', _('Balance Payment')
        REFUND = 'refund', _('Refund')

    class TransactionStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PROCESSING = 'processing', _('Processing')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')
        REFUNDED = 'refunded', _('Refunded')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Payment gateway transaction ID"
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices)
    payment_type = models.CharField(max_length=20,
                                    choices=PaymentMethod.choices,
                                    default=PaymentType.FULL)
    status = models.CharField(max_length=20, choices=PaymentType.choices,
                              default=TransactionStatus.PENDING, db_index=True)

    gateway_response = models.JSONField(
        blank=True,
        null=True,
        help_text="Raw response from payment gateway"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['booking', 'status']),
        ]
        verbose_name = _('Payment')
        verbose_name_plural = _('payment')

    def __str__(self):
        return f"{self.transaction_id} - {self.booking.booking_reference} - {self.amount}"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self._generate_transaction_id()
        super().save(*args, **kwargs)
        logger.debug(
            f"Payment {self.transaction_id} saved with status {self.status}"
        )

    def _generate_transaction_id(self):
        import random
        import string

        prefix = 'TXN'
        while True:
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            random_part = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=6))
            txn_id = f"{prefix}-{timestamp}-{random_part}"

            if not Payment.objects.filter(transaction_id=txn_id).exists():
                return txn_id

    def mark_completed(self, save):
        """Mark payment as completed"""
        self.status = self.TransactionStatus.COMPLETED
        self.processed_at = timezone.now()
        if save:
            self.save()

        self._update_booking_payment_status()
        logger.info(
            f"Payment {self.transaction_id} completed for booking "
            f"{self.booking.booking_reference}"
        )

    def mark_failed(self, save=True):
        """Mark payment as failed"""
        self.status = self.TransactionStatus.FAILED
        self.processed_at = timezone.now()
        if save:
            self.save()
        logger.warning(
            f"Payment {self.transaction_id} failed for booking "
            f"{self.booking.booking_reference}"
        )

    def _update_booking_payment_status(self):
        """Update booking payment status based on payments"""
        total_paid = self.booking.payments.filter(
            status=self.TransactionStatus.COMPLETED
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')

        if total_paid >= self.booking.total_price:
            self.booking.PaymentStatus = Booking.PaymentStatus.PAID
        elif total_paid > 0:
            self.booking.PaymentStatus = Booking.PaymentStatus.PARTIAL
        else:
            self.booking.PaymentStatus = Booking.PaymentStatus.UNPAID

        self.booking.save()


class BookingParticipant(models.Model):
    """Individual participants in a booking"""

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Travel documents
    passport_number = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=100, blank=True)

    detary_requirements = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['booking', 'last_name', 'first_name']
        verbose_name = _('Booking Participants')
        verbose_name_plural = _('Booking Participants')

    def __str__(self):
        return f"{self.first_name} {self.last_name} -"
        "{self.booking.booking_reference}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Review(models.Model):
    """Customer reviews for completed tours"""
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='review'
    )
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()

    # Review moderation
    is_verified = models.BooleanField(
        default=False,
        help_text="Approved for public display"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tour', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        unique_together = ['booking', 'tour']

    def __str__(self):
        return f"{self.user.username} - {self.tour.title} - {self.rating}★"

    def save(self, *args, **kwargs):
        # Auto-verify if booking is confirmed/completed
        if self.booking.status in [Booking.BookingStatus.CONFIRMED,
                                   Booking.BookingStatus.COMPLETED]:
            self.is_verified = True

        super().save(*args, **kwargs)
        logger.info(
            f"Review created by {self.user.username} for tour"
            "{self.tour.title}"
            f"with rating {self.rating}"
        )
