import logging

logger = logging.getLogger(__name__)


class PeerClient:
    def __init__(self, host, port, squeak_server_client):
        self.host = host
        self.port = port
        self.squeak_server_client = squeak_server_client

    def get_stub(self):
        return self.squeak_server_client.get_stub(
            self.host,
            self.port,
        )

    def lookup_squeaks(self, addresses, min_block, max_block):
        with self.get_stub() as stub:
            return self.squeak_server_client.lookup_squeaks(
                stub,
                addresses,
                min_block,
                max_block,
            )

    def post_squeak(self, squeak):
        with self.get_stub() as stub:
            return self.squeak_server_client.post_squeak(
                stub,
                squeak,
            )

    def get_squeak(self, squeak_hash):
        with self.get_stub() as stub:
            return self.squeak_server_client.get_squeak(
                stub,
                squeak_hash,
            )

    def buy_squeak(self, squeak_hash):
        with self.get_stub() as stub:
            return self.squeak_server_client.buy_squeak(
                stub,
                squeak_hash,
            )
