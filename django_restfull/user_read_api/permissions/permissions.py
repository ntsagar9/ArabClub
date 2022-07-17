from rest_framework import permissions
from rest_framework.serializers import ValidationError

from logging_manager import eventslog

logger = eventslog.logger


class IsOwner(permissions.BasePermission):
    """
    This permission for allow only owner to edit data
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if not obj.id == request.user.id:
            logger.error(
                "{} - You do not have permission to perform this "
                "action. ".format(request.user)
            )
            raise ValidationError(
                {
                    "detail": """
                    You do not have permission to perform this action.
                    """
                }
            )
        return obj.id == request.user.id


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        logger.error(f"Bad gateway! - {request.user} - {request}")
