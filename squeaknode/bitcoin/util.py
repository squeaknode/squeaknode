from bitcoin.core import CBlockHeader


def parse_block_header(header_bytes: bytes) -> CBlockHeader:
    return CBlockHeader.deserialize(header_bytes)
