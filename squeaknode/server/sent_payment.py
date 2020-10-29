from collections import namedtuple

SentPayment = namedtuple(
    "SentPayment",
    "sent_payment_id, offer_id, peer_id, squeak_hash, preimage_hash, preimage, amount, node_pubkey, preimage_is_valid",
)
