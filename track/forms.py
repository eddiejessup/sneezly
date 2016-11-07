from django import forms

from . import models


class EventForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = ['type', 'attrs', 'notes', 'time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].required = False


class MessageLogEntryForm(forms.ModelForm):

    class Meta:
        model = models.MessageLogEntry
        fields = ['message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['time'].required = False
