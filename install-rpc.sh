#!/usr/bin/env bash

if [ ! -d "googleapis" ]; then
    git clone https://github.com/googleapis/googleapis.git
fi

echo "Installing RPC protocol files"
python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. \
	proto/lnd.proto \
	proto/squeak_server.proto \
	proto/squeak_admin.proto
