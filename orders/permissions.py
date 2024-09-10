from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.user == user


class IsOwnerCartItem(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.cart.user == request.user:
            return True
