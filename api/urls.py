from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

router = routers.DefaultRouter()

# CRUD ViewSets
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.CustomGroupViewSet)
router.register(r'vlans', views.VLANViewSet)
router.register(r'vrfs', views.VRFViewSet)
router.register(r'subnets', views.SubnetViewSet)
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'buildings', views.BuildingViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'manufacturers', views.ManufacturerViewSet)
router.register(r'device-roles', views.DeviceRoleViewSet)
router.register(r'device-types', views.DeviceTypeViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'interfaces', views.InterfaceViewSet)
router.register(r'connections', views.ConnectionViewSet)

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
]
