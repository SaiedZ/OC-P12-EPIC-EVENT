"""
Custom permissions for CRUD operations on CRMUser and Team models.
"""

import logging

from rest_framework.permissions import BasePermission, SAFE_METHODS

logger = logging.getLogger('custom_logger')


class IsSuperUserOrFromManagement(BasePermission):
    """
    A custom permission class that checks if the current user has the right
    permissions to perform a given action.

    With this permission class for CRMUser:
        - users should be connected and have a team attribut (FK)
        - only superuser and users from `Management` team have permission
          for CRUD operation with CRMUser model
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.team is not None:
                return request.user.team.name == "Management"
            else:
                return request.user.is_superuser

        logger.warning(f"Unauthorized user ` {request.user} ` tried to access "
                       f"{request.path}")
        return False


class IsSuperUserOrManagerForSafeMethods(BasePermission):
    """
    A custom permission class that checks if the current user has the right
    permissions to perform a given action.

    With this permission class for Team:
        - users should be connected and have a team attribut (FK)
        - only superuser have permission for CRUD operation with Team model
        - Users from `Management` team have only the right to view informations
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.team is not None:
                return request.user.team.name == "Management" \
                    and request.method in SAFE_METHODS
            else:
                return request.user.is_superuser
        logger.warning(f"Unauthorized user ` {request.user} ` tried to access "
                       f"{request.path}")
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        logger.warning(f"Unauthorized user ` {request.user} ` tried to access "
                       f"{request.path}")
        return False
