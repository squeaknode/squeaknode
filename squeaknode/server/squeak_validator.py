import logging

from squeak.core import CheckSqueak
from squeak.core import CheckSqueakError
from squeak.core import CSqueak

logger = logging.getLogger(__name__)


class SqueakValidator(object):
    """Validates incoming squeaks"""

    def __init__(self) -> None:
        pass

    def validate(self, squeak: CSqueak) -> bool:
        if not squeak:
            return False

        try:
            CheckSqueak(squeak)
            return True
        except CheckSqueakError as e:
            logger.info("Got invalid squeak with error: {}".format(e))
            return False
