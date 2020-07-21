FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	python3-pip \
	python3-psycopg2 \
	git

# Download the rpc files.
RUN git clone https://github.com/googleapis/googleapis.git

COPY requirements.txt /

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the source code.
COPY . /app

# Copy the downloaded rpc files.
RUN cp -r googleapis /app

WORKDIR /app

# Install the gRPC files.
COPY "install-rpc.sh" .
RUN chmod +x install-rpc.sh
RUN ./install-rpc.sh

RUN python3 setup.py install

EXPOSE 8774
EXPOSE 8994
EXPOSE 18774
EXPOSE 18994

# Copy the entrypoint script.
COPY "docker/sqkserver/start-sqkserver.sh" .
RUN chmod +x start-sqkserver.sh
