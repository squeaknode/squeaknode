FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -qq update && apt-get -qq install -y \
	curl \
	unzip \
	nodejs \
	npm \
	git \
	git-core

RUN npm install -g serve

WORKDIR /tmp

RUN curl -sSL https://github.com/protocolbuffers/protobuf/releases/download/v3.12.2/\
protoc-3.12.2-linux-x86_64.zip -o protoc.zip && \
  unzip -qq protoc.zip && \
  cp ./bin/protoc /usr/local/bin/protoc

RUN curl -sSL https://github.com/grpc/grpc-web/releases/download/1.2.0/\
protoc-gen-grpc-web-1.2.0-linux-x86_64 -o /usr/local/bin/protoc-gen-grpc-web && \
  chmod +x /usr/local/bin/protoc-gen-grpc-web

COPY frontend/squeak-node-frontend .

# Copy the proto files
COPY proto/* src/proto/

RUN cd src && \
	protoc -I=. proto/squeak_admin.proto proto/lnd.proto \
	--js_out=import_style=commonjs:. \
	--grpc-web_out=import_style=commonjs,mode=grpcwebtext:.

# Copy the eslint prepend script.
COPY "docker/frontend/pb_disable-eslint.sh" .
RUN chmod +x pb_disable-eslint.sh && \
	./pb_disable-eslint.sh src/proto/

RUN npm install && \
	npm run build



ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	python3-pip \
	python3-psycopg2 \
	git

WORKDIR /

COPY requirements.txt /

RUN pip3 install --upgrade pip && \
	pip3 install -r requirements.txt

WORKDIR /app

# Download the rpc files.
RUN git clone https://github.com/googleapis/googleapis.git

# Copy the source code.
COPY squeakserver ./squeakserver
COPY proto ./proto
COPY setup.py setup.cfg MANIFEST.in README.md ./

# Copy the frontend code
# COPY frontend/squeak-node-frontend/build/ ./static/build
RUN mkdir ./static && \
	cp -r /tmp/build ./static/build

RUN python3 setup.py install

EXPOSE 8774
EXPOSE 8994
EXPOSE 18774
EXPOSE 18994
# Web server
EXPOSE 12994

# Copy the entrypoint script.
COPY "docker/sqkserver/start-sqkserver.sh" .
RUN chmod +x start-sqkserver.sh
