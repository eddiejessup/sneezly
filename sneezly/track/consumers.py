from channels import Group

from . import models


# Connected to websocket.connect
def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("chat").add(message.reply_channel)


def ws_message(message):
    Group("chat").send({
        'text': 'I hear you...',
    })
    text = message.content['text'].lower()
    if any(s in text for s in ['sneeze', 'achoo']):
        SneezeEvent = models.EventType.objects.get(name__contains='neeze')
        ev = models.Event.objects.create(type=SneezeEvent)
        reply_text = 'Bless you! I heard you sneeze at {}'.format(ev.time)
    else:
        reply_text = 'huh?'
    Group("chat").send({
        'text': reply_text,
    })


# Connected to websocket.disconnect.
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)
