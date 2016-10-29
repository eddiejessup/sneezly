from django.contrib import admin

from .models import Day, EventType, Event

admin.site.register(Day)
admin.site.register(EventType)
admin.site.register(Event)
