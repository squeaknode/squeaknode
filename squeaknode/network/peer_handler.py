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
import queue
import socket
import threading
from typing import Optional

from squeaknode.core.peer_address import PeerAddress


logger = logging.getLogger(__name__)


class PeerHandler():
    """Handles new peer connection.
    """

    def __init__(
            self,
            connection_manager,
            squeak_controller,
    ):
        self.connection_manager = connection_manager
        self.squeak_controller = squeak_controller

    def handle_connection(
            self,
            peer_socket: socket.socket,
            address: PeerAddress,
            outgoing: bool,
            result_queue: Optional[queue.Queue] = None,
    ):
        """Handle a new socket connection.

        This method blocks until the peer connection is established.
        """
        # Create a dummy queue if not needed.
        if result_queue is None:
            result_queue = queue.Queue()

        threading.Thread(
            target=self.start_connection,
            args=(
                peer_socket,
                address,
                outgoing,
                result_queue,
            ),
        ).start()

    def start_connection(
            self,
            peer_socket: socket.socket,
            address: PeerAddress,
            outgoing: bool,
            result_queue: queue.Queue,
    ):
        """Start a connection
        """
        with self.connection_manager.connect(
                peer_socket,
                address,
                outgoing,
                self.squeak_controller,
                result_queue,
        ) as connection:
            connection.handle_connection()
