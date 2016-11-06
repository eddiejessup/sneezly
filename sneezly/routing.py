from channels.routing import route

from track import consumers as track_consumers

channel_routing = [
    route('slack.message', track_consumers.slack_message),
    route('slack.hello', track_consumers.slack_connect),
]
