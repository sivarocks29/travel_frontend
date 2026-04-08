"""
Role-based permissions for Pyolliv.
"""
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Only admin role users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')


class IsCarOwner(BasePermission):
    """Only car/vehicle owner role users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'car')


class IsDriver(BasePermission):
    """Only driver role users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'driver')


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return request.user and request.user.is_authenticated
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')
