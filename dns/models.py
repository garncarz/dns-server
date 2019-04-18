from __future__ import unicode_literals

from django.db import models


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
