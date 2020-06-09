

class BuyOffer():

    def __init__(self, squeak_hash, nonce, amount, preimage_hash, payment_request):
        self.squeak_hash = squeak_hash
        self.nonce = nonce
        self.amount = amount
        self.preimage_hash = preimage_hash
        self.payment_request = payment_request
