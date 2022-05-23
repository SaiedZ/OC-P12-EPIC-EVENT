from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedAndSuperUserOrFromManagement(BasePermission):
    """
    A custom permission class that checks if the current user has the right
    permissions to perform a given action.

    With this permission class for CRMUser:
        - users should be connected and have a team attribut (FK)
        - only superuser and users from `Management` team have permission
          for CRUD operation with CRMUser model
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.team is not None:
            return request.user.is_superuser \
                or request.user.team.name == "Management"
        return False


class IsAuthenticatedAndSuperUserOrManagerForSafeMethods(BasePermission):
    """
    A custom permission class that checks if the current user has the right
    permissions to perform a given action.

    With this permission class for Team:
        - users should be connected and have a team attribut (FK)
        - only superuser have permission for CRUD operation with Team model
        - Users from `Management` team have only the right to view informations
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.team is not None:
            return request.user.is_superuser \
                or request.user.team.name == "Management" \
                and request.method in SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
