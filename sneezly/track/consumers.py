import json

from channels import Channel, Group

from . import models


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
    text = data['text']
    if any(s in text for s in ['sneeze', 'achoo']):
        SneezeEvent = models.EventType.objects.get(name__contains='neeze')
        ev = models.Event.objects.create(type=SneezeEvent)
        reply_text = 'Bless you! I heard you sneeze at {}'.format(ev.time)
    else:
        reply_text = 'huh?'
    target.send({
        'text': reply_text,
        'channel': slack_channel,
    })
