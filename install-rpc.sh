#!/usr/bin/env bash

if [ ! -d "googleapis" ]; then
    git clone https://github.com/googleapis/googleapis.git
fi

if [ ! -f "rpc.proto" ]; then
    curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto
fi

# Move this to squeakserver/common/lnd/rpc.proto instead.
cp rpc.proto proto/lnd.proto

echo "Installing RPC protocol files"
# install lnd protocol
python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. \
	proto/lnd.proto \
	proto/squeak_server.proto \
	proto/squeak_admin.proto
