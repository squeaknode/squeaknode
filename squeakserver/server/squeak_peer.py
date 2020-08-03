from collections import namedtuple

SqueakPeer = namedtuple(
    "SqueakPeer", "peer_id, peer_name, host, port, publishing, subscribed",
)
