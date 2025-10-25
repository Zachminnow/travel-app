from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """Form for contact submissions with validation"""

    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'phone', 'address', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Full name..',
                'required': True,
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Email address..',
                'required': True,
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Phone number..',
                'required': True,
                'autocomplete': 'tel',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Address..',
                'required': True,
                'autocomplete': 'street-address',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write message..',
                'rows': 5,
                'required': True,
            }),
        }

    def clean_full_name(self):
        """Validate full name fields"""
        name = self.cleaned_data.get('full_name', '').strip()

        if len(name) < 2:
            raise forms.ValidationError(
                'Name must be atleast 2 characters long.')

        if len(name) > 100:
            raise forms.ValidationError('Name must not exceed 100 characters.')

        if not re.match(r"^[a-zA-Z\s'-]+$", name):
            raise forms.ValidationError('Name can only contain letters, spaces, '
                                        'hyphens, and apostrophes.')

        return name

    def clean_phone(self):
        """Validate phone number fields"""
        phone = self.cleaned_data.get('phone', '').strip()

        if not re.match(r'^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$', phone):
            raise forms.ValidationError(
                'Please enter a valid phone number (e.g., +1234567890 or 123-456-7890).')

        return phone

    def clean_address(self):
        """Validate address field"""
        address = self.cleaned_data.get('address', '').strip()

        if len(address) < 5:
            raise forms.ValidationError(
                'Address must be at least 5 characters long.')

        if len(address) > 200:
            raise forms.ValidationError(
                'Address must not exceed 200 characters.')

        return address

    def clean_message(self):
        """Validate message field"""
        message = self.cleaned_data.get('message', '').strip()

        if len(message) < 10:
            raise forms.ValidationError(
                'Message must be at least 10 characters long.')

        if len(message) > 1000:
            raise forms.ValidationError(
                'Message must not exceed 1000 characters.')

        return message
