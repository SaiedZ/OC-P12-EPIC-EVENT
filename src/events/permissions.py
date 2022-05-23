from rest_framework.permissions import BasePermission


class HasEventPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.team is not None:
            if view.action == 'create':
                return request.user.team.name == "Sale"
            return request.user.team.name in [
                "Management", "Sale", "Support"
            ]
        return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        if view.action == 'close_event':
            return request.user.id == obj.support_contact.id
        return request.user.id == obj.support_contact.id


class HasEventStatusPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser and request.user.is_authenticated
