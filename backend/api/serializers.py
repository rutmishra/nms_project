from rest_framework import serializers
from ..nms.models import Device, DeviceType, SNMPCredential

class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = '__all__'

class SNMPCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNMPCredential
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    device_type_name = serializers.CharField(source='device_type.name', read_only=True)
    snmp_credential_name = serializers.CharField(source='snmp_credential.name', read_only=True)

    class Meta:
        model = Device
        fields = [
            'id', 'name', 'ip_address', 'device_type', 'device_type_name',
            'serial_number', 'mac_address', 'probe_type', 
            'snmp_credential', 'snmp_credential_name',
            'location', 'operational_status', 'is_active',
            'last_checked', 'date_added'
        ] 