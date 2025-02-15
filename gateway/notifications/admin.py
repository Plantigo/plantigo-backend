from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import UserNotification


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'user',
        'device_link',
        'severity_badge',
        'is_read',
        'created_at',
        'message_preview',
    ]
    list_filter = [
        'severity',
        'is_read',
        'created_at',
        'device',
        'user',
    ]
    search_fields = [
        'message',
        'device__name',
        'device__mac_address',
        'user__username',
        'user__email',
    ]
    readonly_fields = [
        'uuid',
        'created_at',
        'updated_at',
        'telemetry_details',
    ]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user',
            'device',
            'telemetry'
        )
    
    def device_link(self, obj):
        url = reverse('admin:devices_device_change', args=[obj.device.pk])
        return format_html('<a href="{}">{}</a>', url, obj.device.name)
    device_link.short_description = 'Device'
    device_link.admin_order_field = 'device__name'
    
    def severity_badge(self, obj):
        colors = {
            'info': '#17a2b8',
            'warning': '#ffc107',
            'critical': '#dc3545'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px;">{}</span>',
            colors.get(obj.severity, '#6c757d'),
            obj.severity.upper()
        )
    severity_badge.short_description = 'Severity'
    severity_badge.admin_order_field = 'severity'
    
    def message_preview(self, obj):
        max_length = 50
        if len(obj.message) > max_length:
            return f"{obj.message[:max_length]}..."
        return obj.message
    message_preview.short_description = 'Message'
    
    def telemetry_details(self, obj):
        return format_html(
            """
            <div style="padding: 10px; background-color: #f8f9fa; border-radius: 4px;">
                <h4 style="margin-top: 0;">Telemetry Data</h4>
                <p><strong>Temperature:</strong> {}°C</p>
                <p><strong>Humidity:</strong> {}%</p>
                <p><strong>Pressure:</strong> {} hPa</p>
                <p><strong>Soil Moisture:</strong> {}</p>
                <p><strong>Timestamp:</strong> {}</p>
            </div>
            """,
            obj.telemetry.temperature,
            obj.telemetry.humidity,
            obj.telemetry.pressure,
            obj.telemetry.soil_moisture,
            obj.telemetry.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        )
    telemetry_details.short_description = 'Telemetry Details'
    
    fieldsets = (
        (None, {
            'fields': ('uuid', 'user', 'device', 'severity', 'message')
        }),
        ('Telemetry Information', {
            'fields': ('telemetry_details',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'read_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
