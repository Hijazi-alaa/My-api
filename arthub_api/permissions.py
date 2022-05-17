from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Class to permit viewing all profiles to all users
    and restrict edit a profile to only the owner
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user