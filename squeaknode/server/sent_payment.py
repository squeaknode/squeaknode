from collections import namedtuple

SentPayment = namedtuple(
    "SentPayment",
    "sent_payment_id, offer_id, peer_id, squeak_hash, preimage_hash, preimage, price_msat, node_pubkey, preimage_is_valid, time_ms",
)
