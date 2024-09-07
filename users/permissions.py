from rest_framework.permissions import IsAuthenticated


class IsOwnerProfile(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
