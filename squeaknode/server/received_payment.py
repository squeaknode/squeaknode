from collections import namedtuple

ReceivedPayment = namedtuple(
    "ReceivedPayment",
    "received_payment_id, squeak_hash, preimage_hash, price_msat, is_paid, payment_time",
)
