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


def chunks(lst, chunk_size=2):
    return (lst[i:i + n] for i in range(0, len(lst), n))


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
    words = text.split()
    event_name = words[0]
    pairs = [s.split('=') for s in words[1:]]

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
            if key == '@':
                form_data['time'] = calendar.parseDT(value)[0]
            else:
                attrs[key] = value
        form_data['attrs'] = json.dumps(attrs)

    form = forms.EventForm(data=form_data)
    if form.is_valid():
        ev = form.save()
        send('I heard a {} at {}'.format(ev.type.name, ev.time))
    else:
        send('Hmm, I do not understand:')
        send(json.dumps(form.errors))
