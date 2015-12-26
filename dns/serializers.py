from rest_framework import serializers

from . import models


class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Record
        fields = ['name', 'ip']
