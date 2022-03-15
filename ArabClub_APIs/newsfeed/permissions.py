from rest_framework import permissions, serializers


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not obj.user_id == request.user.pk:
            raise serializers.ValidationError(
                {"detail": "You do not have permission to perform this action."}
            )
        return obj.user_id == request.user.id
