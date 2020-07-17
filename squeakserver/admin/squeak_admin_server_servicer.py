import logging
from concurrent import futures

import grpc

from squeak.core import CSqueak

from squeakserver.admin.rpc import squeak_admin_pb2
from squeakserver.admin.rpc import squeak_admin_pb2_grpc
from squeakserver.server.util import get_hash


logger = logging.getLogger(__name__)


class SqueakAdminServerServicer(squeak_admin_pb2_grpc.SqueakAdminServicer):
    """Provides methods that implement functionality of squeak admin server."""

    def __init__(self, host, port, handler):
        self.host = host
        self.port = port
        self.handler = handler

    def GetBalance(self, request, context):
        wallet_balance_response = self.handler.handle_get_balance()
        return squeak_admin_server_pb2.GetBalanceReply(
            walletBalanceResponse=wallet_balance_response,
        )

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        squeak_admin_pb2_grpc.add_SqueakAdminServicer_to_server(
            self, server)
        server.add_insecure_port('{}:{}'.format(self.host, self.port))
        server.start()
        server.wait_for_termination()
