from squeaknode.core.peer_address import PeerAddress


def parse_client_address(grpc_addr_str: str) -> PeerAddress:
    _, host, port = grpc_addr_str.split(':')
    return PeerAddress(
        host=host,
        port=int(port),
    )
