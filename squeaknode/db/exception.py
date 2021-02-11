
class SqueakDatabaseError(Exception):
    """Base class for other squeak database exceptions"""


class DuplicateReceivedPaymentError(SqueakDatabaseError):
    """Raised when the inserted received payment is a duplicate"""
