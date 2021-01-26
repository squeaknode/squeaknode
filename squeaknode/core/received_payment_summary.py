from typing import NamedTuple


class ReceivedPaymentSummary(NamedTuple):
    """Represents information about payments received."""
    num_received_payments: int
    total_amount_received_msat: int
