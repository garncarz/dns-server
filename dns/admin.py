from django.contrib import admin

from . import models


class RecordAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip']


admin.site.register(models.Record, RecordAdmin)
