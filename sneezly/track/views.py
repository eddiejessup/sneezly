from django.http import HttpResponse

from rest_framework import viewsets

from . import models
from . import serializers


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class DayViewSet(viewsets.ModelViewSet):
    queryset = models.Day.objects.all().order_by('date')
    serializer_class = serializers.DaySerializer


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = models.EventType.objects.all().order_by('name')
    serializer_class = serializers.EventTypeSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = models.Event.objects.all().order_by('time')
    serializer_class = serializers.EventSerializer
