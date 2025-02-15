from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Avg, Min, Max
from django.contrib.admin import SimpleListFilter

from .models import Device, Telemetry


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


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'mac_address', 
        'user', 
        'is_active', 
        'telemetry_count',
        'latest_telemetry_info',
        'created_at'
    ]
    list_filter = ['is_active', 'user', 'created_at']
    search_fields = ['name', 'mac_address', 'user__username']
    readonly_fields = ['uuid', 'is_active', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            telemetry_count=Count('telemetry')
        )
    
    def telemetry_count(self, obj):
        url = reverse('admin:devices_telemetry_changelist') + f'?device__uuid__exact={obj.uuid}'
        return format_html('<a href="{}">{} records</a>', url, obj.telemetry_count)
    telemetry_count.short_description = 'Telemetry Records'
    telemetry_count.admin_order_field = 'telemetry_count'
    
    def latest_telemetry_info(self, obj):
        latest = obj.get_latest_telemetry()
        if not latest:
            return '-'
        return format_html(
            """
            <div style="white-space: nowrap;">
                🌡️ {}°C<br>
                💧 {}%<br>
                ⏰ {}
            </div>
            """,
            format_metric(latest.temperature),
            format_metric(latest.humidity),
            latest.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        )
    latest_telemetry_info.short_description = 'Latest Telemetry'


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
