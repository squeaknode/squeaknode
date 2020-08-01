from collections import namedtuple

SqueakSubscription = namedtuple(
    "SqueakSubscription", "subscription_id, subscription_name, host, port, sharing, following",
)
