from collections import namedtuple

Offer = namedtuple("Offer", [
    "squeak_hash",
    "key_cipher",
    "iv",
    "amount",
    "preimage_hash",
    "payment_request",
    "pubkey",
    "host",
    "port",
    "proof",
])
