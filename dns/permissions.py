from constance import config
from rest_framework.permissions import BasePermission


class RecordPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if not request.user.is_authenticated():
            return False
        if request.data['name'] == '%s.%s' % (request.user.username,
                                              config.DOMAIN):
            return True
        return False
