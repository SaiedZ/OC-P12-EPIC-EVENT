from django.urls import path, include
from rest_framework.routers import DefaultRouter

from events import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event')
router.register(r'event-status', views.EventStatusViewSet,
                basename='event-status')

urlpatterns = [
    path('', include(router.urls)),
]
