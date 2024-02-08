from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .helpers import get_token_by_token_body

class HasValidToken(permissions.BasePermission):
    """
    Custom permission to only allow access to authenticated users with a valid token.
    """
    def has_permission(self, request, view):
        token_body = request.headers.get('token', None)
        token = get_token_by_token_body(token_body)
        if token is None:
            raise PermissionDenied('Invalid token')
        return True

class HasReadPermission(permissions.BasePermission):
    """
    Allows tokens that only have read permission
    """
    def has_permission(self, request, view):
        token_body = request.headers.get('token', None)
        token = get_token_by_token_body(token_body)
        return token.scope.scope_name == 'Read'
    
class HasWritePermission(permissions.BasePermission):
    """
    Allows tokens that only have write permission
    """
    def has_permission(self, request, view):
        token_body = request.headers.get('token', None)
        token = get_token_by_token_body(token_body)
        return token.scope.scope_name == 'Write'