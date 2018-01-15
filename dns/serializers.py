from constance import config
from ipware.ip import get_ip
from rest_framework import serializers

from . import models


class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Record
        fields = ['name', 'ip']

    def to_internal_value(self, data):
        if data['ip'] == 'auto':
            data['ip'] = get_ip(self.context['request'])
        if not ('name' in data and data['name']):
            data['name'] = '%s.%s' % (self.context['request'].user.username,
                                      config.DOMAIN)
        return super(RecordSerializer, self).to_internal_value(data)
