from __future__ import unicode_literals

from django.db import models


class Record(models.Model):
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.ip)
