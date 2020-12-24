class BuyOffer:
    def __init__(
        self,
        squeak_hash,
        price_msat,
        nonce,
        payment_request,
        pubkey,
        host,
        port,
    ):
        self.squeak_hash = squeak_hash
        self.price_msat = price_msat
        self.nonce = nonce
        self.payment_request = payment_request
        self.pubkey = pubkey
        self.host = host
        self.port = port
