"""
URL configuration for NetScope project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from NetScope.settings import BASE_DIR
from extras.views import home_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('extras.urls')),
    path('', include('inventory.urls')),
    path('', include('ipam.urls')),
    path('', include('topology.urls')),
    path("", home_dashboard, name="home"),
    path("api/", include("api.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(BASE_DIR, "static"))

handler404 = 'NetScope.views.handler404'
handler403 = 'NetScope.views.handler403'