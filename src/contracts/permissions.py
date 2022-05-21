from rest_framework.permissions import BasePermission,SAFE_METHODS


class ContractPermissionSafeAndPost(BasePermission):

    def has_permission(self, request, view):
        print("has_permission", request.method)
        if request.user.is_authenticated:
            return hasattr(request.user, "team") \
                and request.user.team.name in ["Sale", "Management"] \
                and request.method not in ["PUT", "PATCH", "DELETE"]
        return False

    def has_object_permission(self, request, view, obj):
        print("has_object_permission", request.method)
        print(view.action)
        if request.method in SAFE_METHODS:
            if view.action == "sign_contract":
                return request.user.id == obj.sales_contact
            return True
        return request.user.id == obj.sales_contact
