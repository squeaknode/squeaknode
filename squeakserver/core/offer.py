from collections import namedtuple

Offer = namedtuple("Offer", [
    "offer_id",
    "squeak_hash",
    "key_cipher",
    "iv",
    "amount",
    "preimage_hash",
    "payment_request",
    "node_pubkey",
    "node_host",
    "node_port",
    "proof",
    "peer_id",
])
