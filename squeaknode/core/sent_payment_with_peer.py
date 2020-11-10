from collections import namedtuple

SentPaymentWithPeer = namedtuple(
    "SentPaymentWithPeer",
    [
        "sent_payment",
        "peer",
    ],
)
