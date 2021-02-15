import logging
import threading
from contextlib import contextmanager

import grpc

from squeaknode.lightning.lnd_lightning_client import LNDLightningClient

logger = logging.getLogger(__name__)


class SettledInvoiceSubscriptionClient:
    def __init__(
        self,
        lightning_client: LNDLightningClient,
        get_latest_settle_index_fn,
        stopped: threading.Event,
        retry_s: int = 10,
    ):
        self.lightning_client = lightning_client
        self.get_latest_settle_index_fn = get_latest_settle_index_fn
        self.stopped = stopped
        self.retry_s = retry_s
        self.result_stream = None

    @contextmanager
    def open_subscription(self):
        settle_index = self.get_latest_settle_index_fn()
        logger.info(
            "Getting invoices from settle_index: {}".format(
                settle_index,
            )
        )
        self.result_stream = self.lightning_client.subscribe_invoices(
            settle_index=settle_index,
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
        while not self.stopped.is_set():
            try:
                for invoice in self.result_stream:
                    if invoice.settled:
                        logger.info(
                            "Yield settled invoice: {}".format(invoice)
                        )
                        yield invoice
            except grpc.RpcError as e:
                if e.code() != grpc.StatusCode.CANCELLED:
                    logger.error(
                        "Unable to subscribe invoices from lnd. Retrying in "
                        "{} seconds.".format(self.retry_s),
                    )
            self.stopped.wait(self.retry_s)
