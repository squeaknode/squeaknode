#!/usr/bin/env bash

git clone https://github.com/googleapis/googleapis.git
curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto

cp rpc.proto squeaknode/common

python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. squeaknode/common/rpc.proto
python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. squeaknode/client/rpc/route_guide.proto
