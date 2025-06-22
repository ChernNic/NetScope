from django.urls import path
from .views import connect_device, disconnect_device

urlpatterns = [
        path("connect/<int:pk>/", connect_device, name="connect_device"),
        path("disconnect/<int:pk>/", disconnect_device, name="disconnect_device")
]
