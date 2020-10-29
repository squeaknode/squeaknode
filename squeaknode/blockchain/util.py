from bitcoin.core import CBlockHeader


def parse_block_header(header_bytes: bytes):
    return CBlockHeader.deserialize(header_bytes)
