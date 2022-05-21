from rest_framework.permissions import BasePermission


class HasClientPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and hasattr(request.user, 'team'):
            return request.user.team.name == "Sale"
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and hasattr(request.user, 'team'):
            return request.user.team.name == "Sale"
        return False


class IsManager(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and hasattr(request.user, 'team'):
            return request.user.team.name == "Management" \
                and request.method not in ('POST', 'DELETE')
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and hasattr(request.user, 'team'):
            return request.user.team.name == "Management" \
                and request.method not in ('POST', 'DELETE')
        return False
