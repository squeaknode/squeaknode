from collections import namedtuple

SentOffer = namedtuple(
    "SentOffer",
    "sent_offer_id, squeak_hash, payment_hash, secret_key, nonce, price_msat, payment_request, invoice_time, invoice_expiry, client_addr",
)
