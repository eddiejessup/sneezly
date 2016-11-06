from django.contrib import admin

from .import models


admin.site.register(models.EventType)
admin.site.register(models.Event)
