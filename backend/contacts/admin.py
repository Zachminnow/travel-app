from django.contrib import admin
from .models import Contact, OfficeLocation


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'message', 'address']
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent']
    date_hierarchy = 'created_at'
    list_per_page = 25

    fieldsets = (
        ('Contact Information', {
            'fields': ('full_name', 'email', 'phone', 'address')
        }),
        ('Message Details', {
            'fields': ('message', 'status')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_contacted', 'mark_as_closed']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(status='read')
        self.message_user(request, f'{updated} contact(s) marked as read.')
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(status='contacted')
        self.message_user(
            request, f'{updated} contact(s) marked as contacted.')
    mark_as_contacted.short_description = "Mark selected as contacted"

    def mark_as_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} contact(s) marked as closed.')
    mark_as_closed.short_description = "Mark selected as closed"


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country', 'phone', 'is_active', 'order']
    list_filter = ['is_active', 'country', 'city']
    search_fields = ['name', 'city', 'country', 'address_line1']
    list_editable = ['order', 'is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'is_active', 'order')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'country')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email')
        }),
        ('Map Coordinates', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse', ),
            'description': 'Optional: Add coordinates for precise map markers'
        }),
    )
