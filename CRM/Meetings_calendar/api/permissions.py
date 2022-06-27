from rest_framework import permissions


class MentorCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.groups.filter(name="Mentor").exists():
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Mentor").exists():
            return True
        return False
