from django.shortcuts import render
from rest_framework import viewsets

from . import models
from . import serializers


class RecordViewSet(viewsets.ModelViewSet):
    queryset = models.Record.objects.all()
    serializer_class = serializers.RecordSerializer
