from django.shortcuts import render
import psutil
import time
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from ..nms.models import Device, DeviceType, SNMPCredential
from .serializers import DeviceSerializer, DeviceTypeSerializer, SNMPCredentialSerializer

# Create your views here.

def status_view(request):
    try:
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return JsonResponse({
            "status": "running",
            "system_metrics": {
                "cpu_usage": f"{cpu_percent}%",
                "memory_usage": f"{memory.percent}%",
                "memory_available": f"{memory.available / (1024 * 1024):.1f} MB",
                "disk_usage": f"{disk.percent}%",
                "disk_free": f"{disk.free / (1024 * 1024 * 1024):.1f} GB"
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "error": str(e)
        }, status=500)

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer

class SNMPCredentialViewSet(viewsets.ModelViewSet):
    queryset = SNMPCredential.objects.all()
    serializer_class = SNMPCredentialSerializer
