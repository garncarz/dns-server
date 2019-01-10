from django.contrib import admin

from . import models


class RecordAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip']


class RedirectionAdmin(admin.ModelAdmin):
    list_display = ['abbr', 'target']


admin.site.register(models.Record, RecordAdmin)
admin.site.register(models.Redirection, RedirectionAdmin)
