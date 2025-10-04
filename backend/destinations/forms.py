from django import forms
from .models import Destination, Tour
from django.core.exceptions import ValidationError


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = [
            'name', 'country', 'description', 'image', 'is_active',
        ]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise ValidationError(
                'Destination name must be atleast 3 characters long.')
        return name

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Image must not exceed 5MB.")
            return image


class ToursForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = [
            'title', 'destination', 'package_type', 'description',
            'duration_dates', 'available_from', 'available_until',
            'max_participants', 'main_image', 'created_at'
        ]

    def clean(self):
        cleaned_data = super().clean()
        available_from = cleaned_data.get('available_from')
        available_until = cleaned_data.get('available_until')

        if available_from and available_until:
            if available_until <= available_from:
                raise ValidationError({
                    'available_until': 'End date must be after start date.'
                })

        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise ValidationError('Price cannot be negative.')
        return price

    def clean_main_image(self):
        image = self.cleaned_data.get('main_image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Image file size must not exceed 5MB')
        return image
