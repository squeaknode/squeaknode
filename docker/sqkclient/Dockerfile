FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	python3-pip \
	python3-psycopg2 \
	curl \
	git

# install nc
RUN apt-get update && apt-get install -y netcat

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
COPY "docker/sqkclient/config.ini.sh" .

# Copy the entrypoint script.
COPY "docker/sqkclient/start-sqkclient.sh" .
RUN chmod +x start-sqkclient.sh
