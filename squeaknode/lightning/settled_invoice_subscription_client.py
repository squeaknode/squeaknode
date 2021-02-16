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
        latest_settle_index: int,
        stopped: threading.Event,
        retry_s: int = 10,
    ):
        self.lightning_client = lightning_client
        self.latest_settle_index = latest_settle_index
        self.stopped = stopped
        self.retry_s = retry_s
        self.result_stream = None

    @contextmanager
    def open_subscription(self):
        logger.info(
            "Getting invoices from settle_index: {}".format(
                self.latest_settle_index,
            )
        )
        self.result_stream = self.lightning_client.subscribe_invoices(
            settle_index=self.latest_settle_index,
        )
        threading.Thread(
            target=self.wait_for_stop,
        ).start()
        try:
            yield self
        finally:
            self.stopped.set()

    def wait_for_stop(self):
        self.stopped.wait()
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
                        exc_info=True,
                    )
            self.stopped.wait(self.retry_s)
