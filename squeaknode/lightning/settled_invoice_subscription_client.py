import logging
import threading
from contextlib import contextmanager

import grpc

from squeaknode.core.exception import ProcessReceivedPaymentError
from squeaknode.lightning.lnd_lightning_client import LNDLightningClient

logger = logging.getLogger(__name__)

DEFAULT_MAX_QUEUE_SIZE = 1000
DEFAULT_UPDATE_INTERVAL_S = 1


class SettledInvoiceSubscriptionClient:
    def __init__(
        self,
        lightning_client: LNDLightningClient,
        latest_settle_index: int,
        stopped: threading.Event,
    ):
        self.lightning_client = lightning_client
        self.latest_settle_index = latest_settle_index
        self.stopped = stopped
        self.result_stream = None

    @contextmanager
    def open_subscription(self):
        logger.info(
            "Getting invoices from settle_index: {}".format(
                self.latest_settle_index)
        )
        self.result_stream = self.lightning_client.subscribe_invoices(
            settle_index=self.latest_settle_index,
        )
        threading.Thread(
            target=self.wait_for_stop,
        ).start()
        try:
            logger.info("Before yielding settled invoice client...")
            yield self
            logger.info("After yielding settled invoice client...")
        finally:
            logger.info("Stopping settled invoice client...")
            self.stopped.set()
            logger.info("Stopped settled invoice client...")

    def wait_for_stop(self):
        logger.info("Waiting for stop event.")
        self.stopped.wait()
        logger.info("Cancelled subscription.")
        self.result_stream.cancel()

    def get_settled_invoices(self):
        if self.result_stream is None:
            raise Exception("Result stream has not been initialized.")
        try:
            for invoice in self.result_stream:
                if invoice.settled:
                    logger.info(
                        "Yield settled invoice: {}".format(invoice)
                    )
                    yield invoice
        except grpc.RpcError as e:
            if e.code() != grpc.StatusCode.CANCELLED:
                raise ProcessReceivedPaymentError()
