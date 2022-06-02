"""
CRM URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)
from django.conf.urls.static import static
from django.conf import settings

from CRM.admin import crm_admin_site


urlpatterns = [
    path('admin/', admin.site.urls),
    path('epic-event-crm-admin/', crm_admin_site.urls),
    path('api/', include('rest_framework.urls')),
    path('api/', include('authentication.urls')),
    path('api/', include('teams.urls')),
    path('api/', include('clients.urls')),
    path('api/', include('contracts.urls')),
    path('api/', include('events.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'
         ),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'
         ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
