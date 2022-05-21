from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedAndSuperUserOrFromManagement(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and hasattr(request.user, 'team'):
            return request.user.is_superuser \
                or request.user.team.name == "Management"
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and hasattr(request.user, 'team'):
            return request.user.is_superuser \
                or request.user.team.name == "Management"
        return False


class IsAuthenticatedAndSuperUserOrManagerForSafeMethods(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and hasattr(request.user, 'team'):
            return request.user.is_superuser \
                or request.user.team.name == "Management" \
                and request.method in SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and hasattr(request.user, 'team'):
            return request.user.is_superuser
        return False
