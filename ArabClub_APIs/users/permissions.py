from rest_framework import permissions, status
from rest_framework.serializers import ValidationError


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
            raise ValidationError(
                {"detail": "You do not have permission to perform this action."}
            )
        return obj.id == request.user.id
