import uuid
from constance import config
from ipware import get_client_ip
from rest_framework import serializers

from . import models


class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Record
        fields = ['name', 'ip']

    def to_internal_value(self, data):
        if data['ip'] == 'auto':
            client_ip, is_routable = get_client_ip(self.context['request'])
            data['ip'] = client_ip
        if not ('name' in data and data['name']):
            data['name'] = '%s.%s' % (self.context['request'].user.username,
                                      config.DOMAIN)
        return super(RecordSerializer, self).to_internal_value(data)


class PastebinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pastebin
        fields = ['key', 'content', 'filename', 'content_type']
        read_only_fields = ['key']

    def create(self, validated_data):
        # Generate a unique key
        validated_data['key'] = str(uuid.uuid4())
        
        # Capture client IP
        request = self.context.get('request')
        if request:
            client_ip, _ = get_client_ip(request)
            validated_data['client_ip'] = client_ip
            
        return super(PastebinSerializer, self).create(validated_data)
