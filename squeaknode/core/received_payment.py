from collections import namedtuple

ReceivedPayment = namedtuple(
    "ReceivedPayment",
    "received_payment_id, created, squeak_hash, payment_hash, price_msat, settle_index, client_addr",
)
