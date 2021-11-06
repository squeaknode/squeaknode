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
from typing import Optional

from squeak.core import CSqueak

from squeaknode.core.interests import squeak_matches_interest
from squeaknode.core.offer import Offer
from squeaknode.core.peer_address import PeerAddress
from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)


class DownloadHandler:
    """Handles received squeaks.
    """

    def __init__(self, squeak_controller: SqueakController):
        self.squeak_controller = squeak_controller

    def handle_squeak(self, squeak: CSqueak):
        """Handle a new received squeak.

        """
        # Try saving squeak as active download
        saved_squeak_hash = self.save_active_download_squeak(squeak)
        if saved_squeak_hash is None:
            saved_squeak_hash = self.save_followed_squeak(squeak)
        if saved_squeak_hash is not None:
            self.squeak_controller.request_offers(saved_squeak_hash)

    def handle_offer(self, offer: Offer, peer_address: PeerAddress):
        """Handle a new received offer.

        """
        received_offer_id = self.squeak_controller.save_received_offer(
            offer, peer_address)
        if received_offer_id is None:
            return
        counter = self.squeak_controller.get_download_offer_counter(offer)
        if counter is not None:
            counter.increment()

    def save_active_download_squeak(self, squeak: CSqueak) -> Optional[bytes]:
        """Save the given squeak as a result of an active download.

        Returns:
          bytes: the hash of the saved squeak.
        """
        counter = self.squeak_controller.get_download_squeak_counter(squeak)
        if counter is None:
            return None
        saved_squeak_hash = self.squeak_controller.save_squeak(squeak)
        if saved_squeak_hash is None:
            return None
        counter.increment()
        return saved_squeak_hash

    def save_followed_squeak(self, squeak: CSqueak) -> Optional[bytes]:
        """Save the given squeak because it matches the followed
        interest criteria.

        Returns:
          bytes: the hash of the saved squeak.
        """
        if not self.squeak_matches_interest(squeak):
            return None
        return self.squeak_controller.save_squeak(squeak)

    def squeak_matches_interest(self, squeak: CSqueak) -> bool:
        locator = self.squeak_controller.get_interested_locator()
        for interest in locator.vInterested:
            if squeak_matches_interest(squeak, interest) \
               and self.squeak_controller.squeak_in_limit_of_interest(squeak, interest):
                return True
        return False
