from django.utils.translation import override
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsSuperUser(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.is_superuser


class IsAdminRole(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.role == "admin"


class IsModeratorRole(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.role == "moderator"


class IsUserRole(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.role == "user"


class IsOwnerOrReadOnly(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj == request.user


class IsOwnPageOrReadOnly(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsNotBlocked(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return not request.user.is_blocked


class IsStaffUser(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.is_staff or request.user.role in ("admin", "moderator")


class IsOwnerOrStaffUser(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.is_staff or request.user.role in ("admin", "moderator") or obj == request.user


class IsOwnPageOrStaffUser(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.is_staff or obj.owner == request.user
