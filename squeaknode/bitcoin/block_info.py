from dataclasses import dataclass

@dataclass
class BlockInfo:
    """Class for getting block info from blockchain."""
    block_height: int
    block_hash: str
    block_header: bytes
