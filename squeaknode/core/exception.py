
class SqueakCoreError(Exception):
    """Base class for other squeak core exceptions"""


class ProcessReceivedPaymentError(SqueakCoreError):
    """Raised when unable to process received payments"""
