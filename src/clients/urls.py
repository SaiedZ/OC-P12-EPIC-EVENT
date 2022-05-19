from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clients import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet, basename='client')

urlpatterns = [
   path('', include(router.urls)),
]
