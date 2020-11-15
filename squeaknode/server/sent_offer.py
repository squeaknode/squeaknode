from collections import namedtuple

SentOffer = namedtuple(
    "SentOffer",
    "sent_offer_id, squeak_hash, preimage_hash, preimage, price_msat, invoice_time, invoice_expiry, client_addr",
)
