# from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)


class IsOwnerCartItem(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.cart.user == request.user:
            return True
