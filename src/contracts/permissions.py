from rest_framework.permissions import BasePermission


class ContractPermissionSafeAndPost(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.team is not None:
            return request.user.team.name in ["Sale", "Management"]
        return False

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return True
        return request.user == obj.sales_contact
