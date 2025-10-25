from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.throttling import AnonRateThrottle
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact, OfficeLocation
from .serializers import (
    ContactListSerializer,
    ContactSerializer,
    ContactStatusUpdateSerializer,
    OfficeLocationSerializer
)
import logging

logger = logging.getLogger(__name__)


class ContactSubmitThrottle(AnonRateThrottle):
    """Custom throttle for contact form submissions"""
    rate = '3/hour'
    scope = 'contact_submit'


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filterset_fields = ['status', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'message']
    ordering_fields = ['created_at', 'updated_at', 'full_name']

    def get_permissions(self):
        """Allow anyone to submit, but require admin for other actions"""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_throtles(self):
        """Apply throttling to create action"""
        if self.action == 'create':
            return [ContactSubmitThrottle()]
        return super().get_throttles()

    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'list':
            return ContactListSerializer
        elif self.action == 'update_status':
            return ContactStatusUpdateSerializer
        return ContactSerializer

    def create(self, request, *args, **kwargs):
        """Handle contact form submission"""
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # save contact with metadata
        contact = serializer.save(
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
        )

        # Send notification emails
        email_sent = self.send_notification_email(contact)

        return Response({
            'success': True,
            'message': 'Thank you for contacting us! We will get back to you within 24 hours.',
            'data': {
                'id': contact.id,
                'email_sent': email_sent
            }
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """List all contacts within filters"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'data': serializer.data
            })

    def retrieve(self, request, *args, **kwargs):
        """Rettrieve a specific contact"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        """Update only the status of a contact"""
        contact = self.get_object()
        serializer = ContactStatusUpdateSerializer(
            contact, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Status updated successfully',
                'data': ContactSerializer(contact).data
            })
        return Response({
            'success': False,
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        """Extract client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def send_notification_emails(self, contact):
        """Send email notifications to admin and customer"""
        try:
            admin_subject = 'New Contact Form Submission'
            admin_message = f"""
New Contact Form Submission

Name: {contact.full_name}
Email: {contact.email}
Phone: {contact.phone}
Address: {contact.address}

Message: {contact.message}

Submitted: {contact.created_at.strftime('%Y-%m-%d %H:%M:%S')}
IP Address: {contact.ip_address}
"""
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=True,
            )

            # Customer confirmation
            user_subject = 'Thank you for contacting us - Travola Agency'
            user_message = f"""
Dear {contact.full_name},

Thank you for your inquiry!

We have received your message and will getback to you within 24 hours.

Your message:
{contact.message}

Best regards,
Travola Agency Team

Phone: +1 234 567 890
Email: travolaagency@gmail.com
"""

            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [contact.email],
                fail_silently=True,
            )

            logger.info(f"Emails sent for contact submission: {contact.id}")
            return True
        except Exception as e:
            logger.error(f"Email sending error: {str(e)}")
            return False


class OfficeLocationViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for OfficeLocation model (read-only)"""

    queryset = OfficeLocation.objects.filter(is_active=True)
    serializer_class = OfficeLocationSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        """List all active office locations"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific location"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })
