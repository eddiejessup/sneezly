def ws_echo(message):
    text = message.content['text']
    if 'sneeze' in text:
        reply_text = 'bless you!'
    else:
        reply_text = 'huh?'
    message.reply_channel.send({
        'text': reply_text,
    })
