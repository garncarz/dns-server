from constance import config
from rest_framework.permissions import BasePermission


class RecordPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if not request.user.is_authenticated:
            return False
        if not 'name' in request.data:
            return True
        if request.data['name'] == '%s.%s' % (request.user.username,
                                              config.DOMAIN):
            return True
        return False


class PastebinPermission(BasePermission):
    
    def has_permission(self, request, view):
        # Allow anonymous users to create pastebins (public interface)
        if view.action == 'create':
            return True
        # Only admin can list and retrieve pastebins
        return request.user.is_authenticated and request.user.is_superuser
