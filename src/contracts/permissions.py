from rest_framework.permissions import BasePermission


class ContractPermissionSafeAndPost(BasePermission):
    """
    A custom permission class that checks if the current user has the right
    permissions to perform a given action.

    With this permission class:
        - users should be connected and have a team attribut (FK)
        - only users from `Sale` and `Management` teams have access
          to data and can create new contracts.
        - Only `sales_contact` have the right for modification,
          updating and deletion and signing the contract
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.team is not None:
            return request.user.team.name in ["Sale", "Management"]
        return False

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return True
        return request.user == obj.sales_contact


class SignedContractTReadOnly(BasePermission):
    """
    This permission class is used in addition to the above permission class.

    Signed contracts can't be modified
    """
    def has_object_permission(self, request, view, obj):
        if view.action not in ["retrieve", "destroy"]:
            return not obj.status
        return True
