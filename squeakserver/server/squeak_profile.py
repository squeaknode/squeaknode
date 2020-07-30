from collections import namedtuple

SqueakProfile = namedtuple(
    "SqueakProfile",
    "profile_id, profile_name, private_key, address, shared, following, whitelisted",
)
