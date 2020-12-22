from collections import namedtuple

Offer = namedtuple(
    "Offer",
    [
        "offer_id",
        "squeak_hash",
        "price_msat",
        "payment_hash",
        "payment_point",
        "invoice_timestamp",
        "invoice_expiry",
        "payment_request",
        "destination",
        "node_host",
        "node_port",
        "peer_id",
    ],
)
