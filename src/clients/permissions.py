from rest_framework.permissions import BasePermission


class HasClientPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.team is not None:
            return request.user.team.name == "Sale"
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.team.name == "Sale"


class IsManager(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.team is not None:
            return request.user.team.name == "Management" \
                and request.method != "POST"
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.team.name == "Management" \
            and request.method not in ('DELETE',)
