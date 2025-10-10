import logging
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny
)
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Count, Prefetch

from .models import Destination, Tour
from .serializers import (DestinationListSerializer, DestinationDetailSerializer,
                          DestinationCreateUpdateSerializer, DestinationsWithToursSerializer,
                          TourListSerializer, TourDetailSerializer, TourCreateUpdateSerializer,
                          TourSearchSerializer, DestinationStatsSerializer, TourStatsSerializer)

logger = logging.getLogger('travel')


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Anyone can view (GET) but only owner can edit"""

    def has_object_permission(self, request, view, obj):
        # read permissions for anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if obj has tour_organizer
        if hasattr(obj, 'tour_organizer'):
            return obj.tour_organizer == request.user
        return False


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description', 'country']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    filterset_fields = ['country', 'is_featured', 'is_active']

    def get_serializer_class(self):
        if self.action == 'list':
            return DestinationListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DestinationCreateUpdateSerializer
        elif self.action == 'with_tours':
            return DestinationsWithToursSerializer
        return DestinationDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action in ['list', 'retrieve']:
            queryset = queryset.prefetch_related(
                Prefetch('tours', queryset=Tour.objects.all())
            )

        queryset = queryset.annotate(tour_count=Count('tours'))

        # Filter by active status for non-staff users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)

        return queryset

    def list(self, request, *args, **kwargs):
        # Override list to add logging
        logger.info(
            f"Destinations list accessed",
            extra={
                'user': request.user.id if request.user.is_authenticated else 'anonymus',
                'action': 'destinations_list'
            }
        )
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(
            f"Destination viewed: {instance.name}",
            extra={
                'destination_id': instance.id,
                'user': request.user.id if request.user.is_authenticated else 'anonymous',
                'action': 'destination_detail'
            }
        )
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        logger.info(
            f"Destination created: {response.data.get('name')}",
            extra={
                'user': request.user.id,
                'action': 'destination_created'
            }
        )
        return response

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().update(request, *args, **kwargs)

        logger.info(
            f"Deatination updated: {instance.name}",
            extra={
                'destination_id': instance.id,
                'user': request.user.id,
                'action': 'destination_updated'
            }
        )
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Prevent deletion if destination has tours
        if instance.tour.exists():
            logger.warning(
                f"Deletion blocked: destination has tours",
                extra={
                    'destination_id': instance.id,
                    'user': request.user.id
                }
            )
            return Response(
                {'error': 'Cannot delete destination with existing tours'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.warning(
            f"Destination delete: {instance.name}",
            extra={
                'destination_id': instance.id,
                'user': request.user.id,
                'action': 'destination_deleted'

            }
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured destinations"""
        featured_destinations = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_destinations, many=True)

        logger.info(
            f"Featured destinations accessed",
            extra={'count': featured_destinations.count(),
                   'action': 'featured_destinations'}
        )
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def tours(self, request, slug=None):
        destination = self.get_object()
        tours = destination.tours.all()

        tour_type = request.query_params.get('type')
        if tour_type:
            tours = tours.filter(tour_type=tour_type)

        serializer = TourListSerializer(
            tours,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def statistics(self, request):
        total = Destination.objects.count()
        active = Destination.objects.filter(is_active=True).count()
        featured = Destination.objects.filter(is_featured=True).count()
        total_tours = Tour.objects.count()
        countries = Destination.objects.values_list(
            'country', flat=True).distinct()

        data = {
            'total_destinations': total,
            'active_destinations': active,
            'featured_destinations': featured,
            'total_tours': total_tours,
            'countries': list(countries)
        }

        serializer = DestinationStatsSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_country(self, request):
        from collections import defaultdict

        destinations = self.get_queryset()
        grouped = defaultdict(list)

        for dest in destinations:
            grouped[dest.country].append(
                DestinationListSerializer(
                    dest, context={'request': request}).data
            )
        return Response(dict(grouped))


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    lookup_field = 'slug'

    # Permissions
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'available',
                           'upcoming', 'by_type', 'search_tours']:
            permissions_classes = [AllowAny]
        elif self.action == 'create':
            permissions_classes = [IsAuthenticated]
        else:
            permissions_classes = [IsAuthenticated, IsOwnerOrReadOnly]

        return [permission() for permission in permissions_classes]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['tour_type', 'destination', 'tour_organizer']
    search_fields = ['title', 'description', 'location', 'destination_name']
    ordering_fields = ['created_at', 'available_from', 'duration_dates',
                       'max_participants']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return TourListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TourCreateUpdateSerializer
        elif self.action == 'search_tours':
            return TourSearchSerializer
        return TourDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.select_related(
            'destination',
            'tour_organizer'
        )

        # Filter by date range if provided
        available_from = self.request.query_params.get('available_from')
        available_until = self.request.query_params.get('available_until')

        if available_from:
            queryset = queryset.filter(available_from__gte=available_from)
        if available_until:
            queryset = queryset.filter(available_until__lte=available_until)

        return queryset

    def list(self, request, *args, **kwargs):
        logger.info(
            f"Tours list accessed",
            extra={
                'user': request.user.id if request.user.is_authenticated else 'anonymous',
                'action': 'tour_list'
            }
        )
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(
            f"Tour viewed: {instance.title}",
            extra={
                'tour_id': instance.id,
                'user': request.user.id if request.user.is_authenticated else 'anonymous',
                'action': 'tour_detail'
            }
        )
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # tour organizer
        self.perform_create(serializer)

        logger.info(
            f"Tour created: {serializer.data.get('title')}",
            extra={
                'user': request.user.id,
                'tour_id': serializer.instances.id,
                'action': 'tour_created'
            }
        )

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if user is the organizer
        if instance.tour_organizer != request.user:
            logger.warning(
                f"Unauthorized tour update attempt",
                extra={
                    'tour_id': instance.id,
                    'user': request.user.id,
                    'action': 'unauthorized_update'
                }
            )
            return Response(
                {'error': 'You can only edit your own tours'},
                status=status.HTTP_403_FORBIDDEN
            )
        response = super().update(request, *args, **kwargs)

        logger.info(
            f"Tour updated: {instance.title}",
            extra={
                'tour_id': instance.id,
                'user': request.user.id,
                'action': 'tour_updated'
            }
        )
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.tour_organizer != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only delete your own tours'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if tour has started
        if instance.available_from <= timezone.now().date():
            return Response(
                {'error': 'Cannot delete tours that have already started'},
                status=status.HTTP_404_BAD_REQUEST
            )

        logger.warning(
            f"Tour deleted: {instance.title}",
            extra={
                'tour_id': instance.id,
                'user': request.user.id,
                'action': 'tour_deleted'
            }
        )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def available(self, request):
        today = timezone.now().date()
        available = self.get_queryset().filter(
            available_from__lte=today,
            available_until__gte=today
        )

        serializer = self.get_serializer(available, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        today = timezone.now().date()
        upcoming = self.get_queryset().filter(
            available_from__gt=today
        ).order_by('available_from')

        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):

        from collections import defaultdict

        tours = self.get_queryset()
        grouped = defaultdict(list)

        for tour in tours:
            grouped[tour.tour_type].append(
                TourListSerializer(tour, context={'request': request}).data
            )
        return Response(dict(grouped))

    @action(detail=False, methods=['get'])
    def search_tours(self, request):
        queryset = self.get_queryset()

        query = request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query) |
                Q(destination__name__icontains=query)
            )

        tour_type = request.query_params.get('type')
        if tour_type:
            queryset = queryset.filter(tour_type=tour_type)

        # filter by max duration
        max_duration = request.query_params.get('max_duration')
        if max_duration:
            queryset = queryset.filter(duration_dates__lte=max_duration)

        # Filter by min/max participants
        min_participants = request.query_params.get('min_participants')
        if min_participants:
            queryset = queryset.filter(max_participants__gte=min_participants)

        serializer = TourSearchSerializer(
            queryset,
            many=True,
            context={'request': request}
        )

        logger.info(
            f"Tour search performed",
            extra={
                'query': query,
                'results_count': queryset.count(),
                'action': 'tour_search'
            }
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_tours(self, request):
        my_tours = self.get_queryset().filter(tour_organizer=request.user)
        serializer = self.get_serializer(my_tours, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total = Tour.objects.count()
        today = timezone.now().date()
        available = Tour.objects.filter(
            available_from__lte=today,
            available_until__gte=today
        ).count()
        upcoming = Tour.objects.filter(available_from__gt=today).count()

        # Tour by type
        tours_by_type = {}
        for tour_type, label in Tour.Tour_TYPES:
            tours_by_type[label] = Tour.objects.filter(
                tour_type=tour_type).count()

        data = {
            'total_tours': total,
            'available_tours': available,
            'upcoming_tours': upcoming,
            'tours_by_type': tours_by_type
        }

        serializer = TourStatsSerializer(data)
        return Response(serializer.data)
