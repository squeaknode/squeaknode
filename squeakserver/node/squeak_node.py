from squeakserver.node.squeak_block_verifier import SqueakBlockVerifier
from squeakserver.node.squeak_block_periodic_worker import SqueakBlockPeriodicWorker
from squeakserver.node.squeak_block_queue_worker import SqueakBlockQueueWorker


class SqueakNode:

    def __init__(self, postgres_db, blockchain_client, lightning_client, lightning_host_port, price):
        self.postgres_db = postgres_db
        self.blockchain_client = blockchain_client
        self.lightning_client = lightning_client
        self.lightning_host_port = lightning_host_port
        self.price = price
        self.squeak_block_verifier = SqueakBlockVerifier(postgres_db, blockchain_client)
        self.squeak_block_periodic_worker = SqueakBlockPeriodicWorker(self.squeak_block_verifier)
        self.squeak_block_queue_worker = SqueakBlockQueueWorker(self.squeak_block_verifier)

    def start_running(self):
        # self.squeak_block_periodic_worker.start_running()
        self.squeak_block_queue_worker.start_running()

    def save_squeak(self, squeak):
        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        self.squeak_block_verifier.add_squeak_to_queue(inserted_squeak_hash)

