from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from . import parse_utils


class EventType(models.Model):

    name = models.CharField(max_length=40)
    attr_schema = JSONField(default=dict, blank=True)

    def __str__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    def _clean_attribute(self, key):
        valid_values = self.attr_schema[key]
        # Check key maps to a list.
        if not isinstance(valid_values, list):
            raise ValidationError(
                _("Key '{}' target '{}' is not of type 'list'")
                .format(key, valid_values))
        # Check valid value entries are of sensible types.
        valid_value_types = (int, str)
        for valid_value in valid_values:
            if not isinstance(valid_value, valid_value_types):
                raise ValidationError(
                    _("Key '{}' valid value '{}' must be in types {}, "
                      "not '{}'")
                    .format(key, valid_value,
                            [t.__name__ for t in valid_value_types],
                            type(valid_value).__name__))

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        # Check attributes that are specified are valid.
        for key in self.attr_schema:
            self._clean_attribute(key)


class EventTypeAlias(models.Model):

    name = models.CharField(max_length=40)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)


class Event(models.Model):
    type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    attrs = JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<{} type={}, time={}>'.format(self.__class__.__name__,
                                              self.type.name, self.time)

    def _clean_attribute(self, key):
        schema = self.type.attr_schema
        if key not in schema:
            raise ValidationError(
                _("Attribute '{}' not in event schema keys {}.")
                .format(key, list(schema.keys())))
        value = self.attrs[key]
        valid_values = schema[key]
        if valid_values and value not in valid_values:
            raise ValidationError(
                _("Attribute '{}' value '{}' not in possible values {}")
                .format(key, value, valid_values))

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        # Check attributes that are specified are valid.
        for key in self.attrs:
            self._clean_attribute(key)
        # Check all schema attributes are specified.
        for schema_key in self.type.attr_schema:
            if schema_key not in self.attrs:
                raise ValidationError(
                    _("Attribute '{}' not specified")
                    .format(schema_key))


class MessageLogEntry(models.Model):

    message = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'MessageLogEntry'
        verbose_name_plural = 'MessageLogEntries'
        get_latest_by = 'time_created'

    def __str__(self):
        return '<{}: {}. "{}">'.format(self.__class__.__name__,
                                       self.time_created,
                                       self.message)

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if parse_utils.is_repeat_command(self.message):
            raise ValidationError(
                _("Cannot record a message that will repeat: {}")
                .format(self.message))
