#!/usr/bin/env bash

if [ ! -d "googleapis" ]; then
    git clone https://github.com/googleapis/googleapis.git
fi

if [ ! -f "rpc.proto" ]; then
    curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto
fi

# Move this to squeakserver/common/lnd/rpc.proto instead.
cp rpc.proto squeakserver/common/rpc/lnd.proto
# cp rpc.proto lnd.proto

echo "Installing RPC protocol files"
# install lnd protocol
python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. squeakserver/common/rpc/lnd.proto
# install lnd protocol at the top level
# python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. lnd.proto

# install squeak server protocol
python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. squeakserver/common/rpc/squeak_server.proto

# install squeak client protocol
# python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. squeakserver/client/rpc/route_guide.proto
