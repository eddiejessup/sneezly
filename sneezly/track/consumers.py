import json

from channels import Channel, Group
import parsedatetime

from . import models
from . import forms


calendar = parsedatetime.Calendar()


def slack_connect(message):
    target = Channel('slack.send')
    target.send({
        'text': 'Hello! Sneezly here.',
        'channel': 'general',
    })


def slack_message(message):
    target = Channel('slack.send')
    data = json.loads(message.content['text'].decode('utf-8'))
    slack_channel = data['channel']

    def send(s):
        target.send({
            'text': s,
            'channel': slack_channel,
        })

    form_data = {}

    text = data['text']
    if ' ' in text:
        first_space = text.find(' ')
        event_name = text[:first_space]
        the_rest = text[first_space + 1:]
        pairs = [s.split('=') for s in the_rest.split(',')]
    else:
        event_name = text
        pairs = []

    try:
        event_type = models.EventType.objects.get(name__iexact=event_name)
    except models.EventType.DoesNotExist:
        send("Cannot find event type '{}'".format(event_name))
        return
    else:
        form_data['type'] = event_type.pk

    if pairs:
        attrs = {}
        for key, value in pairs:
            key = key.strip()
            value = value.strip()
            if key == '@':
                form_data['time'] = calendar.parseDT(value)[0]
            else:
                attrs[key] = value
        form_data['attrs'] = json.dumps(attrs)

    form = forms.EventForm(data=form_data)
    if form.is_valid():
        ev = form.save()
        send('I heard a {} at {}'.format(ev.type.name, ev.time))
    # else:
    #     send('Hmm, I do not understand:')
    #     send(json.dumps(form.errors))
