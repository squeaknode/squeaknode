FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	python3-pip \
	curl \
	git

COPY requirements.txt /

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Install the gRPC files for lnd.
RUN git clone https://github.com/googleapis/googleapis.git
RUN curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto

COPY . /app
RUN cp -r googleapis /app
RUN cp rpc.proto /app/squeaknode/common

WORKDIR /app

RUN python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. squeaknode/common/rpc.proto
RUN python3 -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. squeaknode/client/rpc/route_guide.proto
RUN python3 setup.py install

# Copy the entrypoint script.
COPY "docker/sqkclient/start-sqkclient.sh" .
RUN chmod +x start-sqkclient.sh
