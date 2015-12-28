from django.shortcuts import render
from rest_framework import viewsets

from . import models
from . import permissions
from . import serializers


class RecordViewSet(viewsets.ModelViewSet):
    queryset = models.Record.objects.all()
    serializer_class = serializers.RecordSerializer
    permission_classes = [permissions.RecordPermission]

    def create(self, request, *args, **kwargs):
        """
        Not a nice method. Combining create/update mechanism,
        so one can POST a patch without knowing id.
        """

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
            return super(RecordViewSet, self).update(request, *args, **kwargs)
        else:
            return super(RecordViewSet, self).create(request, *args, **kwargs)
