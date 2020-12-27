FROM python:3.8-slim

# RUN apt-get update && apt-get install -y \
# 	git

COPY requirements-itest.txt /
COPY libs /libs

RUN pip3 install -r requirements-itest.txt

WORKDIR /app

# Download the rpc files.
# RUN git clone https://github.com/googleapis/googleapis.git

COPY proto ./proto
COPY itests/test.sh squeaknode/lightning/lnd_lightning_client.py ./
COPY itests/tests ./tests

# # Install the gRPC files.
# RUN chmod +x install-rpc.sh && \
# 	./install-rpc.sh

RUN python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. \
	proto/lnd.proto \
	proto/squeak_server.proto \
	proto/squeak_admin.proto


RUN chmod +x test.sh

CMD ["bash", "test.sh"]
