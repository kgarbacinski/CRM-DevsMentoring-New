from rest_framework import permissions


class MentorAccess(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.user.is_authenticated and request.user.groups.filter(name='Mentor').exists():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Mentor').exists():
            return True
        return False


