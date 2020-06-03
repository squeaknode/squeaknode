#!/usr/bin/env bash

if [ ! -d "googleapis" ]; then
    git clone https://github.com/googleapis/googleapis.git
fi

if [ ! -f "rpc.proto" ]; then
    curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto
fi

# Move this to squeaknode/common/lnd/rpc.proto instead.
cp rpc.proto squeaknode/common

echo "Installing RPC protocol files"
# install lnd protocol
python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. squeaknode/common/rpc.proto

# install squeak server protocol
python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. squeaknode/common/rpc/squeak.proto

# install squeak client protocol
python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. squeaknode/client/rpc/route_guide.proto
