from django.contrib import admin

from .import models


admin.site.register(models.EventType)
admin.site.register(models.EventTypeAlias)
admin.site.register(models.Event)
admin.site.register(models.MessageLogEntry)
