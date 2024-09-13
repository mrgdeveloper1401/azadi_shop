from rest_framework.permissions import IsAdminUser


class IsAdmin(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))
