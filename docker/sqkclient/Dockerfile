FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	python3-pip \
	curl \
	git

COPY requirements.txt /

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


COPY . /app
WORKDIR /app

# Install the gRPC files.
COPY "install-rpc.sh" .
RUN chmod +x install-rpc.sh

RUN python3 setup.py install

# Copy the config file template.
COPY "docker/sqkclient/config.ini.sh" .

# Copy the entrypoint script.
COPY "docker/sqkclient/start-sqkclient.sh" .
RUN chmod +x start-sqkclient.sh
