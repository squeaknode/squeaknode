from collections import namedtuple

SentPayment = namedtuple(
    "SentPayment",
    "sent_payment_id, offer_id, peer_id, squeak_hash, payment_hash, secret_key, price_msat, node_pubkey, time_ms",
)
