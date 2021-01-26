from typing import NamedTuple


class ReceivedPaymentSummary(NamedTuple):
    """Represents information about payments receive and sent."""
    num_received_payments: int
    num_sent_payments: int
    total_amount_received_msat: int
    total_amount_sent_msat: int
