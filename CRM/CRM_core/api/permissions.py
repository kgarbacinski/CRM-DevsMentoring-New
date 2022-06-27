from rest_framework import permissions


class AccessPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user.is_autenticated:
            return True
        return False
