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
import binascii
import logging
import struct
from typing import Iterable

import zmq.asyncio

logger = logging.getLogger(__name__)


class BitcoinBlockSubscriptionClient:
    """Get an iterator of new bitcoin blocks."""

    def __init__(
        self,
        host: str,
        port: int,
    ) -> None:
        self.zmqContext = zmq.Context()
        self.zmqSubSocket = self.zmqContext.socket(zmq.SUB)
        self.zmqSubSocket.setsockopt(zmq.RCVHWM, 0)
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "hashblock")
        self.zmqSubSocket.connect("tcp://{}:{}".format(host, port))

    def get_blocks(self) -> Iterable[bytes]:
        while True:
            topic, body, seq = self.zmqSubSocket.recv_multipart()
            sequence = "Unknown"
            if len(seq) == 4:
                sequence = str(struct.unpack('<I', seq)[-1])
            if topic == b"hashblock":
                logger.debug('- HASH BLOCK (' + sequence + ') -')
                logger.debug(binascii.hexlify(body))
                logger.debug('body type: {}'.format(type(body)))
                logger.debug('body: {}'.format(body))
                yield body
