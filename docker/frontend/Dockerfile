#FROM node:10-stretch
FROM ubuntu:20.04

ARG PORT

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
	REACT_APP_PORT=${PORT} \
	npm run build

EXPOSE 8081
CMD ["serve", "-s", "build", "-l", "8081"]
