import logging

from rest_framework.permissions import BasePermission

logger = logging.getLogger('custom_logger')


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
                if request.user.team.name == "Sale":
                    return True
                logger.warning(f"Unauthorized user ` {request.user} ` "
                               f"tried to access {request.path} "
                               f"using  {request.method=}")
                return False

            if request.user.team.name in [
                "Management", "Sale", "Support"
            ]:
                return True
        logger.warning(f"Unauthorized user ` {request.user} ` "
                       f"tried to access {request.path} "
                       f"using  {request.method=}")
        return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        if view.action == 'close_event':
            if request.user.id == obj.support_contact.id:
                return True
            logger.warning(f"Unauthorized user ` {request.user} ` "
                           f"tried to access {request.path} "
                           f"using  {request.method=}")
            return False
        if request.user.id == obj.support_contact.id:
            return True
        logger.warning(f"Unauthorized user ` {request.user} ` "
                       f"tried to access {request.path} "
                       f"using  {request.method=}")
        return False


class ClosedEventsToReadOnly(BasePermission):
    """
    This permission class is used in addition to the above permission class.

    Closed events can't be modified or deteled
    """
    def has_object_permission(self, request, view, obj):
        if view.action not in ["retrieve", "destroy"]:
            if obj.status.name != "ongoing":
                logger.warning(f"Unauthorized user ` {request.user} ` "
                               f"tried to access {request.path} "
                               f"using  {request.method=}")
                return False
        return True


class HasEventStatusPermission(BasePermission):
    """Event Status can't only be managed by superuser."""
    def has_permission(self, request, view):
        if request.user.is_superuser and request.user.is_authenticated:
            return True

        logger.warning(f"Unauthorized user ` {request.user} ` "
                       f"tried to access {request.path} "
                       f"using  {request.method=}")
        return False
