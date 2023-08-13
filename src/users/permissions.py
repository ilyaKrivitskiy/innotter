from django.utils.translation import override
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class IsNotBlockedAndAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_blocked


class IsSuperUser(IsNotBlockedAndAuthenticated):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.is_superuser


class IsAdminRole(IsNotBlockedAndAuthenticated):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.role == "admin"


class IsModeratorRole(IsNotBlockedAndAuthenticated):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.role == "moderator"


class IsUserRole(IsNotBlockedAndAuthenticated):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.role == "user"


class IsOwnerOrReadOnly(IsNotBlockedAndAuthenticated):

    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj == request.user


class IsOwnPageOrReadOnly(IsNotBlockedAndAuthenticated):

    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsStaffUser(IsNotBlockedAndAuthenticated):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.is_staff


class IsOwnerOrStaffUser(IsNotBlockedAndAuthenticated):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.is_staff or obj == request.user


class IsOwnPageOrStaffUser(IsNotBlockedAndAuthenticated):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.is_staff or obj.owner == request.user


class IsOwnPostOrReadOnly(IsNotBlockedAndAuthenticated):

    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.page.owner == request.user


class IsOwnPostOrStaffUser(IsNotBlockedAndAuthenticated):

    def has_object_permission(self, request: Request, view, obj):
        return request.user.is_staff or obj.page.owner == request.user
