from rest_framework.permissions import BasePermission


class HasEventPermission(BasePermission):
    """
    A custom permission class that checks if the current user has the right
    permissions to perform a given action.

    With this permission class:
        - users should be connected and have a team attribut (FK)
        - only users from `Sale` and `Management` and `Support` teams
          have access to READ data
        - Only `support_contact` have the right for modification,
          updating and deletion and closing event.
    """

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


class ClosedEventsToReadOnly(BasePermission):
    """
    This permission class is used in addition to the above permission class.

    Closed events can't be modified or deteled
    """
    def has_object_permission(self, request, view, obj):
        if view.action not in ["retrieve", "destroy"]:
            return obj.status.name == "ongoing"
        return True


class HasEventStatusPermission(BasePermission):
    """Event Status can't only be managed by superuser."""
    def has_permission(self, request, view):
        return request.user.is_superuser and request.user.is_authenticated
