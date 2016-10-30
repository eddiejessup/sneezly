from channels.routing import route

from track import consumers as track_consumers

channel_routing = [
    route("websocket.connect", track_consumers.ws_add),
    route("websocket.receive", track_consumers.ws_message),
    route("websocket.disconnect", track_consumers.ws_disconnect),
]
