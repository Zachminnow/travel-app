from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import logging
from .models import Booking, Payment, Review
from .serializers import (
    BookingListSerializer,
    BookingDetailSerializer,
    BookingCreateSerializer,
    BookingUpdateSerializer,
    BookingCancelSerializer,
    # BookingParticipantsSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
    ReviewSerializer,
    ReviewDetailSerializer,
    BookingStatsSerializer
)
# from destinations.models import Tour

logger = logging.getLogger(__name__)


class BookingPagination(PageNumberPagination):
    """Custom pagination for bookings"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class BookingViewSet(viewsets.ModelViewSet):
    pagination_class = BookingPagination
    queryset = Booking.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return BookingCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BookingUpdateSerializer
        elif self.action == 'cancel':
            return BookingCancelSerializer
        elif self.action == 'list':
            return BookingListSerializer
        return BookingDetailSerializer

    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['create', 'list', 'retrieve', 'cancel']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        """Regular users see only their bookings, admins see all"""
        user = self.request.user

        if user.is_staff:
            queryset = Booking.objects.all()
        else:
            queryset = Booking.objects.filter(user=user)

        queryset = queryset.select_related(
            'user', 'tour', 'tour__destination', 'cancelled_by'
        ).prefetch_related('participants', 'payments')

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        payment_status = self.request.query_params.get('payment_status')
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)

        tour_id = self.request.query_params.get('tour')
        if tour_id:
            queryset = queryset.filter(tour_id=tour_id)

        date_from = self.request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)

        date_to = self.request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(booking_reference__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__email__icontains=search) |
                Q(tour__title__icontains=search)
            )
        return queryset

    def create(self, request, *args, **kwargs):
        """Create a new booking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = serializer.save()

            logger.info(
                f"Booking created: {booking.booking_reference} by "
                "{request.user.username}"
            )

            detail_serializer = BookingDetailSerializer(
                booking, context={'request': request}
            )

            return Response(
                {
                    'success': True,
                    'message': 'Booking created successfully',
                    'booking': detail_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating booking: {e}", exc_info=True)
            return Response(
                {
                    'error': 'Failed to create booking',
                    'detail': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, *args, **kwargs):
        """Get booking details"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'success': True,
            'booking': serializer.data
        })

    def list(self, request, *args, **kwargs):
        """List bookings with metadata"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            response.data['meta'] = {
                'total_bookings': queryset.count(),
                'active_bookings': queryset.filter(
                    status__in=['pending', 'confirmed']
                ).count(),
                'completed_bookings': queryset.filter(
                    status='completed').count()
            }
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'count': queryset.count(),
            'bookings': serializer.data
        })

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()

        if booking.user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to cancel this booking'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not booking.can_be_cancelled:
            return Response(
                {
                    'error': 'Booking cannot be cancelled',
                    'detail': 'Cancellation deadline has passed or booking is '
                    'not active'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BookingCancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reason = serializer.validated_data.get('reason', '')

        if booking.cancel(reason=reason, cancelled_by=request.user):
            logger.info(
                f"Booking {booking.booking_reference} cancelled by "
                "{request.user.username}"
            )

            return Response({
                'success': True,
                'message': 'Booking cancelled successfully',
                'booking_reference': booking.booking_reference,
                'status': booking.status
            })
        return Response(
            {'error': 'Failed to cancel booking'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAdminUser])
    def confirm(self, request, pk=None):
        """Confirm a pending booking (Admin only)"""
        booking = self.get_object()

        if booking.confirm():
            logger.info(
                f"Booking {booking.booking_reference} confirmed by admin "
                "{request.user.username}"
            )

            return Response({
                'success': True,
                'message': 'Booking confirmed successfully',
                'booking_refernce': booking.booking_reference,
                'status': booking.status
            })
        return Response(
            {
                'error': 'Cannot confirm booking',
                'detail': f'Booking is currently {booking.status}'
            },
            status=HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAdminUser])
    def complete(self, request, pk=None):
        """Mark booking as completed (Admin only)"""
        booking = self.get_object()

        if booking.complete():
            logger.info(
                f"Booking {booking.booking_reference} marked as completed by "
                "{request.user.username}"
            )

            return Response({
                'success': True,
                'message': 'Booking marked as completed',
                'booking_reference': booking.booking_reference,
                'status': booking.status
            })
        return Response(
            {'error': 'Cannot complete booking'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get user's upcoming bookings"""
        queryset = self.get_queryset().filter(
            status__in=['pending', 'confirmed'],
            tour__available_from__gte=timezone.now().date()
        ).order_by('tour__available_from')

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'count': queryset.count(),
            'bookings': serializer.data
        })

    @action(detail=False, methods=['get'])
    def past(self, request):
        """Get user's past bookings"""
        queryset = self.get_queryset().filter(
            Q(status='completed') |
            Q(tour__available_until__lt=timezone.now().date())
        ).order_by('-tour__available_until')

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'count': queryset.count(),
            'bookings': serializer.data
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def stats(self, request):
        """Get booking statistics (Admin only)"""
        queryset = Booking.objects.all()
        now = timezone.now()

        stats = {
            'total_bookings': queryset.count(),
            'confirmed_bookings': queryset.confirmed().count(),
            'pending_bookings': queryset.pending().count(),
            'cancelled_bookings': queryset.cancelled().count(),
            'completed_bookings': queryset.completed().count(),

            'total_revenue': queryset.filter(
                payment_status='paid'
            ).aggregate(
                total=Sum('total_price')
            )['total'] or Decimal('0.00'),

            'average_booking_value': queryset.aggregate(
                avg=Avg('total_price'),
            )['avg'] or Decimal('0.00'),

            'paid_bookings': queryset.filter(
                payment_status='paid').count(),
            'unpaid_bookings': queryset.filter(
                payment_status='unpaid').count(),
            'partial_payments': queryset.filter(
                payment_status='partial').count(),

            'popular_tours': list(
                queryset.values('tour__title').annotate(
                    count=Count('id')
                ).order_by('-count')[:10]
            ),
            'revenue_by_month': {}
        }

        serializer = BookingStatsSerializer(stats)
        logger.info(f"Booking statistics retrieved by {request.user.username}")

        return Response({
            'success': True,
            'data': serializer.data
        })


class PaymentViewSet(viewsets.ModelViewSet):
    """Viewset for managing payments"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter payments based on user"""
        user = self.request.user

        if user.is_staff:
            return Payment.objects.all()

        return Payment.objects.filter(booking__user=user)

    def get_serializer_class(self):
        """Return appropriate serializer"""
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer

    def create(self, request, *args, **kwargs):
        booking_id = request.data.get('booking_id')

        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = Payment.objects.create(
            booking=booking,
            currency=booking.currency,
            **serializer.validated_data
        )
        logger.info(
            f"Payment {payment.transaction_id} created for booking "
            "{booking.booking_reference}"
        )

        return Response(
            {
                'success': True,
                'message': 'Payment initiated',
                'payment': PaymentSerializer(payment).data
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAdminUser])
    def mark_completed(self, request, pk=None):
        """Mark payment as completed"""
        payment = self.get_object()
        payment.mark_completed()

        logger.info(
            f"Payment {payment.transaction_id} marked as completed by "
            "{request.user.username}"
        )

        return Response({
            'success': True,
            'message': 'Payment marked as completed',
            'transaction_id': payment.transaction_id
        })

    @action(detail=True, methods=['post'], permission_classes=[
        permissions.IsAdminUser])
    def mark_failed(self, request, pk=None):
        """Mark payment failed"""
        payment = self.get_object()
        payment.mark_failed()

        logger.info(
            f"Payment {payment.transaction_id} marked as failed by "
            "{request.user.username}"
        )

        return Response({
            'success': True,
            'message': 'Payment marked as failed',
            'transaction_id': payment.transaction_id
        })


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.filter(is_approved=True).select_related(
            'user', 'tour', 'booking'
        )

        tour_id = self.request.query_params.get('tour')
        if tour_id:
            queryset = queryset.filter(tour_id=tour_id)

        rating = self.request.query_params.get('tour')
        if rating:
            queryset = queryset.filter(rating=rating)

        if self.request.user.is_staff:
            user_id = self.request.query_params.get('user')
            if user_id:
                queryset = queryset.filter(user_id=user_id)
        return queryset.order_by('-created_at')

    def get_serializer_class(self):
        """Return appropriate serializer"""
        if self.action == 'retrieve':
            return ReviewDetailSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        """Create review with current user"""
        serializer.save(user=self.request.user)
        logger.info(
            f"Review created by {self.request.user.username} for tour "
            "{serializer.instance.tour.title}"
        )
