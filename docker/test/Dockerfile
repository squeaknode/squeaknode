FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	python3-pip \
	curl \
	git

# Download the rpc files.
RUN git clone https://github.com/googleapis/googleapis.git
RUN curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto

COPY requirements-itest.txt /

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements-itest.txt

# Copy the source code.
COPY . /app

# Copy the downloaded rpc files.
RUN cp -r googleapis /app
RUN cp rpc.proto /app

WORKDIR /app

# Install the gRPC files.
COPY "install-rpc.sh" .
RUN chmod +x install-rpc.sh
RUN ./install-rpc.sh

# Copy the lighting client
COPY "squeakserver/common/lnd_lightning_client.py" .

# Copy the entrypoint script.
COPY "itests/test.sh" .
COPY "itests/test.py" .
RUN chmod +x test.sh

CMD ["bash", "test.sh"]
