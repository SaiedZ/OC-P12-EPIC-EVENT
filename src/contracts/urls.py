from django.urls import path, include
from rest_framework.routers import DefaultRouter

from contracts import views

router = DefaultRouter()
router.register(r"contracts", views.ContractViewSet, basename="contract")

urlpatterns = [
    path("", include(router.urls)),
]
