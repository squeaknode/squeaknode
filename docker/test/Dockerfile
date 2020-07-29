FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	python3-pip \
	git

COPY requirements-itest.txt /

RUN pip3 install --upgrade pip && \
	pip3 install -r requirements-itest.txt

WORKDIR /app

# Download the rpc files.
RUN git clone https://github.com/googleapis/googleapis.git

COPY proto ./proto
COPY install-rpc.sh itests/test.sh squeakserver/common/lnd_lightning_client.py ./
COPY itests/tests ./tests

# Install the gRPC files.
RUN chmod +x install-rpc.sh && \
	./install-rpc.sh

RUN chmod +x test.sh

CMD ["bash", "test.sh"]
