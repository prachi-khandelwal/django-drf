from math import perm
import re
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """ 
    Is a Read Only method if you are not the owner, you allowing safe 
    methods [GET, HEADERS, OPTIONS].
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff   


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return  request.user and request.user.is_staff

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow anyone to read, but only admins can modify.
    Used for admin-moderated content.
    """
    
    def has_permission(self, request, view):
        # Allow read operations for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write operations only for admin users
        return request.user and request.user.is_staff




        
        
