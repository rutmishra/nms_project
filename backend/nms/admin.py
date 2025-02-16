from django.contrib import admin
from .models import Device, DeviceType, SNMPCredential

@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(SNMPCredential)
class SNMPCredentialAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'username', 'date_added', 'last_modified')
    list_filter = ('version',)
    search_fields = ('name', 'username')
    fieldsets = (
        (None, {
            'fields': ('name', 'version')
        }),
        ('SNMPv1/v2c Settings', {
            'fields': ('community_string',),
            'classes': ('collapse',)
        }),
        ('SNMPv3 Settings', {
            'fields': ('username', 'auth_protocol', 'auth_password', 
                      'priv_protocol', 'priv_password'),
            'classes': ('collapse',)
        })
    )

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'mac_address', 'device_type', 'probe_type', 
                   'operational_status', 'is_active')
    list_filter = ('device_type', 'probe_type', 'operational_status', 'is_active')
    search_fields = ('name', 'ip_address', 'location', 'serial_number', 'mac_address')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'ip_address', 'device_type', 'location')
        }),
        ('Device Identification', {
            'fields': ('serial_number', 'mac_address'),
            'classes': ('collapse',)
        }),
        ('Monitoring Configuration', {
            'fields': ('probe_type', 'snmp_credential')
        }),
        ('Status', {
            'fields': ('operational_status', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('last_checked', 'date_added'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('last_checked', 'date_added') 