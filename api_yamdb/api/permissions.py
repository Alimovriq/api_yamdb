from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated and request.user.is_admin:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_admin:
            return True


class AdminOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_admin:
                return True
        return False

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_admin:
                return True
        return False


class AdminOrModeratorOrAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_admin:
            return True
        elif request.user.is_moderator:
            return True
        elif request.user == obj.author and request.user.is_user:
            return True
        return False


class UserIsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
