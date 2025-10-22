# from django.db.models import Sum
from rest_framework import serializers
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
import logging
from .models import Booking, Payment, BookingParticipant, Review
from destinations.models import Tour
from destinations.serializers import TourListSerializer
# from accounts.models import CustomUser
from django.db import models

logger = logging.getLogger(__name__)


class BookingParticipantsSerializer(serializers.ModelSerializer):
    """Serializer for individuals booking participants"""

    class Meta:
        model = BookingParticipant
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'passport_number', 'nationality',
            'dietary_requirements', 'medical_conditions',
            'emergency_contact_name', 'emergency_contact_phone'
        ]

    def validate_email(self, value):
        """Validate email format"""
        if value and '@' not in value:
            raise serializers.ValidationError('Enter a valid email address.')
        return value

    def validate_date_of_birth(self, value):
        """Ensure date of birth is in the past"""
        if value and value >= timezone.now().date():
            raise serializers.ValidationError(
                "Date of birth must be in the past.")
        return value


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payment records"""
    formatted_amount = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'transaction_id', 'amount', 'currency', 'formatted_amount',
            'payment_method', 'payment_type', 'status', 'created_at',
            'processed_at'
        ]
        read_only_fields = [
            'id', 'transaction_id', 'created_at', 'processed_at'
        ]

    def get_formatted_amount(self, obj):
        return f"{obj.currency} {obj.amount:,.2f}"


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating payments"""

    class Meta:
        model = Payment
        fields = [
            'amount', 'payment_method', 'payment_type'
        ]

    def validate_amount(self, value):
        """Validate payment amount"""
        if value <= 0:
            raise serializers.ValidationError(
                "Payment amount must be positive.")
        raise value


class BookingListSerializer(serializers.ModelSerializer):
    """Lightweighht serializer for booking lists"""
    tour_title = serializers.CharField(source='tour.title', read_only=True)
    destination = serializers.CharField(
        source='tour.destination.name', read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(
        source='get_payment_status_display', read_only=True
    )
    total_price_formatted = serializers.SerializerMethodField()
    can_be_cancelled = serializers.BooleanField(read_only=True)
    days_until_tour = serializers.IntegerField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_reference', 'tour_title', 'destination',
            'num_participants', 'total_price_formatted', 'status',
            'status_display', 'payment_status', 'payment_status_display',
            'created_at', 'can_be_cancelled', 'days_until_tour'
        ]
        read_only_fields = [
            'id', 'booking_reference', 'created_at'
        ]

    def get_total_price_formatted(self, obj):
        return f"{obj.currency} {obj.total_price:,.2f}"


