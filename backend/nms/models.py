from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    is_password_changed = models.BooleanField(default=False)  # Forces first-time password change

    # Fix conflicts by renaming the related names
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

class DeviceType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class SNMPCredential(models.Model):
    SNMP_VERSIONS = [
        ('v1', 'SNMPv1'),
        ('v2c', 'SNMPv2c'),
        ('v3', 'SNMPv3')
    ]

    name = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=10, choices=SNMP_VERSIONS)
    community_string = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Required for SNMPv1 and SNMPv2c"
    )
    
    # SNMPv3 specific fields
    username = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Required for SNMPv3"
    )
    auth_protocol = models.CharField(
        max_length=10,
        choices=[('MD5', 'MD5'), ('SHA', 'SHA')],
        blank=True,
        null=True,
        help_text="Authentication protocol for SNMPv3"
    )
    auth_password = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Authentication password for SNMPv3"
    )
    priv_protocol = models.CharField(
        max_length=10,
        choices=[('DES', 'DES'), ('AES', 'AES')],
        blank=True,
        null=True,
        help_text="Privacy protocol for SNMPv3"
    )
    priv_password = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Privacy password for SNMPv3"
    )
    
    date_added = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.version})"

    class Meta:
        ordering = ['name']

class Device(models.Model):
    PROBE_TYPES = [
        ('snmp', 'SNMP'),
        ('icmp', 'ICMP (Ping)'),
    ]

    STATUS_CHOICES = [
        ('up', 'Up'),
        ('down', 'Down'),
        ('unknown', 'Unknown')
    ]

    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    device_type = models.ForeignKey(
        DeviceType, 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    
    # Device identification fields
    serial_number = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Device serial number (optional)"
    )
    mac_address = models.CharField(
        max_length=17,  # Format: XX:XX:XX:XX:XX:XX
        blank=True, 
        null=True,
        help_text="Device MAC address (format: XX:XX:XX:XX:XX:XX)"
    )
    
    # Monitoring configuration
    probe_type = models.CharField(
        max_length=10, 
        choices=PROBE_TYPES,
        default='icmp'
    )
    snmp_credential = models.ForeignKey(
        SNMPCredential,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Required only if probe type is SNMP"
    )
    
    location = models.CharField(max_length=200, blank=True, null=True)
    
    # Status fields
    operational_status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='unknown'
    )
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    last_checked = models.DateTimeField(default=timezone.now)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['operational_status'])
        ]