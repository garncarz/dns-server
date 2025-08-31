from django.contrib import admin

from . import models


class RecordAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip']


class RedirectionAdmin(admin.ModelAdmin):
    list_display = ['abbr', 'target']


class PastebinAdmin(admin.ModelAdmin):
    list_display = ['key', 'filename', 'created_at', 'client_ip']
    list_filter = ['created_at', 'content_type']
    search_fields = ['key', 'filename']
    readonly_fields = ['created_at', 'client_ip']


admin.site.register(models.Record, RecordAdmin)
admin.site.register(models.Redirection, RedirectionAdmin)
admin.site.register(models.Pastebin, PastebinAdmin)
