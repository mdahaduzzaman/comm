from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()
class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """only authenticated user or shop owner can have the permissions or read only"""
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return True
        
        try:
        # Attempt to retrieve the current user's shop
            shop = self.request.user.shop_owner
            return True
        except User.DoesNotExist:
            # User might not exist or doesn't have a shop (OneToOne relation)
            return False


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow admin users full access,
    while allowing read-only access to others.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For unsafe methods (POST, PUT, PATCH, DELETE),
        # only staff users are granted permission.
        return request.user.is_staff