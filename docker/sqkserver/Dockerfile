FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	python3-pip \
	curl \
	git

COPY requirements.txt /

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Download the rpc files.
RUN git clone https://github.com/googleapis/googleapis.git
RUN curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto

# Copy the source code.
COPY . /app

# Copy the source code.
RUN cp -r googleapis /app
RUN cp rpc.proto /app

WORKDIR /app

# Install the gRPC files.
COPY "install-rpc.sh" .
RUN chmod +x install-rpc.sh
RUN ./install-rpc.sh

RUN python3 setup.py install

# Copy the config file template.
COPY "docker/sqkserver/config.ini.sh" .

# Copy the entrypoint script.
COPY "docker/sqkserver/start-sqkserver.sh" .
RUN chmod +x start-sqkserver.sh
