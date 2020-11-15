from collections import namedtuple

ReceivedPayment = namedtuple(
    "ReceivedPayment",
    "received_payment_id, created, squeak_hash, preimage_hash, price_msat, settle_index, client_addr",
)
