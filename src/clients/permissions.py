from rest_framework.permissions import BasePermission


class HasClientPermissions(BasePermission):
    """
    A custom permission class that checks if the current user has the right
    permissions to perform a given action.

    With this permission class:
        - users should be connected and have a team attribut (FK)
        - only users from `Sale` team have access to data
        - they also have the right for modification, updating and deletion
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.team is not None:
            return request.user.team.name == "Sale"
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.team.name == "Sale"


class IsManager(BasePermission):
    """
    A custom permission class that checks if the current user has the right
    permissions to perform a given action.

    With this permission class:
        - users should be connected and have a team attribut (FK)
        - user from `Management` team have access to data
        - they can't create or delete objects
        They have the permission to update data
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.team is not None:
            return request.user.team.name == "Management" \
                and request.method != "POST"
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.team.name == "Management" \
            and request.method not in ('DELETE',)
