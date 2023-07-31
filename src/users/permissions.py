from django.utils.translation import override
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsSuperUser(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return obj.is_superuser


class IsAdminRole(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return obj.role == "admin"


class IsModeratorRole(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return obj.role == "moderator"


class IsUserRole(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return obj.role == "user"


class IsOwnerOrReadOnly(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj == request.user


class IsStaffUser(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return obj.is_staff or obj.role in ("admin", "moderator")


class IsOwnerOrStuffUser(CustomPermission):

    def has_object_permission(self, request: Request, view, obj):
        return obj.is_staff or obj.role in ("admin", "moderator") or obj == request.user