class BookingDetailSerializer(serializers.ModelSerializer):
    tour = TourListSerializer(read_only=True)
    tour_id = serializers.PrimaryKeyRelatedField(
        queryset=Tour.objects.all(),
        source='tour',
        write_only=True
    )
    user = serializers.SerializerMethodField()
    participants = BookingParticipantsSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    status_display = serializers.CharField(
        source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(
        source='get_payment_status_display',
        read_only=True
    )

    total_price_formatted = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    amount_remaining = serializers.SerializerMethodField()

    can_be_cancelled = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    days_until_tour = serializers.IntegerField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_reference', 'tour', 'tour_id', 'user',
            'num_participants', 'status', 'status_display', 'payment_status',
            'payment_status_display', 'total_price_formatted', 'total_paid',
            'amount_remaining', 'currency', 'contact_email', 'contact_phone',
            'special_requests', 'internal_notes', 'participants', 'payments',
            'created_at', 'updated_at', 'confirmed_at', 'cancelled_at',
            'can_be_cancelled', 'is_active', 'days_until_tour'
        ]
        read_only_fields = [
            'id', 'booking_reference', 'user', 'created_at', 'updated_at',
            'confirmed_at', 'cancelled_at', 'total_price_formatted',
            'total_paid', 'amount_remaining', 'payments', 'internal_notes'
        ]

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
        }

    def get_total_price_formatted(self, obj):
        return f"{obj.currency} {obj.total_price:,.2f}"

    def get_total_paid(self, obj):
        total = obj.payments.filter(
            status='completed'
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
        return f"{obj.currency} {total:,.2f}"

    def get_amount_remaining(self, obj):
        total_paid = obj.payments.filter(
            status='completed'
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
        remaining = obj.total_price - total_paid
        return f"{obj.currency} {remaining:,.2f}"


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer form creating bookings"""

    participants = BookingParticipantsSerializer(many=True, required=False)

    class Meta:
        model = Booking
        fields = [
            'tour', 'num_participants', 'contact_email', 'contact_phone',
            'special_requests', 'participants'
        ]

    def validate_tour(self, value):
        """Validate tour is available"""
        if not value.is_active:
            raise serializers.ValidationError(
                "This tour is not available for booking.")
        return value

    def validate(self, data):
        """Cross-field validation"""
        tour = data.get('tour')
        num_participants = data.get('num_participants')

        if tour and num_participants:
            # Check available spots
            booked_participants = Booking.objects.active().filter(
                tour=tour
            ).aggregate(
                total=models.Sum('num_participants')
            )['total'] or 0

            available_spots = tour.max_participants - booked_participants
            if num_participants > available_spots:
                raise serializers.ValidationError({
                    'num_participants': f'Only {available_spots} spots'
                    f'available.'
                })

            # Check if participants data matches count
            participants = data.get('participants', [])
            if participants and len(participants) != num_participants:
                raise serializers.ValidationError({
                    'participants': f'Number of participants '
                    f'({len(participants)}) '
                    f'must match num_participants ({num_participants}).'
                })
        return data

    @transaction.atomic
    def create(self, validated_data):
        """Create booking with parrticipants"""
        participants_data = validated_data.pop('participants', [])
        request = self.context.get('request')

        try:
            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                **validated_data
            )

            # Create participants
            for participant_data in participants_data:
                BookingParticipant.objects.create(
                    booking=booking, **participant_data)

            logger.info(
                f"Booking {booking.booking_reference} created successfully "
                f"by user {request.user.username}"
            )

            return booking
        except Exception as e:
            logger.error(f"Error creating booking: {e}", exc_info=True)
            raise


class BookingCancelSerializer(serializers.Serializer):
    """Serializer for cancelling bookings"""

    reason = serializers.CharField(required=False, allow_blank=True)

    def validate_reason(self, value):
        if value and len(value) < 5:
            raise serializers.ValidationError(
                "Cancellation reason must be atleast 5 characters."
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for tour reviews"""

    user_name = serializers.CharField(
        source='user.get_full_name', read_only=True)
    tour_title = serializers.CharField(source='tour.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'booking', 'tour', 'user_name', 'tour_title', 'rating',
            'title', 'comment', 'is_verified', 'is_approved', 'created_at'
        ]

    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5 stars.")
        return value

    def validate_title(self, value):
        """Validate review title"""
        if len(value) < 5:
            raise serializers.ValidationError(
                "Review title must be at least 5 characters."
            )
        return value

    def validate_comment(self, value):
        """Validate review comment"""
        if len(value) < 10:
            raise serializers.ValidationError(
                "Review comment must be atleast 10 characters."
            )
        return value

    def validate(self, data):
        booking = data.get('booking')
        if booking.status != Booking.BookingStatus.COMPLETED:
            raise serializers.ValidationError(
                "Can only review completed tours."
            )
        return data


class ReviewDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for reviews"""

    user_name = serializers.CharField(
        source='user.get_full_name', read_only=True)
    tour_title = serializers.CharField(source='tour.title', read_only=True)
    tour_destination = serializers.CharField(
        source='tour.destination.name', read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id', 'booking', 'tour', 'username', 'tour_title', 'tour_destination',
            'rating', 'title', 'comment', 'is_verified', 'is_approved', 'created_at',
            'updated_at'
        ]
        read_only_fields = fields


class BookingStatsSerializer(serializers.Serializer):
    """Serializer for booking statistics"""

    total_bookings = serializers.IntegerField()
    confirmed_bookings = serializers.IntegerField()
    pending_bookings = serializers.IntegerField()
    cancelled_bookings = serializers.IntegerField()
    completed_bookings = serializers.IntegerField()

    total_revenue = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False
    )
    average_booking_value = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )

    paid_bookings = serializers.IntegerField(required=False)
    unpaid_bookings = serializers.IntegerField(required=False)
    partial_payments = serializers.IntegerField(required=False)

    popular_tours = serializers.ListField(required=False)
    revenue_by_month = serializers.DictField(required=False)
