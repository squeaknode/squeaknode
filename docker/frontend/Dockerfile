FROM node:10-stretch

RUN apt-get -qq update && apt-get -qq install -y \
  unzip

WORKDIR /tmp

RUN curl -sSL https://github.com/protocolbuffers/protobuf/releases/download/v3.12.2/\
protoc-3.12.2-linux-x86_64.zip -o protoc.zip && \
  unzip -qq protoc.zip && \
  cp ./bin/protoc /usr/local/bin/protoc

RUN curl -sSL https://github.com/grpc/grpc-web/releases/download/1.2.0/\
protoc-gen-grpc-web-1.2.0-linux-x86_64 -o /usr/local/bin/protoc-gen-grpc-web && \
  chmod +x /usr/local/bin/protoc-gen-grpc-web

COPY frontend/squeak-frontend .

# Copy the proto files
RUN mkdir proto
COPY proto/squeak_admin.proto proto/
RUN curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto
RUN cp rpc.proto proto/lnd.proto

RUN protoc -I=. proto/squeak_admin.proto proto/lnd.proto \
	--js_out=import_style=commonjs:. \
	--grpc-web_out=import_style=commonjs,mode=grpcwebtext:.

# RUN npm install && \
# 	npm link grpc-web && \
# 	npx webpack client.js

RUN npm link grpc-web
RUN npm run build
RUN npm install -g serve

EXPOSE 8081
# CMD ["python", "-m", "SimpleHTTPServer", "8081"]
CMD ["serve", "-s", "build", "-l", "8081"]
