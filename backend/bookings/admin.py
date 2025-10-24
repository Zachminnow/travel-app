from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Booking, Payment, BookingParticipant, Review
import logging

logger = logging.getLogger(__name__)


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['transaction_id', 'created_at', 'processing_at']
    fields = ['transaction_id', 'amount', 'currency', 'payment_method',
              'payment_type', 'status', 'created_at']
    can_delete = False


class BookingParticipationInline(admin.TabularInline):
    model = BookingParticipant
    extra = 1
    fields = ['first_name', 'last_name', 'email', 'phone_number',
              'dietary_requirements']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_reference', 'user_link', 'tour_link', 'num_participants',
        'status_badge', 'payment_status_badge', 'total_price_display',
        'created_at', 'days_until_tour_display'
    ]
    list_filter = [
        'status', 'payment_status', 'created_at', 'tour__tour_type',
        ('confirmed', admin.EmptyFieldListFilter),
    ]
    search_fields = [
        'booking_reference', 'user__username', 'user__email',
        'tour__title', 'contact_email'
    ]
    readonly_fields = [
        'id', 'booking_reference', 'created_at', 'updated_at',
        'confirmed_at', 'cancelled_at', 'total_price'
    ]

    fieldsets = (
        ('Booking Information', {
            'fields': (
                'id', 'booking_reference', 'user', 'tour', 'num_participants',
                'status', 'payment_status'
            )
        }),
        ('Pricing', {
            'fields': ('total_price', 'currency')
        }),
        ('Contact Details', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Additional Information', {
            'fields': ('special_requests', 'internal_notes'),
            'classes': ('collapse',)
        }),
        ('Cancellation', {
            'fields': (
                'cancellation_reason', 'cancelled_by', 'cancelled_at'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [BookingParticipationInline, PaymentInline]

    actions = ['confirm_bookings', 'cancel_bookings', 'mark_as_completed']

    def user_link(self, obj):
        url = reverse('admin:accounts_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'

    def tour_link(self, obj):
        url = reverse('admin:tours_type_change', args=[obj.tour.id])
        return format_html('<a href="{}">{}</a>', url, obj.tour.title)
    tour_link.short_description = 'Tour'

    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'confirmed': '#28A745',
            'cancelled': '#DC3545',
            'completed': '#6C757D',
            'refunded': '#17A2B8',
        }
        color = colors.get(obj.status, '#6C757D')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def payment_status_badge(self, obj):
        colors = {
            'unpaid': '#DC3545',
            'partial': '#FFA500',
            'paid': '#28A745',
            'refunded': '#17A2B8',
        }
        color = colors.get(obj.payment_status, '#6C757D')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment'

    def total_price_display(self, obj):
        return f"{obj.currency} {obj.total_price:,.2f}"
    total_price_display.short_description = 'Total Price'

    def days_until_tour_display(self, obj):
        days = obj.days_until_tour
        if days == 0:
            return format_html('<strong style="color: red;">Today</strong>')
        elif days < 7:
            return format_html(
                '<strong syle="color: orange;">{} days</strong>', days)
    days_until_tour_display.short_description = 'Days Until Tour'

    @admin.action(description='Confirm select bookings')
    def confirm_bookings(self, request, queryset):
        updated = 0
        for booking in queryset:
            if booking.confirm():
                updated += 1

        self.message_user(
            request,
            f"{updated} booking(s) successfully confirmed."
        )
        logger.info(
            f"Admin {request.user.username} confirmed {updated} bookings")

    @admin.action(description='Cancel selected bookings')
    def cancel_bookings(self, request, queryset):
        updated = 0

        for booking in queryset:
            if booking.cancel(reason='Cancelled by admin',
                              cancelled_by=request.user):
                updated += 1

        self.message_user(
            request,
            f"{updated} booking(s) successfully cancelled."
        )
        logger.info(
            f"Admin {request.user.username} completed {updated} bookings")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id', 'booking_link', 'amount_display', 'payment_method',
        'payment_method', 'payment_type', 'status_badge', 'created_at'
    ]
    list_filter = [
        'status', 'payment_method', 'payment_type', 'created_at'
    ]
    search_fields = [
        'transaction_id', 'booking__booking_reference',
        'booking__user__username'
    ]
    readonly_fields = [
        'id', 'transaction_id', 'created_at', 'processed_at',
        'gateway_response'
    ]

    fieldsets = (
        ('Transaction Details', {
            'fields': ('id', 'transaction_id', 'booking')
        }),
        ('Payment Information', {
            'fields': (
                'amount', 'currency', 'payment_method', 'payment_type',
                'status'
            )
        }),
        ('Gateway Details', {
            'fields': ('gateway_response',),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_completed', 'mark_as_failed']

    def booking_link(self, obj):
        url = reverse('admin:bookings_booking_change', args=[obj.booking.id])
        return format_html(
            '<a href="{}">{}</a>',
            url, obj.booking.booking_reference
        )
    booking_link.short_description = 'Booking'

    def amount_display(self, obj):
        return f"{obj.currency} {obj.amount:,.2f}"
    amount_display.description = 'Amount'

    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'processing': '#17A2B8',
            'completed': '#28A745',
            'failed': '#DC3545',
            'refunded': '#6C757D',
        }
        color = colors.get(obj.status, '#6C757D')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    @admin.action(description='Mark selected payments as failed')
    def mark_as_failed(self, request, queryset):
        updated = 0
        for payment in queryset.filter(status='pending'):
            payment.mark_failed()
            updated += 1

        self.message_user(
            request,
            f"{updated} payment(s) marked as completed."
        )
        logger.info(
            f"Admin {request.user.username} completed {updated} payments")

    @admin.action(description='Mark selected payments as completed')
    def mark_as_completed(self, request, queryset):
        updated = 0
        for payment in queryset.filter(status='pending'):
            payment.mark_completed()
            updated += 1

        self.message_user(
            request,
            f"{updated} payment(s) marked as completed."
        )
        logger.info(
            f"Admin {request.user.username} completed {updated} payments")


@admin.register(BookingParticipant)
class BookingParticipantAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'booking_link', 'email', 'phone_number',
        'dietary_requirements_preview', 'created_at'
    ]
    list_filter = ['created_at', 'booking__tour']
    search_fields = [
        'first_name', 'last_name', 'email', 'phone_number', 'passport_number',
        'booking__booking_reference'
    ]
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number',
                       'date_of_birth')
        }),
        ('Travel Documents', {
            'fields': ('passport_number', 'nationality'),
            'classes': ('collapse',)
        }),
        ('Health Dietary', {
            'fields': ('dietary_requirements', 'medical_conditions'),
            'classes': ('collapse',)
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone'),
            'classes': ('collapse',)
        }),
        ('Booking Information', {
            'fields': ('booking',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def booking_link(self, obj):
        url = reverse('admin:bookings_booking_change', args=[obj.booking.id])
        return format_html(
            '<a href="{}"></a>',
            url, obj.booking.booking_reference
        )
    booking_link.short_description = 'Booking'

    def dietary_requirements_preview(self, obj):
        if obj.dietary_requirements:
            preview = obj.dietary_requirements[:50]
            if len(obj.dietary_requirements) > 50:
                preview += '...'
            return preview
        return '-'
    dietary_requirements_preview.short_description = 'Dietary Requirements'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'rating_stars', 'user_link', 'tour_link', 'is_verified_badge',
        'is_approved_badge', 'created_at', 'tour__destination'
    ]
    search_fields = [
        'user__username', 'tour__title', 'title', 'comment',
        'booking__booking_reference'
    ]
    readonly_fields = ['created_at', 'updated_at', 'booking_link']

    fieldsets = (
        ('Review Information', {
            'fields': ('booking_link', 'tour', 'user', 'rating', 'title')
        }),
        ('Review Content', {
            'fields': ('comment',)
        }),
        ('Moderation', {
            'fields': ('is_verified', 'is_approved'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['approve_reviews', 'reject_reviews']

    def user_link(self, obj):
        url = reverse('admin:accounts_customuser_change', args=[obj.tour.id])
        return format_html(
            '<a href="{}">{}</a>',
            url, obj.user.username
        )
    user_link.short_description = 'User'

    def tour_link(self, obj):
        url = reverse('admin:tours_tour_change', args=[obj.tour.id])
        return format_html(
            '<a href"{}">{}</a>', url, obj.tour.title)
    tour_link.short_description = 'Tour'

    def booking_link(self, obj):
        url = reverse('admin:bookings_booking_change', args=[obj.booking.id])
        return format_html(
            '<a href"{}">{}</a>',
            url, obj.booking.booking_reference
        )
    booking_link.short_description = 'Booking Reference'

    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html(
            '<strong>{}</strong>', stars
        )
    rating_stars.short_description = 'Rating'

    def is_verified_badge(self, obj):
        if obj.is_verified:
            return format_html(
                '<span style="color: green; font-weight: bold;">'
            )
        return format_html(
            '<span style="color: gray;">Unverified</span>'
        )
    is_verified_badge.short_descripition = 'Verified'

    def is_approved_badge(self, obj):
        if obj.is_approved:
            return format_html(
                '<span style="color: green; font-weight: bold;">'
                '✓ Approved</span>'
            )
    is_approved_badge.short_description = 'Aproved'

    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(
            request,
            f"{updated} review(s) approved and will now be visible."
        )
        logger.info(
            f"Admin {request.user.username} approved {updated} reviews")

    @admin.action(description='Reject selected reviews')
    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(
            request,
            f"{updated} review(s) rejected."
        )
        logger.info(
            f"Admin {request.user.username} rejected {updated} reviews")
