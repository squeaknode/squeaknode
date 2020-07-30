from collections import namedtuple

SqueakServer = namedtuple(
    "SqueakServer",
    "server_id, server_name, host, port, sharing, following",
)
