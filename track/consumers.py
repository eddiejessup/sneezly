import json

import arrow
import parsedatetime
from channels import Channel, Group

from . import models
from . import forms


calendar = parsedatetime.Calendar()


class HandledError(Exception):
    pass


def send_to_slack(s, target_channel, target_slack_channel):
    target_channel.send({
        'text': s,
        'channel': target_slack_channel,
    })


def slack_connect(message):
    target = Channel('slack.send')
    s = 'Hello! Sneezly here.'
    send_to_slack(s, target_channel=target, target_slack_channel='general')


def parse_text_to_form_data(text, send_func):
    form_data = {}
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
        send_func('Cannot find event type {}'.format(event_name))
        raise HandledError
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
    return form_data


def execute_text(text, send_func):
    sneezly_tag = '[Sneezly]'

    def _send_func(s):
        send_func('{} {}'.format(sneezly_tag, s))

    # Make sure we do not reply to ourselves.
    if text.startswith(sneezly_tag):
        return

    try:
        form_data = parse_text_to_form_data(text, send_func=send_func)
    except HandledError:
        return
    except Exception as e:
        send_func('Hmm, I do not understand:')
        send_func(str(e))
        raise

    form = forms.EventForm(data=form_data)
    if form.is_valid():
        ev = form.save()
        t_str = arrow.get(ev.time).format('YYYY-MM-DD HH:mm:ss')
        send_func('I heard a {} at {}'.format(ev.type.name, t_str))
    else:
        send_func('Hmm, I do not understand:')
        send_func(json.dumps(form.errors))


def slack_message(message):
    data = json.loads(message.content['text'].decode('utf-8'))
    target_channel = Channel('slack.send')

    def reply(s):
        send_to_slack(s, target_channel, target_slack_channel=data['channel'])

    execute_text(data['text'], send_func=reply)


def ws_message(message):
    data = message.content

    def reply(s):
        message.reply_channel.send({
            'text': s,
        })

    execute_text(data['text'], send_func=reply)
