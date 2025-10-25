from rest_framework import serializers
from .models import Contact, OfficeLocation
import re


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model"""

    class Meta:
        model = Contact
        fields = [
            'id', 'full_name', 'email', 'phone', 'address',
            'message', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def validate_full_name(self, value):
        """Validate full name field"""
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                'Name must be at least 2 characters long.')

        if len(value) > 100:
            raise serializers.ValidationError(
                'Name must not exceed 100 characters.')

        if not re.match(r"^[a-zA-Z\s'-]+$", value):
            raise serializers.ValidationError(
                'Name can only contact letters, spaces, hyphen and apostrophes.')

        return value

    def validate_phone(self, value):
        """Validate phone number field"""
        value = value.strip()

        if not re.match(r'^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$', value):
            raise serializers.ValidationError(
                'Please enter a valid phone number.')

        return value

    def validate_address(self, value):
        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError(
                'Address must be at least 5 characters long.')

        if len(value) > 200:
            raise serializers.ValidationError(
                'Address must not exceed 200 characters.')

        return value

    def validate_message(self, value):
        """Validate message field"""
        value = value.strip()

        if len(value) < 10:
            raise serializers.ValidationError(
                'Message must be at least 10 characters long.')

        if len(value) > 1000:
            raise serializers.ValidationError(
                'Message must not exceed 1000 characters.')

        return value


class ContactListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing contacts (admin)"""

    class Meta:
        model = Contact
        fields = ['id', 'full_name', 'email', 'phone', 'status', 'created_at']


class ContactStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating contact status"""

    class Meta:
        model = Contact
        fields = ['status']

    def validate_status(self, value):
        valid_statuses = ['new', 'read', 'contacted', 'closed']
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(valid_statuses)}")

        return value


class OfficeLocationSerializer(serializers.ModelSerializer):
    """Serializer for OfficeLocation model"""

    class Meta:
        model = OfficeLocation
        fields = [
            'id', 'name', 'address_line1', 'address_line2',
            'city', 'country', 'phone', 'email', 'latitude',
            'longitude', 'order'
        ]
