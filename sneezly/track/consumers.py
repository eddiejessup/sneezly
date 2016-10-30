from . import models


def ws_echo(message):
    message.reply_channel.send({
        'text': 'I hear you...',
    })
    text = message.content['text'].lower()
    if any(s in text for s in ['sneeze', 'achoo']):
        SneezeEvent = models.EventType.objects.get(name__contains='neeze')
        ev = models.Event.objects.create(type=SneezeEvent)
        reply_text = 'Bless you! I heard you sneeze at {}'.format(ev.time)
    else:
        reply_text = 'huh?'
    message.reply_channel.send({
        'text': reply_text,
    })
