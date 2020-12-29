from dataclasses import dataclass


@dataclass
class BlockInfo:
    """Class for getting block info from blockchain."""

    block_height: int
    block_hash: bytes
    block_header: bytes
