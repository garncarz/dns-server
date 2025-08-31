from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Record(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip = models.GenericIPAddressField('IP')

    def __unicode__(self):
        return '<Record name=%s ip=%s>' % (self.name, self.ip)


class Redirection(models.Model):

    abbr = models.CharField(max_length=100, unique=True)
    target = models.URLField()

    def __unicode__(self):
        return '<Redirection %s => %s>' % (self.abbr, self.target)


class Pastebin(models.Model):
    key = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    filename = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    client_ip = models.GenericIPAddressField('IP', blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return '<Pastebin key=%s created=%s>' % (self.key, self.created_at)
