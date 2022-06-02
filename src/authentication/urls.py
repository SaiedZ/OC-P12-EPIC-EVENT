"""
URL mappings for the authebntication API.
"""

from django.urls import path
from authentication import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('logout/', views.LogoutView.as_view(),
         name='logout'),
    path('logout-from-all/', views.LogoutAllView.as_view(),
         name='logout_from_all'),
]
