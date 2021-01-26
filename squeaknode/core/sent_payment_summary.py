from typing import NamedTuple


class SentPaymentSummary(NamedTuple):
    """Represents information about payments sent."""
    num_sent_payments: int
    total_amount_sent_msat: int
