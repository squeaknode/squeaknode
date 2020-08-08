from collections import namedtuple

Offer = namedtuple("Offer", [
    "offer_id",
    "squeak_hash",
    "key_cipher",
    "iv",
    "price_msat",
    "payment_hash",
    "payment_request",
    "destination",
    "node_host",
    "node_port",
    "proof",
    "peer_id",
])
