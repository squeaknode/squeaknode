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

#COPY frontend/squeak-frontend .
COPY frontend/react-material-admin .

# Copy the proto files
RUN mkdir proto
COPY proto/* src/proto/

RUN cd src && \
	protoc -I=. proto/squeak_admin.proto proto/lnd.proto \
	--js_out=import_style=commonjs:. \
	--grpc-web_out=import_style=commonjs,mode=grpcwebtext:.

# Copy the eslint prepend script.
COPY "docker/frontend/pb_disable-eslint.sh" .
RUN chmod +x pb_disable-eslint.sh
RUN ./pb_disable-eslint.sh src/proto/

RUN npm install
RUN npm run build
RUN npm install -g serve

EXPOSE 8081
CMD ["serve", "-s", "build", "-l", "8081"]
