import json

import arrow
import parsedatetime
from channels import Channel, Group

from . import models
from . import forms
from . import parse_utils


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


def resolve_event_name_to_type(event_name):
    try:
        return models.EventType.objects.get(name__iexact=event_name)
    except models.EventType.DoesNotExist:
        alias_obj = models.EventTypeAlias.objects.get(name__iexact=event_name)
        return alias_obj.event_type


def _execute_text(text, send_func):
    form_data = {}
    text = text.strip()

    # Special commands.
    # Do not log these, especially 'repeat', as we could get into an infinite
    # loop.

    if parse_utils.is_repeat_command(text):
        latest_entry = models.MessageLogEntry.objects.latest()
        _execute_text(latest_entry.message, send_func)
        return
    else:
        log_form = forms.MessageLogEntryForm(data={'message': text})
        if log_form.is_valid():
            log_form.save()
        else:
            send_func('Not logging message:')
            send_func(json.dumps(log_form.errors))

    if text == 'undo':
        latest_ev = models.Event.objects.latest('time_created')
        obj_str = latest_ev.__str__()
        latest_ev.delete()
        send_func('Deleted {}'.format(obj_str))
        return

    if ' ' in text:
        first_space = text.find(' ')
        raw_event_name = text[:first_space]
        the_rest = text[first_space + 1:]
        pairs = [s.split('=') for s in the_rest.split(',')]
    else:
        raw_event_name = text
        pairs = []

    try:
        event_type = resolve_event_name_to_type(raw_event_name)
    except models.EventTypeAlias.DoesNotExist:
        send_func('Cannot find event type {}'.format(raw_event_name))
        raise HandledError
    form_data['type'] = event_type.pk

    if pairs:
        attrs = {}
        for key, value in pairs:
            key = key.strip()
            value = value.strip()
            if key in ('@', 't', 'time'):
                form_data['time'] = calendar.parseDT(value)[0]
            elif key in ('d', 'desc', 'description', 'notes'):
                form_data['notes'] = value
            else:
                attrs[key] = value
        form_data['attrs'] = json.dumps(attrs)

    form = forms.EventForm(data=form_data)
    if form.is_valid():
        ev = form.save()
        t_str = arrow.get(ev.time).format('YYYY-MM-DD HH:mm:ss')
        send_func('I heard a {} at {}'.format(ev.type.name, t_str))
    else:
        send_func('Hmm, I do not understand:')
        send_func(json.dumps(form.errors))


def execute_text(text, send_func):
    sneezly_tag = '[Sneezly]'

    def signed_send_func(s):
        send_func('{} {}'.format(sneezly_tag, s))

    # Make sure we do not reply to ourselves.
    if text.startswith(sneezly_tag):
        return

    try:
        _execute_text(text, send_func=signed_send_func)
    except HandledError:
        return
    except Exception as e:
        send_func('Hmm, I do not understand:')
        send_func(str(e))
        raise


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
