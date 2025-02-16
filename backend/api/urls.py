from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, DeviceTypeViewSet, SNMPCredentialViewSet, status_view

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'devicetypes', DeviceTypeViewSet)
router.register(r'snmpcredentials', SNMPCredentialViewSet)

urlpatterns = [
    path('status/', status_view, name='status'),
    path('', include(router.urls)),
] 