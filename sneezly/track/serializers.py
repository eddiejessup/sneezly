from rest_framework import serializers

from . import models


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventType
        fields = ('id', 'name',)


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Event
        fields = ('id', 'type', 'time', 'notes',)
