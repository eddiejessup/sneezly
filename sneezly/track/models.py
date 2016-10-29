from datetime import date

from django.db import models
from django.utils import timezone


class Day(models.Model):
    date = models.DateField(default=date.today, unique=True)

    DOVE = 'DV'
    SIMPLE = 'SM'
    NONE = 'NN'
    SOAP_CHOICES = (
        (DOVE, 'Dove'),
        (SIMPLE, 'Simple'),
        (NONE, 'None'),
    )

    HOT = 'HO'
    WARM = 'WA'
    COLD = 'CO'
    SHOWER_TEMP_CHOICES = (
        (HOT, 'Hot'),
        (WARM, 'Warm'),
        (COLD, 'Cold'),
    )

    soap_type = models.CharField(max_length=2, choices=SOAP_CHOICES,
                                 default=SIMPLE, blank=True)
    shower_temp = models.CharField(max_length=2, choices=SHOWER_TEMP_CHOICES,
                                   default=HOT, blank=True)

    def __str__(self):
        return '<{} date={}>'.format(self.__class__.__name__, self.date)


class EventType(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return '<{} name={}>'.format(self.__class__.__name__, self.name)


class Event(models.Model):
    type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    def __str__(self):
        return '<{} type={}, time={}>'.format(self.__class__.__name__,
                                              self.type, self.time)
