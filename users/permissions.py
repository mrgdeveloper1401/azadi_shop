from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsOwnerProfile(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True


class IsVerifiedUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_verified:
            raise PermissionDenied("you must verify account")
        return True
