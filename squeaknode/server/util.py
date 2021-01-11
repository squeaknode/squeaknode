

def parse_ip_address(grpc_addr_str: str) -> str:
    return grpc_addr_str.split(':')[1]
