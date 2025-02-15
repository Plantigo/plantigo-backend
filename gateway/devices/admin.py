from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Avg, Min, Max, Q, OuterRef, Subquery
from django.contrib.admin import SimpleListFilter

from .models import Device, Telemetry, DeviceSensorLimits
from django.utils.timezone import localtime


def format_metric(value, unit='', precision=1):
    """Helper function to format metric values with handling None."""
    if value is None:
        return '-'
    return f"{value:.{precision}f}{unit}"


class NumericRangeFilter(SimpleListFilter):
    parameter_name = 'range'
    title = 'range'  # będzie nadpisane w podklasach

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        self.field_name = self.parameter_name.replace('_range', '')

    def lookups(self, request, model_admin):
        return (
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        field_stats = queryset.aggregate(
            avg=Avg(self.field_name),
            std_dev=Max(self.field_name) - Min(self.field_name)
        )
        avg = field_stats['avg'] or 0
        std_dev = field_stats['std_dev'] or 0

        if self.value() == 'low':
            return queryset.filter(**{f'{self.field_name}__lt': avg - std_dev * 0.5})
        elif self.value() == 'medium':
            return queryset.filter(**{
                f'{self.field_name}__gte': avg - std_dev * 0.5,
                f'{self.field_name}__lte': avg + std_dev * 0.5
            })
        elif self.value() == 'high':
            return queryset.filter(**{f'{self.field_name}__gt': avg + std_dev * 0.5})


class TemperatureRangeFilter(NumericRangeFilter):
    parameter_name = 'temperature_range'
    title = 'Temperature Range'


class HumidityRangeFilter(NumericRangeFilter):
    parameter_name = 'humidity_range'
    title = 'Humidity Range'


class HasUnreadNotificationsFilter(SimpleListFilter):
    title = 'unread notifications'
    parameter_name = 'has_unread'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Has unread'),
            ('no', 'All read'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.annotate(
                unread_count=Count('notifications', filter=Q(notifications__is_read=False))
            ).filter(unread_count__gt=0)
        if self.value() == 'no':
            return queryset.exclude(
                notifications__is_read=False
            )
        return queryset

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'mac_address', 'user', 'is_active',
        'created_at'
    ]
    list_filter = ['is_active', 'user', HasUnreadNotificationsFilter, 'created_at']
    search_fields = ['name', 'mac_address', 'user__username']
    ordering = ['-created_at']
    list_select_related = ['user']

    readonly_fields = [
        'uuid', 'is_active', 'created_at', 'updated_at',
        'notifications_summary', 'latest_telemetry_summary'
    ]

    def latest_telemetry_summary(self, obj):
        telemetry = obj.get_latest_telemetry()
        if not telemetry:
            return "No telemetry data available"

        return format_html("""
            <div style="padding: 10px; background-color: #f8f9fa; border-radius: 4px;">
                <h4 style="margin-top: 0;">Latest Telemetry</h4>
                <p><strong>Temperature:</strong> {}°C</p>
                <p><strong>Humidity:</strong> {}%</p>
                <p><strong>Pressure:</strong> {} hPa</p>
                <p><strong>Soil Moisture:</strong> {}</p>
                <p><strong>Timestamp:</strong> {}</p>
            </div>
            """,
            format_metric(telemetry.temperature),
            format_metric(telemetry.humidity),
            format_metric(telemetry.pressure),
            telemetry.soil_moisture,
            localtime(telemetry.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        )

    latest_telemetry_summary.short_description = 'Latest Telemetry'

    # 📌 Optymalizacja wyświetlania powiadomień
    def notifications_summary(self, obj):
        notifications = obj.notifications.select_related('telemetry').order_by('-created_at')[:5]

        if not notifications:
            return "No notifications"

        summary_html = ['<div style="padding: 10px; background-color: #f8f9fa; border-radius: 4px;">']
        summary_html.append('<h4 style="margin-top: 0;">Recent Notifications</h4>')

        for notification in notifications:
            severity_colors = {
                'info': '#17a2b8',
                'warning': '#ffc107',
                'critical': '#dc3545'
            }
            color = severity_colors.get(notification.severity, '#6c757d')
            read_status = '✓' if notification.is_read else '○'

            summary_html.append(
                f'<div style="margin-bottom: 10px; padding: 8px; background-color: white; border-radius: 4px;">'
                f'<div style="margin-bottom: 5px;">'
                f'<span style="background-color: {color}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.8em;">{notification.severity.upper()}</span>'
                f'<span style="float: right;">{read_status} {notification.created_at.strftime("%Y-%m-%d %H:%M")}</span>'
                f'</div>'
                f'<div style="white-space: pre-wrap;">{notification.message}</div>'
                f'</div>'
            )

        all_notifications_url = reverse(
            'admin:notifications_usernotification_changelist') + f'?device__uuid__exact={obj.uuid}'
        summary_html.append(
            f'<a href="{all_notifications_url}" style="display: block; text-align: center; margin-top: 10px;">View all notifications</a>')
        summary_html.append('</div>')

        return format_html(''.join(summary_html))

    notifications_summary.short_description = 'Recent Notifications'

    fieldsets = (
        (None, {
            'fields': ('uuid', 'name', 'mac_address', 'user', 'is_active')
        }),
        ('Latest Telemetry', {
            'fields': ('latest_telemetry_summary',),
        }),
        ('Notifications', {
            'fields': ('notifications_summary',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'device',
        'timestamp',
        'temperature',
        'humidity',
        'pressure',
        'soil_moisture',
        'created_at'
    ]
    list_filter = [
        'device',
        'timestamp',
        TemperatureRangeFilter,
        HumidityRangeFilter,
    ]
    search_fields = ['device__name', 'device__mac_address', 'uuid']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('device')

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        try:
            queryset = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = queryset.aggregate(
            avg_temp=Avg('temperature'),
            min_temp=Min('temperature'),
            max_temp=Max('temperature'),
            avg_humidity=Avg('humidity'),
            avg_pressure=Avg('pressure'),
        )

        extra_context = {
            'metrics': {
                'Temperature': {
                    'avg': format_metric(metrics['avg_temp'], '°C'),
                    'min': format_metric(metrics['min_temp'], '°C'),
                    'max': format_metric(metrics['max_temp'], '°C'),
                },
                'Humidity': {
                    'avg': format_metric(metrics['avg_humidity'], '%'),
                },
                'Pressure': {
                    'avg': format_metric(metrics['avg_pressure'], ' hPa'),
                },
            }
        }

        response.context_data.update(extra_context)
        return response

    class Media:
        css = {
            'all': ['admin/css/metrics.css']
        }


@admin.register(DeviceSensorLimits)
class DeviceSensorLimitsAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'device_link',
        'temperature_range',
        'humidity_range',
        'pressure_range',
        'soil_moisture_range',
        'created_at',
    ]
    list_filter = [
        'device__user',
        'created_at',
    ]
    search_fields = [
        'device__name',
        'device__mac_address',
        'device__user__username',
        'device__user__email',
    ]
    readonly_fields = [
        'uuid',
        'created_at',
        'updated_at',
        'current_telemetry',
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'device',
            'device__user'
        )

    def device_link(self, obj):
        url = reverse('admin:devices_device_change', args=[obj.device.pk])
        return format_html('<a href="{}">{}</a>', url, obj.device.name)

    device_link.short_description = 'Device'
    device_link.admin_order_field = 'device__name'

    def temperature_range(self, obj):
        return format_html(
            '<span title="Current limits">{}°C to {}°C</span>',
            format_metric(obj.temp_min),
            format_metric(obj.temp_max)
        )

    temperature_range.short_description = 'Temperature Range'

    def humidity_range(self, obj):
        return format_html(
            '<span title="Current limits">{}% to {}%</span>',
            format_metric(obj.humidity_min),
            format_metric(obj.humidity_max)
        )

    humidity_range.short_description = 'Humidity Range'

    def pressure_range(self, obj):
        return format_html(
            '<span title="Current limits">{} to {} hPa</span>',
            format_metric(obj.pressure_min),
            format_metric(obj.pressure_max)
        )

    pressure_range.short_description = 'Pressure Range'

    def soil_moisture_range(self, obj):
        return format_html(
            '<span title="Current limits">{} to {}</span>',
            obj.soil_moisture_min,
            obj.soil_moisture_max
        )

    soil_moisture_range.short_description = 'Soil Moisture Range'

    def current_telemetry(self, obj):
        latest = obj.device.get_latest_telemetry()
        if not latest:
            return "No telemetry data available"

        violations = obj.check_limits(latest)
        status_color = '#28a745' if not violations else '#dc3545'

        return format_html(
            """
            <div style="padding: 10px; background-color: #f8f9fa; border-radius: 4px;">
                <h4 style="margin-top: 0;">Latest Telemetry</h4>
                <p><strong>Temperature:</strong> <span style="color: {}">{}</span>°C (limit: {} to {}°C)</p>
                <p><strong>Humidity:</strong> <span style="color: {}">{}</span>% (limit: {} to {}%)</p>
                <p><strong>Pressure:</strong> <span style="color: {}">{}</span> hPa (limit: {} to {} hPa)</p>
                <p><strong>Soil Moisture:</strong> <span style="color: {}">{}</span> (limit: {} to {})</p>
                <p><strong>Timestamp:</strong> {}</p>
                {}
            </div>
            """,
            # Temperature
            '#dc3545' if latest.temperature < obj.temp_min or latest.temperature > obj.temp_max else '#28a745',
            format_metric(latest.temperature),
            format_metric(obj.temp_min),
            format_metric(obj.temp_max),
            # Humidity
            '#dc3545' if latest.humidity < obj.humidity_min or latest.humidity > obj.humidity_max else '#28a745',
            format_metric(latest.humidity),
            format_metric(obj.humidity_min),
            format_metric(obj.humidity_max),
            # Pressure
            '#dc3545' if latest.pressure < obj.pressure_min or latest.pressure > obj.pressure_max else '#28a745',
            format_metric(latest.pressure),
            format_metric(obj.pressure_min),
            format_metric(obj.pressure_max),
            # Soil Moisture
            '#dc3545' if latest.soil_moisture < obj.soil_moisture_min or latest.soil_moisture > obj.soil_moisture_max else '#28a745',
            latest.soil_moisture,
            obj.soil_moisture_min,
            obj.soil_moisture_max,
            # Timestamp
            latest.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            # Violations if any
            f'<div style="margin-top: 10px; padding: 10px; background-color: #dc3545; color: white; border-radius: 4px;">'
            f'<strong>Violations:</strong><br>{"<br>".join(violations)}</div>' if violations else ''
        )

    current_telemetry.short_description = 'Current Telemetry Status'

    fieldsets = (
        (None, {
            'fields': ('uuid', 'device')
        }),
        ('Temperature Limits', {
            'fields': (('temp_min', 'temp_max'),)
        }),
        ('Humidity Limits', {
            'fields': (('humidity_min', 'humidity_max'),)
        }),
        ('Pressure Limits', {
            'fields': (('pressure_min', 'pressure_max'),)
        }),
        ('Soil Moisture Limits', {
            'fields': (('soil_moisture_min', 'soil_moisture_max'),)
        }),
        ('Current Status', {
            'fields': ('current_telemetry',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
