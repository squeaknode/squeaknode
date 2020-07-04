FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	python3-pip \
	python3-psycopg2 \
	curl \
	git

# Download the rpc files.
RUN git clone https://github.com/googleapis/googleapis.git
RUN curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto

COPY requirements.txt /

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Install the local squeaklib
COPY squeak /squeak
RUN pip3 install -e /squeak

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

EXPOSE 8774

CMD ["runsqueakserver", "--config", "config.ini", "--log-level", "DEBUG", "run-server"]
