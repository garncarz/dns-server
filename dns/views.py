import logging

from django.shortcuts import get_object_or_404, redirect
from django_statsd.clients import statsd
from rest_framework import viewsets

from . import models
from . import permissions
from . import serializers

logger = logging.getLogger(__name__)


class RecordViewSet(viewsets.ModelViewSet):
    queryset = models.Record.objects.all()
    serializer_class = serializers.RecordSerializer
    permission_classes = [permissions.RecordPermission]

    def create(self, request, *args, **kwargs):
        """
        Not a nice method. Combining create/update mechanism,
        so one can POST a patch without knowing id.
        """

        request.POST._mutable = True

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        name = serializer.data.get('name', None)
        instance = None

        if name:
            try:
                instance = models.Record.objects.get(name=name)
            except models.Record.DoesNotExist:
                pass

        if instance:
            self.get_object = lambda: instance
            logger.info('Update record: %s' % serializer.data)
            statsd.incr('record.update')
            return super(RecordViewSet, self).update(request, *args, **kwargs)

        else:
            logger.info('New record: %s' % serializer.data)
            statsd.incr('record.new')
            return super(RecordViewSet, self).create(request, *args, **kwargs)


def redirection(request, abbr):
    redir_obj = get_object_or_404(models.Redirection, abbr=abbr)
    return redirect(redir_obj.target)
