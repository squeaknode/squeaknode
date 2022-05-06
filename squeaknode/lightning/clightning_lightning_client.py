# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import time
import uuid

from pyln.client import LightningRpc

from squeaknode.lightning.info import Info
from squeaknode.lightning.invoice import Invoice
from squeaknode.lightning.invoice_stream import InvoiceStream
from squeaknode.lightning.lightning_client import LightningClient
from squeaknode.lightning.pay_req import PayReq
from squeaknode.lightning.payment import Payment


logger = logging.getLogger(__name__)


class CLightningClient(LightningClient):
    """Access a c-lightning instance using the Python API."""

    def __init__(
        self,
        rpc_path: str,
    ) -> None:
        self.rpc_path = rpc_path
        # Create an instance of the LightningRpc object using the Core Lightning daemon on your computer.
        logger.info('initializing clightning client: {}'.format(self.rpc_path))
        self.lrpc = LightningRpc(self.rpc_path)

    def init(self):
        pass

    def pay_invoice(self, payment_request: str) -> Payment:
        payment = self.lrpc.pay(payment_request)
        logger.info('payment: {}'.format(payment))
        if payment['status'] == 'complete':
            return Payment(
                payment_preimage=bytes.fromhex(payment['payment_preimage']),
                payment_error='',
            )
        else:
            return Payment(
                payment_preimage=b'',
                payment_error='Payment failed.',
            )

    def get_info(self) -> Info:
        info = self.lrpc.getinfo()
        pubkey = info['id']
        binding = info.get('binding')
        logger.info(binding)
        uris = []
        if binding:
            for b in binding:
                address = b['address']
                if ':' not in address:  # TODO: Change type of uri to LightningAddress.
                    port = b['port']
                    uri = f"{pubkey}@{address}:{port}"
                    logger.info(uri)
                    uris.append(uri)

        # get_info_request = lnd_pb2.GetInfoRequest()
        # get_info_response = self.stub.GetInfo(
        #     get_info_request,
        # )
        # return Info(
        #     uris=get_info_response.uris,
        # )
        return Info(
            uris=uris,
        )

    def decode_pay_req(self, payment_request: str) -> PayReq:
        pay_req = self.lrpc.decodepay(payment_request)
        return PayReq(
            payment_hash=bytes.fromhex(pay_req['payment_hash']),
            payment_point=b'',  # TODO: Use real payment point.
            num_msat=pay_req['amount_msat'].millisatoshis,
            destination=pay_req['payee'],
            timestamp=int(pay_req['created_at']),
            expiry=int(pay_req['expiry']),
        )

    # def lookup_invoice(self, r_hash_str: str) -> lnd_pb2.Invoice:
    #     payment_hash = lnd_pb2.PaymentHash(
    #         r_hash_str=r_hash_str,
    #     )
    #     return self.stub.LookupInvoice(payment_hash)

    def create_invoice(self, preimage: bytes, amount_msat: int) -> Invoice:
        logger.info('preimage: {}'.format(preimage.hex()))
        logger.info('amount msat: {}'.format(amount_msat))
        created_invoice = self.lrpc.invoice(
            amount_msat,
            label=str(uuid.uuid4()),
            description="Squeaknode invoice",
            preimage=preimage.hex(),
        )
        logger.info('created invoice: {}'.format(created_invoice))

        # add_invoice_response = self.add_invoice(preimage, amount_msat)
        # payment_hash = add_invoice_response.r_hash
        # lookup_invoice_response = self.lookup_invoice(
        #     payment_hash.hex()
        # )
        # return Invoice(
        #     r_hash=lookup_invoice_response.r_hash,
        #     payment_request=lookup_invoice_response.payment_request,
        #     value_msat=amount_msat,
        #     settled=lookup_invoice_response.settled,
        #     settle_index=lookup_invoice_response.settle_index,
        #     creation_date=lookup_invoice_response.creation_date,
        #     expiry=lookup_invoice_response.expiry,
        # )

        creation_time = int(time.time())
        expiry = int(created_invoice['expires_at']) - creation_time
        logger.info('creation_time: {}'.format(creation_time))
        logger.info('expiry: {}'.format(expiry))

        return Invoice(
            r_hash=bytes.fromhex(created_invoice['payment_hash']),
            payment_request=created_invoice['bolt11'],
            value_msat=amount_msat,
            settled=False,
            settle_index=0,
            creation_date=creation_time,
            expiry=expiry,
        )

    def subscribe_invoices(self, settle_index: int) -> InvoiceStream:
        # subscribe_invoices_request = lnd_pb2.InvoiceSubscription(
        #     settle_index=settle_index,
        # )
        # subscribe_result = self.stub.SubscribeInvoices(
        #     subscribe_invoices_request,
        # )
        # return InvoiceStream(
        #     cancel=subscribe_result.cancel,
        #     result_stream=iter(subscribe_result),
        # )
        def cancel_fn():
            return None

        return InvoiceStream(
            cancel=cancel_fn,
            result_stream=iter([]),
        )
