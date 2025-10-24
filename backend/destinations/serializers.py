from rest_framework import serializers
from .models import Destination, Tour
from django.utils import timezone
from accounts.models import CustomUser


class UserBasicSerializer(serializers.ModelSerializer):
    """Used when you need to show user info inside another serializer
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'full_name', 'phone_number']
        read_only_fields = ['id', 'username', 'email']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user profile endpoints"""
    full_name = serializers.SerializerMethodField()
    total_tours = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'full_name', 'date_joined', 'total_tours']
        read_only_fields = ['id', 'username', 'date_joined']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

    def get_total_tours(self, obj):
        return obj.tour_set.count()


class DestinationDetailSerializer(serializers.ModelSerializer):
    tour_count = serializers.SerializerMethodField()
    tours = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    featured_tours = serializers.SerializerMethodField()

    class Meta:
        model = Destination
        fields = ['id', 'name', 'slug', 'country', 'description', 'image_url',
                  'created_at', 'tour_count', 'tours',
                  'is_active', 'featured_tours']

        read_only_fields = ['id', 'slug', 'created_at', 'is_featured']

    def get_tour_count(self, obj):
        return obj.tours.count()

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_tours(self, obj):
        """Use TourListSerializer to avoid circular imports"""
        tours = obj.tours.all()[:10]
        return TourListSerializer(tours, many=True, context=self.context).data

    def get_featured_tours(self, obj):
        tours = obj.tours.all()
        return TourListSerializer(tours, many=True, context=self.context).data


class DestinationListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views"""
    image_url = serializers.SerializerMethodField()
    tour_count = serializers.SerializerMethodField()

    class Meta:
        model = Destination
        fields = ['id', 'name', 'slug', 'country', 'description', 'image_url',
                  'is_active', 'is_featured', 'tour_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_tour_count(self, obj):
        return obj.tours.count()

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class DestinationCreateUpdateSerializer(serializers.ModelSerializer):
    """use this for: POST /api/destinations/, PUT /api/destinations/{slug}/"""
    class Meta:
        model = Destination
        fields = [
            'name', 'country', 'description', 'image', 'is_active'
        ]

    def validate_name(self, value):
        """ensures name is atleast 3 char"""
        if len(value) < 3:
            raise serializers.ValidationError(
                "Destination ,ust be atleast 3 characters long."
            )
        return value

    def validate_image(self, value):
        """Check file size and type"""
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(
                    "Image file size cannot exceed 5MB."
                )

            # Check file type
            allowed_type = ['image/jpeg', 'image/png',
                            'image/jpg', 'image/webp']
            if value.content_type not in allowed_type:
                raise serializers.ValidationError(
                    "Only JPEG, PNG, and Webp images are allowed."
                )

        return value

# TOUR SERIALIZERS


class TourListSerializer(serializers.ModelSerializer):
    """Use this for: /api/tours/"""
    destination_name = serializers.CharField(
        source='destination.name', read_only=True)
    destination_country = serializers.CharField(
        source='destination.country', read_only=True)
    organizer_name = serializers.CharField(
        source='tour_organizer.username', read_only=True)
    image_url = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    days_until_start = serializers.SerializerMethodField()

    pricing = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    currency = serializers.CharField(max_length=3, read_only=True)

    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'slug', 'destination_name', 'destination_country',
            'tour_type', 'location', 'duration_dates', 'available_from',
            'available_until', 'max_participants', 'image_url', 'description',
            'organizer_name', 'is_available', 'days_until_start', 'created_at',
            'pricing', 'currency'
        ]
        read_only_fields = ['id', 'slug', 'created_at']

    def get_image_url(self, obj):
        """Return full image url"""
        if obj.main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.main_image.url)
            return obj.main_image.url
        return None

    def get_is_available(self, obj):
        """Compares date with today"""
        today = timezone.now().date()
        return obj.available_from <= today <= obj.available_until

    def get_days_until_start(self, obj):
        today = timezone.now().date()
        delta = obj.available_from - today
        return delta.days if delta.days > 0 else 0


class TourDetailSerializer(serializers.ModelSerializer):
    """Use this for: /api/tours/{slug}/ (single tour)
    """
    destination = DestinationListSerializer(read_only=True)
    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all(),
        source='destination',
        write_only=True
    )
    organizer = UserBasicSerializer(source='tour_organizer', read_only=True)
    image_url = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    days_until_start = serializers.SerializerMethodField()
    days_until_end = serializers.SerializerMethodField()
    spots_remaining = serializers.SerializerMethodField()

    pricing = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    currency = serializers.CharField(max_length=3, read_only=True)
    formatted_price = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ['id', 'title', 'slug', 'destination', 'destination_id',
                  'tour_type', 'description', 'organizer', 'travel_guide',
                  'location', 'duration_dates', 'available_from',
                  'available_until', 'max_participants', 'image_url',
                  'is_available', 'days_until_start', 'days_until_end',
                  'spots_remaining', 'created_at', 'pricing', 'currency',
                  'formatted_price']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_image_url(self, obj):
        if obj.main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.main_image.url)
            return obj.main_image.url
        return None

    def get_is_available(self, obj):
        today = timezone.now().date()
        return obj.available_from <= today <= obj.available_until

    def get_days_until_start(self, obj):
        today = timezone.now().date()
        delta = obj.available_from - today
        return delta.days if delta.days > 0 else 0

    def get_days_until_end(self, obj):
        today = timezone.now().date()
        delta = obj.available_until - today
        return delta.days if delta.days > 0 else 0

    def get_spots_remaining(self, obj):
        return obj.max_participants

    def get_formatted_price(self, obj):
        """Return price with currency symbol"""
        if obj.pricing:
            return f"{obj.currency} {obj.pricing:,.2f}"
        return None


class TourCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = [
            'title', 'destination', 'tour_type', 'description', 'travel_guide',
            'location', 'duration_dates', 'available_from', 'available_until',
            'max_participants', 'main_image', 'pricing', 'currency'
        ]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Tour title must be atleast 5 characters long."
            )
        return value

    def validate_duration_dates(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Duration must be atleast 1 day."
            )
        return value

    def validate_max_participants(self, value):
        # validate max_participants
        if value < 1:
            raise serializers.ValidationError(
                "Must allow at least 1 participant."
            )
        if value > 100:
            raise serializers.ValidationError(
                "Maximum of 100 participants allowed."
            )
        return value

    def validate_price(self, value):
        """Validate price is positive"""
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Price must be greator than 0."
            )
        return value

    def validate_currency(self, value):
        """Validate currency code"""
        allowed_currencies = ['USD', 'EUR', 'GBP', 'KES', 'TZS', 'UGX']
        if value and value not in allowed_currencies:
            raise serializers.ValidationError(
                f"Currency must be one of: {', '.join(allowed_currencies)}"
            )
        return value

    def validate(self, data):
        # Validates relationships between fields
        available_from = data.get('available_from')
        available_until = data.get('available_until')

        if available_from and available_until:
            # Check if end date is after start date
            if available_until <= available_from:
                raise serializers.ValidationError({
                    'available_until': 'End date must be after start date.'
                })

            # Check if start date is not in the past
            if available_from < timezone.now().date():
                raise serializers.ValidationError({
                    'available_from': 'start date cannot be in the past.'
                })

            # Check if duration matches data range
            duration = data.get('duration_dates')
            if duration:
                date_range = (available_until - available_from).days + 1
                if duration > date_range:
                    raise serializers.ValidationError({
                        'duration_dates': f'Duration ({duration} days) exceeds'
                        'available data range ({date_range} days).'
                    })
        return data

    def create(self, validated_data):
        # Automatically set tour_organizer to current user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['tour_organizer'] = request.user
        return super().create(validated_data)


class DestinationsWithToursSerializer(serializers.ModelSerializer):
    # Showing destinations with all its tours
    tours = TourListSerializer(many=True, read_only=True)
    tour_count = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'country', 'description', 'image_url',
            'is_featured', 'tour_count', 'tours'
        ]

    def get_tour_count(self, obj):
        return obj.tours.count()

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class TourSearchSerializer(serializers.ModelSerializer):
    """Optimized serializer for search results
    Minimal fields for fast responses
    """
    destination_name = serializers.CharField(
        source='destination.name', read_only=True)
    image_url = serializers.SerializerMethodField()

    formatted_price = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'slug', 'destination_name', 'tour_type', 'location',
            'duration_dates', 'image_url', 'formatted_price'
        ]

    def get_formatted_price(self, obj):
        if obj.pricing:
            return f"{obj.currency} {obj.pricing:,.2f}"
        return None

    def get_image_url(self, obj):
        if obj.main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.main_image.url)
            return obj.main_image.url
        return None


class DestinationStatsSerializer(serializers.Serializer):
    total_destinations = serializers.IntegerField()
    active_destinations = serializers.IntegerField()
    featured_destinations = serializers.IntegerField()
    total_tours = serializers.IntegerField()
    countries = serializers.ListField(child=serializers.CharField())


class TourStatsSerializer(serializers.Serializer):
    """Statistics for tours"""
    total_tours = serializers.IntegerField()
    tours_by_type = serializers.DictField()
    available_tours = serializers.IntegerField()
    upcoming_tours = serializers.IntegerField()

    average_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False)
    price_range = serializers.DictField(required=False)
