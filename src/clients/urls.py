from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clients import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet, basename='client')


app_name = 'clients'


urlpatterns = [
    path('', include(router.urls)),
]
