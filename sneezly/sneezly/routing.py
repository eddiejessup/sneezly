from channels.routing import route

from track.consumers import ws_echo

channel_routing = [
    route('websocket.receive', ws_echo),
]
